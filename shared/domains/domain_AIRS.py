#!/usr/bin/env python3
"""Domain definition for AIRS SDN to work with RAE.

This file defines the tasks, methods, and commands for the AIRS SDN domain.
"""
__author__ = 'alex'

from env_AIRS import Sense
from domain_constants import SUCCESS, FAILURE
from state import state, rv
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


def get_component_stat(component_id, stat_key):
    """Returns the :class:`dict` for the given statistic, or ``None`` if it doesn't exist."""

    if hasattr(state, 'stats') and component_id in state.stats:
        if stat_key in state.stats[component_id]:
            return state.stats[component_id][stat_key]
    return None


#
# Commands
#

def restart_vm(component_id):
    """Restart a component virtual machine."""

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

    # Host table size should reset after restarting
    hosttable_stat = get_component_stat(component_id, 'host_table_size')
    if hosttable_stat is not None:
        hosttable_stat['value'] = 0

    # Done
    return SUCCESS


def kill_top_proc(component_id):
    """Kill top CPU-consuming process in a component virtual machine."""

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


def clear_ctrl_state_besteffort(component_id):
    """Clear the SDN controller state (including host table), if possible."""

    # Sense success vs. failure
    res = Sense('clear_ctrl_state_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_ctrl_state_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_ctrl_state_fallback(component_id):
    """Clear the SDN controller state (including host table) in a more robust way."""

    # Sense success vs. failure
    res = Sense('clear_ctrl_state_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_ctrl_state_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_besteffort(component_id):
    """Reinstall the SDN controller software, if possible."""

    # Sense success vs. failure
    res = Sense('reinstall_ctrl_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "reinstall_ctrl_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_fallback(component_id):
    """Reinstall the SDN controller software in a more robust way."""

    # Sense success vs. failure
    res = Sense('reinstall_ctrl_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "reinstall_ctrl_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_besteffort(component_id):
    """Clear the switch state (including flow table), if possible."""

    # Sense success vs. failure
    res = Sense('clear_switch_state_besteffort')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_switch_state_besteffort"')
        return FAILURE

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_fallback(component_id):
    """Clear the switch state (including flow table) in a more robust way."""

    # Sense success vs. failure
    res = Sense('clear_switch_state_fallback')
    if res == FAILURE:
        log_err('Sense() returned FAILURE for "clear_switch_state_fallback"')
        return FAILURE

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def disconnect_reconnect_switch_port(component_id):
    """Disconnect and then reconnect switch port with most transmitted traffic."""

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


def disconnect_switch_port(component_id):
    """Disconnect switch port with most transmitted traffic."""

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
    kill_top_proc,
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
    'kill_top_proc': 5,
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
    'kill_top_proc': 5,
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

def fix_sdn(config):
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
                        rae.do_task('fix_component', component_id, config)


def fix_ctrl(component_id, config):
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
            rae.do_task('shrink_ctrl_hosttable', component_id)
        elif do_alleviate_cpu:
            # Alleviate elevated CPU stat
            log_info('adding new task "alleviate_ctrl_cpu" for "' + component_id + '"')
            rae.do_task('alleviate_ctrl_cpu', component_id)
        elif do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            log_info('adding new task "restore_ctrl_health" for "' + component_id + '"')
            rae.do_task('restore_ctrl_health', component_id)
        else:
            # No problem could be identified from stats
            log_info('no task to add for "' + component_id + '"')
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            # log_err('could not figure out how to fix controller "' + component_id + '"')
            # rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def fix_switch(component_id, config):
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
            rae.do_task('shrink_switch_flowtable', component_id)
        elif do_alleviate_cpu:
            # Alleviate elevated CPU stat
            log_info('adding new task "alleviate_switch_cpu" for "' + component_id + '"')
            rae.do_task('alleviate_switch_cpu', component_id)
        elif do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            log_info('adding new task "restore_switch_health" for "' + component_id + '"')
            rae.do_task('restore_switch_health', component_id)
        else:
            # No problem could be identified from stats
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            log_err('could not figure out how to fix switch "' + component_id + '"')
            rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def handle_event(event, config):
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
                rae.do_task('fix_component', component, config)

        # Unhandled event source
        else:
            log_err('unhandled event source "' + event['source'] + '"')
            rae.do_command(fail)


def ctrl_clearstate_besteffort(component_id):
    """Method to clear controller state (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(clear_ctrl_state_besteffort, component_id)


def ctrl_clearstate_fallback(component_id):
    """Method to clear controller state (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(clear_ctrl_state_fallback, component_id)


def ctrl_reinstall_besteffort(component_id):
    """Method to reinstall controller software (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(reinstall_ctrl_besteffort, component_id)


def ctrl_reinstall_fallback(component_id):
    """Method to reinstall controller software (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        log_err('component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(reinstall_ctrl_fallback, component_id)


def component_restartvm(component_id):
    """Method to restart the virtual machine of a component."""

    rae.do_command(restart_vm, component_id)


def component_kill_top_proc(component_id):
    """Method to kill the top CPU-consuming process in a component virtual machine."""

    rae.do_command(kill_top_proc, component_id)


def switch_clearstate_besteffort(component_id):
    """Method to clear switch state (best effort)."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(clear_switch_state_besteffort, component_id)


def switch_clearstate_fallback(component_id):
    """Method to clear switch state (fallback)."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(clear_switch_state_fallback, component_id)


def switch_discon_recon_txport(component_id):
    """Method to disconnect and then reconnect switch port with most transmitted traffic."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(disconnect_reconnect_switch_port, component_id)


def switch_disconnect_txport(component_id):
    """Method to disconnect switch port with most transmitted traffic."""

    if not is_component_type(component_id, 'SWITCH'):
        log_err('component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(disconnect_switch_port, component_id)


#
# Task-to-method mappings
#

rae.declare_task('fix_sdn', 'config')

rae.declare_task('fix_component', 'component_id', 'config')
rae.declare_task('fix_ctrl', 'component_id', 'config')
rae.declare_task('fix_switch', 'component_id', 'config')

rae.declare_task('handle_event', 'event', 'config')

rae.declare_task('shrink_ctrl_hosttable', 'component_id')
rae.declare_task('alleviate_ctrl_cpu', 'component_id')
rae.declare_task('restore_ctrl_health', 'component_id')

rae.declare_task('shrink_switch_flowtable', 'component_id')
rae.declare_task('alleviate_switch_cpu', 'component_id')
rae.declare_task('restore_switch_health', 'component_id')

rae.declare_methods(
    'fix_sdn',
    fix_sdn
)

rae.declare_methods(
    'fix_component',
    fix_ctrl,
    fix_switch
)
rae.declare_methods(
    'fix_ctrl',
    fix_ctrl
)
rae.declare_methods(
    'fix_switch',
    fix_switch
)

rae.declare_methods(
    'handle_event',
    handle_event
)

rae.declare_methods(
    'shrink_ctrl_hosttable',
    ctrl_clearstate_besteffort,
    ctrl_clearstate_fallback,
    ctrl_reinstall_besteffort,
    ctrl_reinstall_fallback
)
rae.declare_methods(
    'alleviate_ctrl_cpu',
    component_kill_top_proc,
    ctrl_reinstall_besteffort,
    ctrl_reinstall_fallback,
    component_restartvm
)
rae.declare_methods(
    'restore_ctrl_health',
    ctrl_reinstall_besteffort,
    ctrl_reinstall_fallback,
    component_restartvm
)

rae.declare_methods(
    'shrink_switch_flowtable',
    switch_clearstate_besteffort,
    switch_clearstate_fallback
)
rae.declare_methods(
    'alleviate_switch_cpu',
    switch_discon_recon_txport,
    component_kill_top_proc,
    switch_clearstate_besteffort,
    switch_clearstate_fallback,
    switch_disconnect_txport
)
rae.declare_methods(
    'restore_switch_health',
    switch_discon_recon_txport,
    switch_clearstate_besteffort,
    switch_clearstate_fallback,
    switch_disconnect_txport
)
