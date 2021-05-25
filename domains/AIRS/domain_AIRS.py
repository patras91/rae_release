#!/usr/bin/env python3
"""Domain definition for AIRS SDN to work with RAE and UPOM.

This file defines the tasks, methods, and commands for the AIRS SDN domain.
"""
__author__ = 'alex'
# From Sunandita on March 27, 2021: I modified the domain file to fit with the new object-oriented of the code base

from domains.constants import *
from shared.timer import DURATION
import numpy as np

class AIRSDomain():
    def __init__(self, state, rv, actor, env):
        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv

        # Declare commands in actor's engine
        actor.declare_commands([
            self.restart_vm,
            self.add_vcpu,
            self.increase_mem,
            self.kill_top_proc,
            self.apply_update,
            self.add_switch,
            self.move_critical_hosts,
            self.clear_ctrl_state_besteffort,
            self.clear_ctrl_state_fallback,
            self.reinstall_ctrl_besteffort,
            self.reinstall_ctrl_fallback,
            self.reconnect_switch_to_ctrl,
            self.clear_switch_state_besteffort,
            self.clear_switch_state_fallback,
            self.disconnect_reconnect_switch_port,
            self.disconnect_switch_port,
            self.succeed,
            self.unsure,
            self.fail
        ])

        #
        # Task-to-method mappings
        #

        self.actor.declare_task('fix_sdn', 'config', 'context')
        self.actor.declare_task('handle_event', 'event', 'config', 'context')

        self.actor.declare_task('fix_component', 'component_id', 'config', 'context')

        self.actor.declare_task('fix_low_resources', 'component_id', 'config', 'context')
        self.actor.declare_task('try_generic_fix', 'component_id', 'config', 'context')
        self.actor.declare_task('fix_sdn_controller', 'component_id', 'config', 'context')
        self.actor.declare_task('fix_switch', 'component_id', 'config', 'context')

        self.actor.declare_task('shrink_ctrl_hosttable', 'component_id', 'config', 'context')
        self.actor.declare_task('shrink_ctrl_switchtable', 'component_id', 'config', 'context')
        self.actor.declare_task('alleviate_ctrl_cpu', 'component_id', 'config', 'context')
        self.actor.declare_task('restore_ctrl_health', 'component_id', 'config', 'context')

        self.actor.declare_task('reconnect_ctrl', 'component_id', 'config', 'context')
        self.actor.declare_task('shrink_switch_flowtable', 'component_id', 'config', 'context')
        self.actor.declare_task('alleviate_switch_cpu', 'component_id', 'config', 'context')
        self.actor.declare_task('restore_switch_health', 'component_id', 'config', 'context')
        
        self.actor.declare_methods(
            'fix_sdn',
            self.m_fix_sdn
        )

        self.actor.declare_methods(
            'handle_event',
            self.m_handle_event
        )

        self.actor.declare_methods(
            'fix_component',
            self.m_fix_vm,
            #self.m_fix_software
        )
        self.actor.declare_methods(
            'fix_low_resources',
            self.m_add_vcpu,
            self.m_increase_mem
        )
        self.actor.declare_methods(
            'try_generic_fix',
            self.m_software_update,
            self.m_software_reinstall
        )
        self.actor.declare_methods(
            'fix_sdn_controller',
            self.m_ctrl_clearstate_besteffort,
            self.m_ctrl_mitigate_pktinflood,
            self.m_fix_sdn_controller_fallback
        )
        self.actor.declare_methods(
            'fix_switch',
            self.m_fix_switch
        )

        self.actor.declare_methods(
            'shrink_ctrl_hosttable',
            self.m_ctrl_clearstate_besteffort,
            self.m_ctrl_clearstate_fallback,
            self.m_ctrl_reinstall_besteffort,
            self.m_ctrl_reinstall_fallback
        )
        self.actor.declare_methods(
            'shrink_ctrl_switchtable',
            self.m_ctrl_clearstate_besteffort,
            self.m_ctrl_clearstate_fallback,
            self.m_ctrl_reinstall_besteffort,
            self.m_ctrl_reinstall_fallback
        )
        self.actor.declare_methods(
            'alleviate_ctrl_cpu',
            self.m_component_kill_top_proc,
            self.m_ctrl_reinstall_besteffort,
            self.m_ctrl_reinstall_fallback,
            self.m_component_restartvm
        )
        self.actor.declare_methods(
            'restore_ctrl_health',
            self.m_ctrl_reinstall_besteffort,
            self.m_ctrl_reinstall_fallback,
            self.m_component_restartvm
        )

        self.actor.declare_methods(
            'reconnect_ctrl',
            self.m_switch_reconnect_ctrl
        )
        self.actor.declare_methods(
            'shrink_switch_flowtable',
            self.m_switch_clearstate_besteffort,
            self.m_switch_clearstate_fallback
        )
        self.actor.declare_methods(
            'alleviate_switch_cpu',
            self.m_switch_discon_recon_txport,
            self.m_component_kill_top_proc,
            self.m_switch_clearstate_besteffort,
            self.m_switch_clearstate_fallback,
            self.m_switch_disconnect_txport
        )
        self.actor.declare_methods(
            'restore_switch_health',
            self.m_switch_discon_recon_txport,
            self.m_switch_clearstate_besteffort,
            self.m_switch_clearstate_fallback,
            self.m_switch_disconnect_txport
        )

    def add_refinement_method(self, task, method):
        print(method.__name__)
        setattr(self, method.__name__, method)
        m2 = getattr(self, method.__name__)
        print(m2.__code__.co_argcount)
        self.actor.add_new_method(task, getattr(self, method.__name__))
        

    #
    # Helper functions
    #

    def log(self, level, header, msg):
        """Print a log message, if enabled by self.actor's current verbosity level."""

        if self.actor.verbosity >= level:
            print(header + ': ' + msg)


    def log_err(self, msg):
        """Print an error message, if self.actor's current verbosity level is at least 1."""

        self.log(1, 'error', msg)


    def log_info(self, msg):
        """Print an info message, if self.actor's current verbosity level is at least 2."""

        self.log(2, 'info', msg)


    def log_trace(self, msg):
        """Print a trace message, if self.actor's current verbosity level is at least 3."""

        self.log(3, 'trace', msg)


    def is_component_type(self, component_id, comp_type):
        """Check whether given component is of the given type (e.g., ``CTRL`` or ``SWITCH``)."""

        # Component types should be defined in state
        if not hasattr(self.state, 'components'):
            return False
        if component_id not in self.state.components:
            return False
        if 'type' not in self.state.components[component_id]:
            return False

        # Check whether component type matches
        if self.state.components[component_id]['type'] == comp_type:
            return True
        else:
            return False


    def is_component_critical(self, component_id):
        """Check whether given component is critical."""

        # Component types should be defined in self.state
        if not hasattr(self.state, 'components'):
            return False
        if component_id not in self.state.components:
            return False
        if 'critical' not in self.state.components[component_id]:
            return False

        # Check whether component type matches
        return (self.state.components[component_id]['critical'] is True)


    def get_component_stat(self, component_id, stat_key):
        """Returns the :class:`dict` for the given statistic, or ``None`` if it doesn't exist."""

        if hasattr(self.state, 'stats') and component_id in self.state.stats:
            if stat_key in self.state.stats[component_id]:
                return self.state.stats[component_id][stat_key]
        return None


    def is_component_healthy(self, component_id):
        """Check whether the given component's health value is above the healthy threshold."""

        health_stat = self.get_component_stat(component_id, 'health')
        if health_stat is not None:
            health_val = health_stat['value']
            health_thresh_fn = health_stat['thresh_exceeded_fn']
            if not health_thresh_fn(health_val):
                return True
        return False


    #
    # Commands
    #

    def restart_vm(self, component_id, explain):
        """Restart a component virtual machine."""

        # Print human-friendly explanation
        self.log_info(explain)

        # Sense success vs. failure
        res = self.env.Sense('restart_vm')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "restart_vm"')
            return FAILURE

        # Restarting takes some time, but can fix some problems, so increase health
        # TODO: how to choose best new health value ???
        health_stat = self.get_component_stat(component_id, 'health')
        if health_stat is not None:
            cur_health = health_stat['value']
            new_health = min(1.0, (cur_health + 0.1) * 2)
            health_stat['value'] = new_health

        # CPU utilization should reset after restarting
        cpu_stat = self.get_component_stat(component_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cpu_stat['value'] = 0.0

        # Memory utilization should reset after restarting
        mem_stat = self.get_component_stat(component_id, 'mem_perc_ewma')
        if mem_stat is not None:
            mem_stat['value'] = 0.0

        # Host table size should reset after restarting
        hosttable_stat = self.get_component_stat(component_id, 'host_table_size')
        if hosttable_stat is not None:
            hosttable_stat['value'] = 0

        # Switch table size should reset after restarting
        switchtable_stat = self.get_component_stat(component_id, 'switch_table_size')
        if switchtable_stat is not None:
            switchtable_stat['value'] = 0

        # Flow table size should reset after restarting
        flowtable_stat = self.get_component_stat(component_id, 'flow_table_size')
        if flowtable_stat is not None:
            flowtable_stat['value'] = 0

        # Switch-to-ctrl connection status should reset after restarting
        isconn_stat = self.get_component_stat(component_id, 'is_conn_to_ctrl')
        if isconn_stat is not None:
            isconn_stat['value'] = True

        # Done
        return SUCCESS


    def add_vcpu(self, component_id, explain):
        """Add VCPU to component virtual machine, thus increasing component's VCPU count by one."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('add_vcpu')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "add_vcpu"')
            return FAILURE

        # CPU utilization should decrease
        cpu_stat = self.get_component_stat(component_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cpu_val = cpu_stat['value']
            cpu_stat['value'] = cpu_val / 2.0

        # Health should increase after increasing CPU
        # TODO: how to choose best new health value ???
        health_stat = self.get_component_stat(component_id, 'health')
        if health_stat is not None:
            cur_health = health_stat['value']
            new_health = min(1.0, cur_health + 0.1)
            health_stat['value'] = new_health
        return SUCCESS


    def increase_mem(self, component_id, explain):
        """Increase memory of component virtual machine."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('increase_mem')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "increase_mem"')
            return FAILURE

        # Memory utilization should decrease
        # TODO: how much memory was there in the first place?
        # TODO: how much do we expect the utilization percentage to decrease?
        mem_stat = self.get_component_stat(component_id, 'mem_perc_ewma')
        if mem_stat is not None:
            mem_val = mem_stat['value']
            mem_stat['value'] = mem_val / 2.0

        # Health should increase after increasing memory
        # TODO: how to choose best new health value ???
        health_stat = self.get_component_stat(component_id, 'health')
        if health_stat is not None:
            cur_health = health_stat['value']
            new_health = min(1.0, cur_health + 0.1)
            health_stat['value'] = new_health
        return SUCCESS


    def kill_top_proc(self, component_id, explain):
        """Kill top CPU-consuming process in a component virtual machine."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('kill_top_proc')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "kill_top_proc"')
            return FAILURE

        # CPU utilization should decrease if CPU-hungry process is stopped
        # TODO: how best to predict new CPU stat value ???
        cpu_stat = self.get_component_stat(component_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cur_cpu = cpu_stat['value']
            new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
            cpu_stat['value'] = new_cpu

        # Health should increase after CPU-hungry process is stopped
        # TODO: how to choose best new health value ???
        health_stat = self.get_component_stat(component_id, 'health')
        if health_stat is not None:
            cur_health = health_stat['value']
            new_health = min(1.0, (cur_health + 0.1) * 2)
            health_stat['value'] = new_health
        return SUCCESS


    def apply_update(self, component_id, software, explain):
        """Apply updates to the given software package in the component virtual machine."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('apply_update')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "apply_update"')
            return FAILURE

        # TODO: how to implement? does it have any measurable effect on the self.state?
        return SUCCESS


    def add_switch(self, component_id, explain):
        """Add a new switch to the SDN, copying connectivity/links of the given switch."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('add_switch')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "add_switch"')
            return FAILURE

        new_id = component_id + '-new'
        self.state.components[new_id] = self.state.components[component_id]
        self.state.components[new_id]['id'] = new_id

        self.state.stats[new_id] = self.state.stats[component_id]

        # Reset health
        health_stat =  self.get_component_stat(new_id, 'health')
        if health_stat is not None:
            health_stat['value'] = 1.0

        # Reset CPU utilization
        cpu_stat =  self.get_component_stat(new_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cpu_stat['value'] = 0.0

        # Reset memory utilization
        mem_stat =  self.get_component_stat(new_id, 'mem_perc_ewma')
        if mem_stat is not None:
            mem_stat['value'] = 0.0

        # Reset flow table size
        flowtable_stat = self.get_component_stat(new_id, 'flow_table_size')
        if flowtable_stat is not None:
            flowtable_stat['value'] = 0

        return SUCCESS


    def move_critical_hosts(self, old_switch_id, new_switch_id, explain):
        """Move critical hosts from one switch to another."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('move_critical_hosts')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "move_critical_hosts"')
            return FAILURE

        # TODO: how to implement? does it have any measurable effect on the self.state?
        # TODO: are hosts a part of the self.state?
        return SUCCESS


    def clear_ctrl_state_besteffort(self, component_id, explain):
        """Clear the SDN controller state (including host/switch tables), if possible."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('clear_ctrl_state_besteffort')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "clear_ctrl_state_besteffort"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'host_table_size')
        if stat is not None:
            stat['value'] = 0
        stat = self.get_component_stat(component_id, 'switch_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def clear_ctrl_state_fallback(self, component_id, explain):
        """Clear the SDN controller state (including host/switch tables) in a more robust way."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('clear_ctrl_state_fallback')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "clear_ctrl_state_fallback"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'host_table_size')
        if stat is not None:
            stat['value'] = 0
        stat = self.get_component_stat(component_id, 'switch_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def reinstall_ctrl_besteffort(self, component_id, explain):
        """Reinstall the SDN controller software, if possible."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('reinstall_ctrl_besteffort')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "reinstall_ctrl_besteffort"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'host_table_size')
        if stat is not None:
            stat['value'] = 0
        stat = self.get_component_stat(component_id, 'switch_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def reinstall_ctrl_fallback(self, component_id, explain):
        """Reinstall the SDN controller software in a more robust way."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('reinstall_ctrl_fallback')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "reinstall_ctrl_fallback"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'host_table_size')
        if stat is not None:
            stat['value'] = 0
        stat = self.get_component_stat(component_id, 'switch_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def reconnect_switch_to_ctrl(self, component_id, explain):
        """Reconnect a switch to its ctrl."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('reconnect_switch_to_ctrl')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "reconnect_switch_to_ctrl"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'is_conn_to_ctrl')
        if stat is not None:
            stat['value'] = True
        return SUCCESS


    def clear_switch_state_besteffort(self, component_id, explain):
        """Clear the switch state (including flow table), if possible."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('clear_switch_state_besteffort')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "clear_switch_state_besteffort"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'flow_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def clear_switch_state_fallback(self, component_id, explain):
        """Clear the switch state (including flow table) in a more robust way."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('clear_switch_state_fallback')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "clear_switch_state_fallback"')
            return FAILURE

        stat = self.get_component_stat(component_id, 'flow_table_size')
        if stat is not None:
            stat['value'] = 0
        return SUCCESS


    def disconnect_reconnect_switch_port(self, component_id, explain):
        """Disconnect and then reconnect switch port with most transmitted traffic."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('disconnect_reconnect_switch_port')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "disconnect_reconnect_switch_port"')
            return FAILURE

        cpu_stat = self.get_component_stat(component_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cur_cpu = cpu_stat['value']
            new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
            cpu_stat['value'] = new_cpu
        return SUCCESS


    def disconnect_switch_port(self, component_id, explain):
        """Disconnect switch port with most transmitted traffic."""

        # Print human-friendly explanation
        self.log_info(explain)

        # self.env.Sense success vs. failure
        res = self.env.Sense('disconnect_switch_port')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "disconnect_switch_port"')
            return FAILURE

        cpu_stat = self.get_component_stat(component_id, 'cpu_perc_ewma')
        if cpu_stat is not None:
            cur_cpu = cpu_stat['value']
            new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
            cpu_stat['value'] = new_cpu
        return SUCCESS


    def succeed(self, ):
        """Simply return success (always succeeds)."""

        # No need to self.env.Sense()

        return SUCCESS


    def unsure(self, ):
        """Add some cost within refinement method."""

        # self.env.Sense success vs. failure
        res = self.env.Sense('unsure')
        if res == FAILURE:
            self.log_err('self.env.Sense() returned FAILURE for "unsure"')
            return FAILURE

        return SUCCESS


    def fail(self, ):
        """Simply return failure (always fails)."""

        # No need to self.env.Sense()

        return FAILURE
    #
    # Methods
    #

    def m_fix_sdn(self, config, context):
        """Method to fix all symptoms in the SDN by checking each component.

        Checks the health of each component. For any component with health below the critical threshold,
        delegates to ``fix_component``.
        """

        if not isinstance(config, dict) or 'health_critical_thresh' not in config:
            self.log_err('could not find "health_critical_thresh" in config')
            self.actor.do_command(self.fail)
        else:
            self.log_info('will check health for ' + str(len(self.state.components.keys())) + ' components')
            for component_id in self.state.components:
                if component_id not in self.state.stats or 'health' not in self.state.stats[component_id]:
                    self.log_err('could not find "health" in self.state.stats["' + component_id + '"]')
                    self.actor.do_command(self.fail)
                else:
                    health_obj = self.state.stats[component_id]['health']
                    if 'value' not in health_obj or 'thresh_exceeded_fn' not in health_obj:
                        self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                                + component_id + '"]["health"]')
                        self.actor.do_command(self.fail)
                    else:
                        # Check for low health
                        value = health_obj['value']
                        thresh_exceeded_fn = health_obj['thresh_exceeded_fn']
                        if thresh_exceeded_fn(value):
                            self.log_info('threshold exceeded for stat "health": ' + component_id)
                            self.log_info('adding new task "fix_component" for "' + component_id + '"')
                            self.actor.do_task('fix_component', component_id, config, context)

                            # Check new health
                            if not self.is_component_healthy(component_id):
                                self.log_err('failed to restore component health: ' + component_id)
                                self.actor.do_command(self.fail)


    def m_handle_event(self, event, config, context):
        """Method to handle a specific anomaly/event."""

        # Handle event types based on their source
        if 'source' not in event:
            self.log_err('could not find "source" in event')
            self.actor.do_command(self.fail)
        else:
            if event['source'] == 'sysmon':
                # SysMon detects events related to high resource consumption
                low_resource_components = []

                # Add component that triggered this event
                component_id = event['component_id']
                low_resource_components.append(component_id)

                # Check stats of all other components
                # for component in self.state.components:
                #     if component not in low_resource_components:

                #         # Check each monitored stat
                #         if component not in self.state.stats:
                #             log_err('could not find "' + component + '" in self.state.stats')
                #             #self.actor.do_command(self.fail)
                #         else:
                #             for stat in self.state.stats[component]:
                #                 stat_obj = self.state.stats[component][stat]
                #                 value = stat_obj['value']
                #                 thresh_exceeded_fn = stat_obj['thresh_exceeded_fn']
                #                 if thresh_exceeded_fn(value):
                #                     log_trace('stat "' + stat + '" for component "' + component
                #                               + '" is exceeded')
                #                     low_resource_components.append(component)
                #                     break

                # Address symptoms of each affected component
                for component in low_resource_components:
                    self.log_info('adding new task "fix_component" for "' + component + '"')
                    cur_ctx = context + " and " + component + " has low resources"
                    self.actor.do_task('fix_component', component, config, cur_ctx)

                # Check whether affected component is now healthy
                if not self.is_component_healthy(component_id):
                    self.log_err('failed to restore component health: ' + component_id)
                    self.actor.do_command(self.fail)

            # Unhandled event source
            else:
                self.log_err('unhandled event source "' + event['source'] + '"')
                self.actor.do_command(self.fail)


    def m_fix_vm(self, component_id, config, context):
        """Method to fix symptoms at the virtual machine level."""

        do_fix_low_resources = False
        for stat_key in ['cpu_perc_ewma', 'mem_perc_ewma']:
            stat_obj = self.get_component_stat(component_id, stat_key)
            if stat_obj is not None:
                cur_val = stat_obj['value']
                thresh_exceeded_fn = stat_obj['thresh_exceeded_fn']
                if thresh_exceeded_fn(cur_val):
                    do_fix_low_resources = True
                    break
        if do_fix_low_resources is True:
            self.actor.do_task('fix_low_resources', component_id, config, context)
        else:
            explain = context + ", so restart the component VM"
            self.actor.do_command(self.restart_vm, component_id, explain)


    # def m_fix_software(self, component_id, config, context):
    #     """Method to fix symptoms at the software/process level."""

    #     do_fix_generic = False
    #     do_fix_sdnctrl = False
    #     do_fix_switch = False
    #     if self.is_component_type(component_id, 'CTRL'):
    #         do_fix_sdnctrl = True
    #     elif self.is_component_type(component_id, 'SWITCH'):
    #         do_fix_switch = True
    #     else:
    #         do_fix_generic = True

    #     if do_fix_generic is True:
    #         self.actor.do_task('try_generic_fix', component_id, config, context)
    #     elif do_fix_sdnctrl is True:
    #         self.actor.do_task('fix_sdn_controller', component_id, config, context)
    #     elif do_fix_switch is True:
    #         self.actor.do_task('fix_switch', component_id, config, context)
    #     else:
    #         self.actor.do_command(self.fail)


    def m_software_update(self, component_id, config, context):
        """Method to apply updates to a software package."""

        explain = context + ", so apply latest software updates within component VM"
        self.actor.do_command(self.apply_update, component_id, explain)


    def m_software_reinstall(self, component_id, config, context):
        """Method to reinstall a software package."""

        if self.is_component_type(component_id, 'CTRL'):
            explain = context + ", so reinstall SDN controller software within component VM"
            self.actor.do_command(self.reinstall_ctrl_besteffort, component_id, explain)
        else:
            self.actor.do_command(self.fail)


    def m_ctrl_mitigate_pktinflood(self, component_id, config, context):
        """Method to mitigate an SDN PACKET_IN flooding attack on a controller."""

        if not self.is_component_type(component_id, 'CTRL'):
            log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)

        # Detect which switches are the source of attack
        for switch_id in self.state.components:
            if self.is_component_type(switch_id, 'SWITCH') and not self.is_component_healthy(switch_id):

                cur_ctx = context + " and " + switch_id + " also needs to be fixed"

                # Move critical hosts away from unhealthy switch
                if self.is_component_critical(switch_id):

                    # Add new switch
                    explain_addswitch = cur_ctx + ", so add a new switch"
                    self.actor.do_command(self.add_switch, switch_id, explain_addswitch)

                    # Move critical hosts from unhealthy switches
                    explain_mvhosts = cur_ctx + ", so add a new switch and move critical hosts to it"
                    self.actor.do_command(self.move_critical_hosts, switch_id, switch_id + '-new', explain_mvhosts)

                # Fix unhealthy switch
                self.actor.do_task('fix_switch', switch_id, config, cur_ctx)

        # Clear controller state
        explain = context + ", so clear SDN controller state"
        self.actor.do_command(self.clear_ctrl_state_besteffort, component_id, explain)

        # Check whether controller is now healthy
        if not self.is_component_healthy(component_id):
            self.log_err('failed to restore component health: ' + component_id)
            self.actor.do_command(self.fail)


    def m_fix_sdn_controller_fallback(self, component_id, config, context):
        """Method to fix symptoms for a controller."""

        if not self.is_component_type(component_id, 'CTRL'):
            self.log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)
        elif component_id not in self.state.stats:
            self.log_err('could not find "' + component_id + '" in self.state.stats')
            self.actor.do_command(self.fail)
        else:
            # Check stats and determine what needs to be fixed
            stat_obj = self.state.stats[component_id]
            do_shrink_hosttable = False
            do_shrink_switchtable = False
            do_alleviate_cpu = False
            do_restore_health = False
            if 'host_table_size' in stat_obj:
                # TODO: if missing from state, can be populated lazily (here), via a probing action ???
                if ('value' not in stat_obj['host_table_size']
                        or 'thresh_exceeded_fn' not in stat_obj['host_table_size']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["host_table_size"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for inflated host table
                    value = stat_obj['host_table_size']['value']
                    thresh_exceeded_fn = stat_obj['host_table_size']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "host_table_size"')
                        do_shrink_hosttable = True
            if 'switch_table_size' in stat_obj:
                # TODO: if missing from state, can be populated lazily (here), via a probing action ???
                if ('value' not in stat_obj['switch_table_size'] or stat_obj['switch_table_size']['value'] == None
                        or 'thresh_exceeded_fn' not in stat_obj['switch_table_size']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["switch_table_size"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for inflated switch table
                    value = stat_obj['switch_table_size']['value']
                    thresh_exceeded_fn = stat_obj['switch_table_size']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "switch_table_size"')
                        do_shrink_switchtable = True
            if 'cpu_perc_ewma' in stat_obj:
                if ('value' not in stat_obj['cpu_perc_ewma']
                        or 'thresh_exceeded_fn' not in stat_obj['cpu_perc_ewma']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["cpu_perc_ewma"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for elevated CPU stat
                    value = stat_obj['cpu_perc_ewma']['value']
                    thresh_exceeded_fn = stat_obj['cpu_perc_ewma']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "cpu_perc_ewma": ' + component_id)
                        do_alleviate_cpu = True
            if 'health' in stat_obj:
                if ('value' not in stat_obj['health']
                        or 'thresh_exceeded_fn' not in stat_obj['health']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["health"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for low health
                    value = stat_obj['health']['value']
                    thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "health": ' + component_id)
                        do_restore_health = True

            # TODO: consider history when choosing an action here ??? or maintain in env_AIRS.py ???
            if do_shrink_hosttable:
                # Fix problem with inflated host table
                self.log_info('adding new task "shrink_ctrl_hosttable" for "' + component_id + '"')
                self.actor.do_task('shrink_ctrl_hosttable', component_id, config, context)
            elif do_shrink_switchtable:
                # Fix problem with inflated switch table
                self.log_info('adding new task "shrink_ctrl_switchtable" for "' + component_id + '"')
                self.actor.do_task('shrink_ctrl_switchtable', component_id, config, context)
            elif do_alleviate_cpu:
                # Alleviate elevated CPU stat
                self.log_info('adding new task "alleviate_ctrl_cpu" for "' + component_id + '"')
                self.actor.do_task('alleviate_ctrl_cpu', component_id, config, context)
            elif do_restore_health:
                # Restore low health (often also fixes CPU over-utilization)
                self.log_info('adding new task "restore_ctrl_health" for "' + component_id + '"')
                self.actor.do_task('restore_ctrl_health', component_id, config, context)
            else:
                # No problem could be identified from stats
                self.log_info('no task to add for "' + component_id + '"')
                # TODO: probe further ???
                # For now, fail
                # TODO: OR... succeed, because nothing was found to be wrong ???
                # log_err('could not figure out how to fix controller "' + component_id + '"')
                # self.actor.do_command(self.fail)

            # TODO: loop and continue checking stats until symptoms are gone ???


    def m_fix_switch(self, component_id, config, context):
        """Method to fix symptoms for a switch."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        elif component_id not in self.state.stats:
            self.log_err('could not find "' + component_id + '" in self.state.stats')
            self.actor.do_command(self.fail)
        else:
            # Check stats and determine what needs to be fixed
            stat_obj = self.state.stats[component_id]
            do_reconnect_ctrl = False
            do_shrink_flowtable = False
            do_alleviate_cpu = False
            do_restore_health = False
            if 'is_conn_to_ctrl' in stat_obj:
                if ('value' not in stat_obj['is_conn_to_ctrl']
                        or 'thresh_exceeded_fn' not in stat_obj['is_conn_to_ctrl']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["is_conn_to_ctrl"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for disconnection
                    value = stat_obj['is_conn_to_ctrl']['value']
                    thresh_exceeded_fn = stat_obj['is_conn_to_ctrl']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "is_conn_to_ctrl"')
                        do_reconnect_ctrl = True
            if 'flow_table_size' in stat_obj:
                # TODO: if missing from state, can be populated lazily (here), via a probing action ???
                if ('value' not in stat_obj['flow_table_size']
                        or 'thresh_exceeded_fn' not in stat_obj['flow_table_size']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["flow_table_size"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for inflated flow table
                    value = stat_obj['flow_table_size']['value']
                    thresh_exceeded_fn = stat_obj['flow_table_size']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "flow_table_size"')
                        do_shrink_flowtable = True
            if 'cpu_perc_ewma' in stat_obj:
                if ('value' not in stat_obj['cpu_perc_ewma']
                        or 'thresh_exceeded_fn' not in stat_obj['cpu_perc_ewma']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["cpu_perc_ewma"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for elevated CPU stat
                    value = stat_obj['cpu_perc_ewma']['value']
                    thresh_exceeded_fn = stat_obj['cpu_perc_ewma']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "cpu_perc_ewma": ' + component_id)
                        do_alleviate_cpu = True
            if 'health' in stat_obj:
                if ('value' not in stat_obj['health']
                        or 'thresh_exceeded_fn' not in stat_obj['health']):
                    self.log_err('could not find "value" or "thresh_exceeded_fn" in self.state.stats["'
                            + component_id + '"]["health"]')
                    self.actor.do_command(self.fail)
                else:
                    # Check for low health
                    value = stat_obj['health']['value']
                    thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        self.log_info('threshold exceeded for stat "health"')
                        do_restore_health = True

            # TODO: consider history when choosing an action here ??? or maintain in env_AIRS.py ???
            if do_reconnect_ctrl:
                # Fix problem with disconnected ctrl
                self.log_info('adding new task "reconnect_ctrl" for "' + component_id + '"')
                self.actor.do_task('reconnect_ctrl', component_id, config, context)
            if do_shrink_flowtable:
                # Fix problem with inflated flow table
                self.log_info('adding new task "shrink_switch_flowtable" for "' + component_id + '"')
                self.actor.do_task('shrink_switch_flowtable', component_id, config, context)
            elif do_alleviate_cpu:
                # Alleviate elevated CPU stat
                self.log_info('adding new task "alleviate_switch_cpu" for "' + component_id + '"')
                self.actor.do_task('alleviate_switch_cpu', component_id, config, context)
            elif do_restore_health:
                # Restore low health (often also fixes CPU over-utilization)
                log_info('adding new task "restore_switch_health" for "' + component_id + '"')
                self.self.actor.do_task('restore_switch_health', component_id, config, context)
            else:
                # No problem could be identified from stats
                # TODO: probe further ???
                # For now, fail
                # TODO: OR... succeed, because nothing was found to be wrong ???
                self.log_err('could not figure out how to fix switch "' + component_id + '"')
                self.actor.do_command(self.fail)

            # TODO: loop and continue checking stats until symptoms are gone ???


    def m_add_vcpu(self, component_id, config, context):
        """Method to add a VCPU to a component virtual machine."""

        explain = context + ", so add an additional VCPU to the VM"
        # TODO: should this action be temporary ????
        self.actor.do_command(self.add_vcpu, component_id, explain)


    def m_increase_mem(self, component_id, config, context):
        """Method to increase memory in a component virtual machine."""

        explain = context + ", so increase the memory in the VM"
        # TODO: should this action be temporary ????
        self.actor.do_command(self.increase_mem, component_id, explain)


    def m_ctrl_clearstate_besteffort(self, component_id, config, context):
        """Method to clear controller state (best effort)."""

        if not self.is_component_type(component_id, 'CTRL'):
            self.log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so clear SDN controller state"
            self.actor.do_command(self.clear_ctrl_state_besteffort, component_id, explain)


    def m_ctrl_clearstate_fallback(self, component_id, config, context):
        """Method to clear controller state (fallback)."""

        if not self.is_component_type(component_id, 'CTRL'):
            self.log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so clear SDN controller state using a fallback method"
            self.actor.do_command(self.clear_ctrl_state_fallback, component_id, explain)


    def m_ctrl_reinstall_besteffort(self, component_id, config, context):
        """Method to reinstall controller software (best effort)."""

        if not self.is_component_type(component_id, 'CTRL'):
            self.log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so reinstall SDN controller software within component VM"
            self.actor.do_command(self.reinstall_ctrl_besteffort, component_id, explain)


    def m_ctrl_reinstall_fallback(self, component_id, config, context):
        """Method to reinstall controller software (fallback)."""

        if not self.is_component_type(component_id, 'CTRL'):
            self.log_err('component "' + component_id + '" is not a controller')
            self.actor.do_command(self.fail)
        else:
            explain = (context + ", so reinstall SDN controller software within component VM " +
                       "using a fallback method")
            self.actor.do_command(self.reinstall_ctrl_fallback, component_id, explain)


    def m_component_restartvm(self, component_id, config, context):
        """Method to restart the virtual machine of a component."""

        explain = context + ", so restart the component VM"
        self.actor.do_command(self.restart_vm, component_id, explain)


    def m_component_kill_top_proc(self, component_id, config, context):
        """Method to kill the top CPU-consuming process in a component virtual machine."""

        explain = context + ", so kill the process that is consuming the most CPU in the VM"
        self.actor.do_command(self.kill_top_proc, component_id, explain)


    def m_switch_reconnect_ctrl(self, component_id, config, context):
        """Method to reconnect switch to its ctrl."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so reconnect switch to its ctrl"
            self.actor.do_command(self.reconnect_switch_to_ctrl, component_id, explain)


    def m_switch_clearstate_besteffort(self, component_id, config, context):
        """Method to clear switch state (best effort)."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so clear switch state"
            self.actor.do_command(self.clear_switch_state_besteffort, component_id, explain)


    def m_switch_clearstate_fallback(self, component_id, config, context):
        """Method to clear switch state (fallback)."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so clear switch state using a fallback method"
            self.actor.do_command(self.clear_switch_state_fallback, component_id, explain)


    def m_switch_discon_recon_txport(self, component_id, config, context):
        """Method to disconnect and then reconnect switch port with most transmitted traffic."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so temporarily disconnect the port with the most transmitted traffic"
            self.actor.do_command(self.disconnect_reconnect_switch_port, component_id, explain)


    def m_switch_disconnect_txport(self, component_id, config, context):
        """Method to disconnect switch port with most transmitted traffic."""

        if not self.is_component_type(component_id, 'SWITCH'):
            self.log_err('component "' + component_id + '" is not a switch')
            self.actor.do_command(self.fail)
        else:
            explain = context + ", so disconnect the port with the most transmitted traffic"
            self.actor.do_command(self.disconnect_switch_port, component_id, explain)



DURATION.TIME = {
    'restart_vm': 60,
    'add_vcpu': 5,
    'increase_mem': 5,
    'kill_top_proc': 5,
    'apply_update': 60,
    'add_switch': 30,
    'move_critical_hosts': 15,
    'clear_ctrl_state_besteffort': 10,
    'clear_ctrl_state_fallback': 20,
    'reinstall_ctrl_besteffort': 30,
    'reinstall_ctrl_fallback': 60,
    'reconnect_switch_to_ctrl': 10,
    'clear_switch_state_besteffort': 10,
    'clear_switch_state_fallback': 20,
    'disconnect_reconnect_switch_port': 5,
    'disconnect_switch_port': 10,
    'succeed': 1,
    'unsure': 5,
    'fail': 1
}

DURATION.COUNTER = {
    'restart_vm': 60,
    'add_vcpu': 5,
    'increase_mem': 5,
    'kill_top_proc': 5,
    'apply_update': 60,
    'add_switch': 30,
    'move_critical_hosts': 15,
    'clear_ctrl_state_besteffort': 10,
    'clear_ctrl_state_fallback': 20,
    'reinstall_ctrl_besteffort': 30,
    'reinstall_ctrl_fallback': 60,
    'reconnect_switch_to_ctrl': 10,
    'clear_switch_state_besteffort': 10,
    'clear_switch_state_fallback': 20,
    'disconnect_reconnect_switch_port': 5,
    'disconnect_switch_port': 10,
    'succeed': 1,
    'unsure': 5,
    'fail': 1
}



class AIRSEnv():
    def __init__(self, state, rv):
        # Each command is associated with a tuple indicating probability of success vs. failure
        self.commandProb = {
            'restart_vm': (0.95, 0.05),
            'add_vcpu': (0.95, 0.05),
            'increase_mem': (0.95, 0.05),
            'kill_top_proc': (0.95, 0.05),
            'apply_update': (0.6, 0.4),
            'add_switch': (0.75, 0.25),
            'move_critical_hosts': (0.6, 0.4),
            'clear_ctrl_state_besteffort': (0.6, 0.4),
            'clear_ctrl_state_fallback': (0.8, 0.2),
            'reinstall_ctrl_besteffort': (0.75, 0.25),
            'reinstall_ctrl_fallback': (0.9, 0.1),
            'reconnect_switch_to_ctrl': (0.8, 0.2),
            'clear_switch_state_besteffort': (0.8, 0.2),
            'clear_switch_state_fallback': (0.9, 0.1),
            'disconnect_reconnect_switch_port': (0.75, 0.25),
            'disconnect_switch_port': (0.9, 0.1),
            'succeed': (1, 0),
            'unsure': (0.5, 0.5),
            'fail': (0, 1)
        }
        self.state = state
        self.rv = rv


    def Sense(self, cmd):
        """Return ``SUCCESS`` or ``FAILURE`` based on random choice according to ``commandProb``."""

        p = self.commandProb[cmd]
        outcome = np.random.choice(len(p), 50, p=p)
        res = outcome[0]
        if res == 0:
            return SUCCESS
        else:
            return FAILURE


