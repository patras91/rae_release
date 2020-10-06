#!/usr/bin/env python3
"""Domain definition for AIRS SDN to work with RAE.

This file defines the tasks, methods, and commands for the AIRS SDN domain.
"""
__author__ = 'alex'

from env_AIRS import Sense
from domain_constants import SUCCESS, FAILURE
from state import state
from timer import DURATION
import RAE1_and_RAEplan as rae


#
# Helper functions
#

def log(level, header, msg):
    """Print a log message, if enabled by RAE's current verbosity level."""

    if rae.verbose >= level:
        print(header + ': ' + msg)


def log_err(msg):
    """Print an error message, if RAE's current verbosity level is at least 1."""

    log(1, 'error', msg)


def log_info(msg):
    """Print an info message, if RAE's current verbosity level is at least 2."""

    log(2, 'info', msg)


def log_trace(msg):
    """Print a trace message, if RAE's current verbosity level is at least 3."""

    log(3, 'trace', msg)


def is_component_type(component_id, comp_type):
    """Check whether given component is of the given type (e.g., ``CTRL`` or ``SWITCH``)."""

    # Component types should be defined in state
    if not hasattr(state, 'components'):
        return False
    if component_id not in state.components:
        return False
    if 'type' not in state.components[component_id]:
        return False

    # Check whether component type matches
    if state.components[component_id]['type'] == comp_type:
        return True
    else:
        return False


def is_component_critical(component_id):
    """Check whether given component is critical."""

    # Component types should be defined in state
    if not hasattr(state, 'components'):
        return False
    if component_id not in state.components:
        return False
    if 'critical' not in state.components[component_id]:
        return False

    # Check whether component type matches
    return (state.components[component_id]['critical'] is True)


def get_component_stat(component_id, stat_key):
    """Returns the :class:`dict` for the given statistic, or ``None`` if it doesn't exist."""

    if hasattr(state, 'stats') and component_id in state.stats:
        if stat_key in state.stats[component_id]:
            return state.stats[component_id][stat_key]
    return None


def is_component_healthy(component_id):
    """Check whether the given component's health value is above the healthy threshold."""

    health_stat = get_component_stat(component_id, 'health')
    if health_stat is not None:
        health_val = health_stat['value']
        health_thresh_fn = health_stat['thresh_exceeded_fn']
        if not health_thresh_fn(health_val):
            return True
    return False


#
# Commands
#

def restart_vm(component_id, explain):
    """Restart a component virtual machine."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('restart_vm')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "restart_vm"')
        return FAILURE

    # Restarting takes some time, but can fix some problems, so increase health
    # TODO: how to choose best new health value ???
    health_stat = get_component_stat(component_id, 'health')
    if health_stat is not None:
        cur_health = health_stat['value']
        new_health = min(1.0, (cur_health + 0.1) * 2)
        health_stat['value'] = new_health

    # CPU utilization should reset after restarting
    cpu_stat = get_component_stat(component_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cpu_stat['value'] = 0.0

    # Memory utilization should reset after restarting
    mem_stat = get_component_stat(component_id, 'mem_perc_ewma')
    if mem_stat is not None:
        mem_stat['value'] = 0.0

    # Host table size should reset after restarting
    hosttable_stat = get_component_stat(component_id, 'host_table_size')
    if hosttable_stat is not None:
        hosttable_stat['value'] = 0

    # Flow table size should reset after restarting
    flowtable_stat = get_component_stat(component_id, 'flow_table_size')
    if flowtable_stat is not None:
        flowtable_stat['value'] = 0

    # Done
    return SUCCESS


def add_vcpu(component_id, explain):
    """Add VCPU to component virtual machine, thus increasing component's VCPU count by one."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('add_vcpu')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "add_vcpu"')
        return FAILURE

    # CPU utilization should decrease
    cpu_stat = get_component_stat(component_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cpu_val = cpu_stat['value']
        cpu_stat['value'] = cpu_val / 2.0

    # Health should increase after increasing CPU
    # TODO: how to choose best new health value ???
    health_stat = get_component_stat(component_id, 'health')
    if health_stat is not None:
        cur_health = health_stat['value']
        new_health = min(1.0, cur_health + 0.1)
        health_stat['value'] = new_health
    return SUCCESS


def increase_mem(component_id, explain):
    """Increase memory of component virtual machine."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('increase_mem')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "increase_mem"')
        return FAILURE

    # Memory utilization should decrease
    # TODO: how much memory was there in the first place?
    # TODO: how much do we expect the utilization percentage to decrease?
    mem_stat = get_component_stat(component_id, 'mem_perc_ewma')
    if mem_stat is not None:
        mem_val = mem_stat['value']
        mem_stat['value'] = mem_val / 2.0

    # Health should increase after increasing memory
    # TODO: how to choose best new health value ???
    health_stat = get_component_stat(component_id, 'health')
    if health_stat is not None:
        cur_health = health_stat['value']
        new_health = min(1.0, cur_health + 0.1)
        health_stat['value'] = new_health
    return SUCCESS


def kill_top_proc(component_id, explain):
    """Kill top CPU-consuming process in a component virtual machine."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('kill_top_proc')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "kill_top_proc"')
        return FAILURE

    # CPU utilization should decrease if CPU-hungry process is stopped
    # TODO: how best to predict new CPU stat value ???
    cpu_stat = get_component_stat(component_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cur_cpu = cpu_stat['value']
        new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
        cpu_stat['value'] = new_cpu

    # Health should increase after CPU-hungry process is stopped
    # TODO: how to choose best new health value ???
    health_stat = get_component_stat(component_id, 'health')
    if health_stat is not None:
        cur_health = health_stat['value']
        new_health = min(1.0, (cur_health + 0.1) * 2)
        health_stat['value'] = new_health
    return SUCCESS


def apply_update(component_id, software, explain):
    """Apply updates to the given software package in the component virtual machine."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('apply_update')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "apply_update"')
        return FAILURE

    # TODO: how to implement? does it have any measurable effect on the state?
    return SUCCESS


def add_switch(component_id, explain):
    """Add a new switch to the SDN, copying connectivity/links of the given switch."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('add_switch')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "add_switch"')
        return FAILURE

    new_id = component_id + '-new'
    state.components[new_id] = state.components[component_id]
    state.components[new_id]['id'] = new_id

    state.stats[new_id] = state.stats[component_id]

    # Reset health
    health_stat = get_component_stat(new_id, 'health')
    if health_stat is not None:
        health_stat['value'] = 1.0

    # Reset CPU utilization
    cpu_stat = get_component_stat(new_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cpu_stat['value'] = 0.0

    # Reset memory utilization
    mem_stat = get_component_stat(new_id, 'mem_perc_ewma')
    if mem_stat is not None:
        mem_stat['value'] = 0.0

    # Reset flow table size
    flowtable_stat = get_component_stat(new_id, 'flow_table_size')
    if flowtable_stat is not None:
        flowtable_stat['value'] = 0

    return SUCCESS


def move_critical_hosts(old_switch_id, new_switch_id, explain):
    """Move critical hosts from one switch to another."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('move_critical_hosts')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "move_critical_hosts"')
        return FAILURE

    # TODO: how to implement? does it have any measurable effect on the state?
    # TODO: are hosts a part of the state?
    return SUCCESS


def clear_ctrl_state_besteffort(component_id, explain):
    """Clear the SDN controller state (including host table), if possible."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('clear_ctrl_state_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_ctrl_state_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_ctrl_state_fallback(component_id, explain):
    """Clear the SDN controller state (including host table) in a more robust way."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('clear_ctrl_state_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_ctrl_state_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_besteffort(component_id, explain):
    """Reinstall the SDN controller software, if possible."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('reinstall_ctrl_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "reinstall_ctrl_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_fallback(component_id, explain):
    """Reinstall the SDN controller software in a more robust way."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('reinstall_ctrl_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "reinstall_ctrl_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_besteffort(component_id, explain):
    """Clear the switch state (including flow table), if possible."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('clear_switch_state_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_switch_state_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_fallback(component_id, explain):
    """Clear the switch state (including flow table) in a more robust way."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('clear_switch_state_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_switch_state_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def disconnect_reconnect_switch_port(component_id, explain):
    """Disconnect and then reconnect switch port with most transmitted traffic."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('disconnect_reconnect_switch_port')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "disconnect_reconnect_switch_port"')
        return FAILURE

    cpu_stat = get_component_stat(component_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cur_cpu = cpu_stat['value']
        new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
        cpu_stat['value'] = new_cpu
    return SUCCESS


def disconnect_switch_port(component_id, explain):
    """Disconnect switch port with most transmitted traffic."""

    # Print human-friendly explanation
    log_info(explain)

    # Sense success vs. failure
    res = Sense('disconnect_switch_port')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "disconnect_switch_port"')
        return FAILURE

    cpu_stat = get_component_stat(component_id, 'cpu_perc_ewma')
    if cpu_stat is not None:
        cur_cpu = cpu_stat['value']
        new_cpu = max(0.0, (cur_cpu - 50.0) / 2)
        cpu_stat['value'] = new_cpu
    return SUCCESS


def succeed():
    """Simply return success (always succeeds)."""

    # No need to Sense()

    return SUCCESS


def unsure():
    """Add some cost within refinement method."""

    # Sense success vs. failure
    res = Sense('unsure')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "unsure"')
        return FAILURE

    return SUCCESS


def fail():
    """Simply return failure (always fails)."""

    # No need to Sense()

    return FAILURE


# Declare commands in RAE engine
rae.declare_commands([
    restart_vm,
    add_vcpu,
    increase_mem,
    kill_top_proc,
    apply_update,
    add_switch,
    move_critical_hosts,
    clear_ctrl_state_besteffort,
    clear_ctrl_state_fallback,
    reinstall_ctrl_besteffort,
    reinstall_ctrl_fallback,
    clear_switch_state_besteffort,
    clear_switch_state_fallback,
    disconnect_reconnect_switch_port,
    disconnect_switch_port,
    succeed,
    unsure,
    fail
])

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
    'clear_switch_state_besteffort': 10,
    'clear_switch_state_fallback': 20,
    'disconnect_reconnect_switch_port': 5,
    'disconnect_switch_port': 10,
    'succeed': 1,
    'unsure': 5,
    'fail': 1
}


#
# Methods
#

def m_fix_sdn(config, context):
    """Method to fix all symptoms in the SDN by checking each component.

    Checks the health of each component. For any component with health below the critical threshold,
    delegates to ``fix_component``.
    """

    if not isinstance(config, dict) or 'health_critical_thresh' not in config:
        log_err('could not find "health_critical_thresh" in config')
        rae.do_command(fail)
    else:
        log_info('will check health for ' + str(len(state.components.keys())) + ' components')
        for component_id in state.components:
            if component_id not in state.stats or 'health' not in state.stats[component_id]:
                log_err('could not find "health" in state.stats["' + component_id + '"]')
                rae.do_command(fail)
            else:
                health_obj = state.stats[component_id]['health']
                if 'value' not in health_obj or 'thresh_exceeded_fn' not in health_obj:
                    log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                            + component_id + '"]["health"]')
                    rae.do_command(fail)
                else:
                    # Check for low health
                    value = health_obj['value']
                    thresh_exceeded_fn = health_obj['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        log_info('threshold exceeded for stat "health": ' + component_id)
                        log_info('adding new task "fix_component" for "' + component_id + '"')
                        rae.do_task('fix_component', component_id, config, context)

                        # Check new health
                        if not is_component_healthy(component_id):
                            log_err('failed to restore component health: ' + component_id)
                            rae.do_task(fail)


def m_handle_event(event, config, context):
    """Method to handle a specific anomaly/event."""

    # Handle event types based on their source
    if 'source' not in event:
        log_err('could not find "source" in event')
        rae.do_command(fail)
    else:
        if event['source'] == 'sysmon':
            # SysMon detects events related to high resource consumption
            low_resource_components = []

            # Add component that triggered this event
            component_id = event['component_id']
            low_resource_components.append(component_id)

            # Check stats of all other components
            # for component in state.components:
            #     if component not in low_resource_components:

            #         # Check each monitored stat
            #         if component not in state.stats:
            #             log_err('could not find "' + component + '" in state.stats')
            #             #rae.do_command(fail)
            #         else:
            #             for stat in state.stats[component]:
            #                 stat_obj = state.stats[component][stat]
            #                 value = stat_obj['value']
            #                 thresh_exceeded_fn = stat_obj['thresh_exceeded_fn']
            #                 if thresh_exceeded_fn(value):
            #                     log_trace('stat "' + stat + '" for component "' + component
            #                               + '" is exceeded')
            #                     low_resource_components.append(component)
            #                     break

            # Address symptoms of each affected component
            for component in low_resource_components:
                log_info('adding new task "fix_component" for "' + component + '"')
                cur_ctx = context + " and " + component + " has low resources"
                rae.do_task('fix_component', component, config, cur_ctx)

            # Check whether affected component is now healthy
            if not is_component_healthy(component_id):
                log_err('failed to restore component health: ' + component_id)
                rae.do_task(fail)

        # Unhandled event source
        else:
            log_err('unhandled event source "' + event['source'] + '"')
            rae.do_command(fail)


def m_fix_vm(component_id, config, context):
    """Method to fix symptoms at the virtual machine level."""

    do_fix_low_resources = False
    for stat_key in ['cpu_perc_ewma', 'mem_perc_ewma']:
        stat_obj = get_component_stat(component_id, stat_key)
        if stat_obj is not None:
            cur_val = stat_obj['value']
            thresh_exceeded_fn = stat_obj['thresh_exceeded_fn']
            if thresh_exceeded_fn(cur_val):
                do_fix_low_resources = True
                break
    if do_fix_low_resources is True:
        rae.do_task('fix_low_resources', component_id, config, context)
    else:
        explain = context + ", so restart the component VM"
        rae.do_command(restart_vm, component_id, explain)


def m_fix_software(component_id, config, context):
    """Method to fix symptoms at the software/process level."""

    do_fix_generic = False
    do_fix_sdnctrl = False
    do_fix_switch = False
    if is_component_type(component_id, 'CTRL'):
        do_fix_sdnctrl = True
    elif is_component_type(component_id, 'SWITCH'):
        do_fix_switch = True
    else:
        do_fix_generic = True

    if do_fix_generic is True:
        rae.do_task('try_generic_fix', component_id, config, context)
    elif do_fix_sdnctrl is True:
        rae.do_task('fix_sdn_controller', component_id, config, context)
    elif do_fix_switch is True:
        rae.do_task('fix_switch', component_id, config, context)
    else:
        rae.do_command(fail)


def m_software_update(component_id, config, context):
    """Method to apply updates to a software package."""

    explain = context + ", so apply latest software updates within component VM"
    rae.do_command(apply_update, component_id, explain)


def m_software_reinstall(component_id, config, context):
    """Method to reinstall a software package."""

    if is_component_type(component_id, 'CTRL'):
        explain = context + ", so reinstall SDN controller software within component VM"
        rae.do_command(reinstall_ctrl_besteffort, component_id, explain)
    else:
        rae.do_command(fail)


def m_ctrl_mitigate_pktinflood(component_id, config, context):
    """Method to mitigate an SDN PACKET_IN flooding attack on a controller."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)

    # Detect which switches are the source of attack
    for switch_id in state.components:
        if is_component_type(switch_id, 'SWITCH') and not is_component_healthy(switch_id):

            cur_ctx = context + " and " + switch_id + " also needs to be fixed"

            # Move critical hosts away from unhealthy switch
            if is_component_critical(switch_id):

                # Add new switch
                explain_addswitch = cur_ctx + ", so add a new switch"
                rae.do_command(add_switch, switch_id, explain_addswitch)

                # Move critical hosts from unhealthy switches
                explain_mvhosts = cur_ctx + ", so add a new switch and move critical hosts to it"
                rae.do_command(move_critical_hosts, switch_id, switch_id + '-new', explain_mvhosts)

            # Fix unhealthy switch
            rae.do_task('fix_switch', switch_id, cur_ctx)

    # Clear controller state
    explain = context + ", so clear SDN controller state"
    rae.do_command(clear_ctrl_state_besteffort, component_id, explain)

    # Check whether controller is now healthy
    if not is_component_healthy(component_id):
        log_err('failed to restore component health: ' + component_id)
        rae.do_task(fail)


def m_fix_sdn_controller_fallback(component_id, config, context):
    """Method to fix symptoms for a controller."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    elif component_id not in state.stats:
        log_err('could not find "' + component_id + '" in state.stats')
        rae.do_command(fail)
    else:
        # Check stats and determine what needs to be fixed
        stat_obj = state.stats[component_id]
        do_shrink_hosttable = False
        do_alleviate_cpu = False
        do_restore_health = False
        if 'host_table_size' in stat_obj:
            # TODO: if missing from state, can be populated lazily (here), via a probing action ???
            if ('value' not in stat_obj['host_table_size']
                    or 'thresh_exceeded_fn' not in stat_obj['host_table_size']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["host_table_size"]')
                rae.do_command(fail)
            else:
                # Check for inflated host table
                value = stat_obj['host_table_size']['value']
                thresh_exceeded_fn = stat_obj['host_table_size']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "host_table_size"')
                    do_shrink_hosttable = True
        if 'cpu_perc_ewma' in stat_obj:
            if ('value' not in stat_obj['cpu_perc_ewma']
                    or 'thresh_exceeded_fn' not in stat_obj['cpu_perc_ewma']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["cpu_perc_ewma"]')
                rae.do_command(fail)
            else:
                # Check for elevated CPU stat
                value = stat_obj['cpu_perc_ewma']['value']
                thresh_exceeded_fn = stat_obj['cpu_perc_ewma']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "cpu_perc_ewma": ' + component_id)
                    do_alleviate_cpu = True
        if 'health' in stat_obj:
            if ('value' not in stat_obj['health']
                    or 'thresh_exceeded_fn' not in stat_obj['health']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["health"]')
                rae.do_command(fail)
            else:
                # Check for low health
                value = stat_obj['health']['value']
                thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "health": ' + component_id)
                    do_restore_health = True

        # TODO: consider history when choosing an action here ??? or maintain in env_AIRS.py ???
        if do_shrink_hosttable:
            # Fix problem with inflated host table
            log_info('adding new task "shrink_ctrl_hosttable" for "' + component_id + '"')
            rae.do_task('shrink_ctrl_hosttable', component_id, context)
        elif do_alleviate_cpu:
            # Alleviate elevated CPU stat
            log_info('adding new task "alleviate_ctrl_cpu" for "' + component_id + '"')
            rae.do_task('alleviate_ctrl_cpu', component_id, context)
        elif do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            log_info('adding new task "restore_ctrl_health" for "' + component_id + '"')
            rae.do_task('restore_ctrl_health', component_id, context)
        else:
            # No problem could be identified from stats
            log_info('no task to add for "' + component_id + '"')
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            # log_err('could not figure out how to fix controller "' + component_id + '"')
            # rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def m_fix_switch(component_id, config, context):
    """Method to fix symptoms for a switch."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    elif component_id not in state.stats:
        log_err('could not find "' + component_id + '" in state.stats')
        rae.do_command(fail)
    else:
        # Check stats and determine what needs to be fixed
        stat_obj = state.stats[component_id]
        do_shrink_flowtable = False
        do_alleviate_cpu = False
        do_restore_health = False
        if 'flow_table_size' in stat_obj:
            # TODO: if missing from state, can be populated lazily (here), via a probing action ???
            if ('value' not in stat_obj['flow_table_size']
                    or 'thresh_exceeded_fn' not in stat_obj['flow_table_size']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["flow_table_size"]')
                rae.do_command(fail)
            else:
                # Check for inflated flow table
                value = stat_obj['flow_table_size']['value']
                thresh_exceeded_fn = stat_obj['flow_table_size']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "flow_table_size"')
                    do_shrink_flowtable = True
        if 'cpu_perc_ewma' in stat_obj:
            if ('value' not in stat_obj['cpu_perc_ewma']
                    or 'thresh_exceeded_fn' not in stat_obj['cpu_perc_ewma']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["cpu_perc_ewma"]')
                rae.do_command(fail)
            else:
                # Check for elevated CPU stat
                value = stat_obj['cpu_perc_ewma']['value']
                thresh_exceeded_fn = stat_obj['cpu_perc_ewma']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "cpu_perc_ewma": ' + component_id)
                    do_alleviate_cpu = True
        if 'health' in stat_obj:
            if ('value' not in stat_obj['health']
                    or 'thresh_exceeded_fn' not in stat_obj['health']):
                log_err('could not find "value" or "thresh_exceeded_fn" in state.stats["'
                        + component_id + '"]["health"]')
                rae.do_command(fail)
            else:
                # Check for low health
                value = stat_obj['health']['value']
                thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    log_info('threshold exceeded for stat "health"')
                    do_restore_health = True

        # TODO: consider history when choosing an action here ??? or maintain in env_AIRS.py ???
        if do_shrink_flowtable:
            # Fix problem with inflated flow table
            log_info('adding new task "shrink_switch_flowtable" for "' + component_id + '"')
            rae.do_task('shrink_switch_flowtable', component_id, context)
        elif do_alleviate_cpu:
            # Alleviate elevated CPU stat
            log_info('adding new task "alleviate_switch_cpu" for "' + component_id + '"')
            rae.do_task('alleviate_switch_cpu', component_id, context)
        elif do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            log_info('adding new task "restore_switch_health" for "' + component_id + '"')
            rae.do_task('restore_switch_health', component_id, context)
        else:
            # No problem could be identified from stats
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            log_err('could not figure out how to fix switch "' + component_id + '"')
            rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def m_add_vcpu(component_id, context):
    """Method to add a VCPU to a component virtual machine."""

    explain = context + ", so add an additional VCPU to the VM"
    # TODO: should this action be temporary ????
    rae.do_command(add_vcpu, component_id, explain)


def m_increase_mem(component_id, context):
    """Method to increase memory in a component virtual machine."""

    explain = context + ", so increase the memory in the VM"
    # TODO: should this action be temporary ????
    rae.do_command(increase_mem, component_id, explain)


def m_ctrl_clearstate_besteffort(component_id, context):
    """Method to clear controller state (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        explain = context + ", so clear SDN controller state"
        rae.do_command(clear_ctrl_state_besteffort, component_id, explain)


def m_ctrl_clearstate_fallback(component_id, context):
    """Method to clear controller state (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        explain = context + ", so clear SDN controller state using a fallback method"
        rae.do_command(clear_ctrl_state_fallback, component_id, explain)


def m_ctrl_reinstall_besteffort(component_id, context):
    """Method to reinstall controller software (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        explain = context + ", so reinstall SDN controller software within component VM"
        rae.do_command(reinstall_ctrl_besteffort, component_id, explain)


def m_ctrl_reinstall_fallback(component_id, context):
    """Method to reinstall controller software (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        explain = (context + ", so reinstall SDN controller software within component VM " +
                   "using a fallback method")
        rae.do_command(reinstall_ctrl_fallback, component_id, explain)


def m_component_restartvm(component_id, context):
    """Method to restart the virtual machine of a component."""

    explain = context + ", so restart the component VM"
    rae.do_command(restart_vm, component_id, explain)


def m_component_kill_top_proc(component_id, context):
    """Method to kill the top CPU-consuming process in a component virtual machine."""

    explain = context + ", so kill the process that is consuming the most CPU in the VM"
    rae.do_command(kill_top_proc, component_id, explain)


def m_switch_clearstate_besteffort(component_id, context):
    """Method to clear switch state (best effort)."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        explain = context + ", so clear switch state"
        rae.do_command(clear_switch_state_besteffort, component_id, explain)


def m_switch_clearstate_fallback(component_id, context):
    """Method to clear switch state (fallback)."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        explain = context + ", so clear switch state using a fallback method"
        rae.do_command(clear_switch_state_fallback, component_id, explain)


def m_switch_discon_recon_txport(component_id, context):
    """Method to disconnect and then reconnect switch port with most transmitted traffic."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        explain = context + ", so temporarily disconnect the port with the most transmitted traffic"
        rae.do_command(disconnect_reconnect_switch_port, component_id, explain)


def m_switch_disconnect_txport(component_id, context):
    """Method to disconnect switch port with most transmitted traffic."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        explain = context + ", so disconnect the port with the most transmitted traffic"
        rae.do_command(disconnect_switch_port, component_id, explain)


#
# Task-to-method mappings
#

rae.declare_task('fix_sdn', 'config', 'context')
rae.declare_task('handle_event', 'event', 'config', 'context')

rae.declare_task('fix_component', 'component_id', 'config', 'context')

rae.declare_task('fix_low_resources', 'component_id', 'config', 'context')
rae.declare_task('try_generic_fix', 'component_id', 'config', 'context')
rae.declare_task('fix_sdn_controller', 'component_id', 'config', 'context')
rae.declare_task('fix_switch', 'component_id', 'config', 'context')

rae.declare_task('shrink_ctrl_hosttable', 'component_id', 'context')
rae.declare_task('alleviate_ctrl_cpu', 'component_id', 'context')
rae.declare_task('restore_ctrl_health', 'component_id', 'context')

rae.declare_task('shrink_switch_flowtable', 'component_id', 'context')
rae.declare_task('alleviate_switch_cpu', 'component_id', 'context')
rae.declare_task('restore_switch_health', 'component_id', 'context')

rae.declare_methods(
    'fix_sdn',
    m_fix_sdn
)

rae.declare_methods(
    'handle_event',
    m_handle_event
)

rae.declare_methods(
    'fix_component',
    m_fix_vm,
    m_fix_software
)
rae.declare_methods(
    'fix_low_resources',
    m_add_vcpu,
    m_increase_mem
)
rae.declare_methods(
    'try_generic_fix',
    m_software_update,
    m_software_reinstall
)
rae.declare_methods(
    'fix_sdn_controller',
    m_ctrl_clearstate_besteffort,
    m_ctrl_mitigate_pktinflood,
    m_fix_sdn_controller_fallback
)
rae.declare_methods(
    'fix_switch',
    m_fix_switch
)

rae.declare_methods(
    'shrink_ctrl_hosttable',
    m_ctrl_clearstate_besteffort,
    m_ctrl_clearstate_fallback,
    m_ctrl_reinstall_besteffort,
    m_ctrl_reinstall_fallback
)
rae.declare_methods(
    'alleviate_ctrl_cpu',
    m_component_kill_top_proc,
    m_ctrl_reinstall_besteffort,
    m_ctrl_reinstall_fallback,
    m_component_restartvm
)
rae.declare_methods(
    'restore_ctrl_health',
    m_ctrl_reinstall_besteffort,
    m_ctrl_reinstall_fallback,
    m_component_restartvm
)

rae.declare_methods(
    'shrink_switch_flowtable',
    m_switch_clearstate_besteffort,
    m_switch_clearstate_fallback
)
rae.declare_methods(
    'alleviate_switch_cpu',
    m_switch_discon_recon_txport,
    m_component_kill_top_proc,
    m_switch_clearstate_besteffort,
    m_switch_clearstate_fallback,
    m_switch_disconnect_txport
)
rae.declare_methods(
    'restore_switch_health',
    m_switch_discon_recon_txport,
    m_switch_clearstate_besteffort,
    m_switch_clearstate_fallback,
    m_switch_disconnect_txport
)
