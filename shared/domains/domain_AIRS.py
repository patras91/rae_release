#!/usr/bin/env python3
"""Domain definition for AIRS SDN to work with RAE.

This file defines the tasks, methods, and commands for the AIRS SDN domain.
"""

from domain_constants import SUCCESS, FAILURE
from state import state
from timer import DURATION
import RAE1_and_RAEplan as rae


#
# Helper functions
#

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
    """Restart the SDN controller virtual machine."""

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


def clear_ctrl_state_besteffort(component_id):
    """Clear the SDN controller state (including host table), if possible."""

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_ctrl_state_fallback(component_id):
    """Clear the SDN controller state (including host table) in a more robust way."""

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_besteffort(component_id):
    """Reinstall the SDN controller software, if possible."""

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def reinstall_ctrl_fallback(component_id):
    """Reinstall the SDN controller software in a more robust way."""

    stat = get_component_stat(component_id, 'host_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_besteffort(component_id):
    """Clear the switch state (including flow table), if possible."""

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def clear_switch_state_fallback(component_id):
    """Clear the switch state (including flow table) in a more robust way."""

    stat = get_component_stat(component_id, 'flow_table_size')
    if stat is not None:
        stat['value'] = 0
    return SUCCESS


def disconnect_switch_port(component_id, port_idx):
    """Disconnect the switch port with the most transmitted traffic."""

    # TODO: implement
    return FAILURE


def succeed():
    """Simply return success (always succeeds)."""

    return SUCCESS


def unsure():
    """Add some cost within refinement method."""

    return SUCCESS


def fail():
    """Simply return failure (always fails)."""

    return FAILURE


# Declare commands in RAE engine
rae.declare_commands([
    restart_vm,
    clear_ctrl_state_besteffort,
    clear_ctrl_state_fallback,
    reinstall_ctrl_besteffort,
    reinstall_ctrl_fallback,
    clear_switch_state_besteffort,
    clear_switch_state_fallback,
    disconnect_switch_port,
    succeed,
    unsure,
    fail
])

DURATION.TIME = {
    'restart_vm': 60,
    'clear_ctrl_state_besteffort': 10,
    'clear_ctrl_state_fallback': 20,
    'reinstall_ctrl_besteffort': 30,
    'reinstall_ctrl_fallback': 60,
    'clear_switch_state_besteffort': 10,
    'clear_switch_state_fallback': 20,
    'disconnect_switch_port': 5,
    'succeed': 1,
    'unsure': 5,
    'fail': 1
}

DURATION.COUNTER = {
    'restart_vm': 60,
    'clear_ctrl_state_besteffort': 10,
    'clear_ctrl_state_fallback': 20,
    'reinstall_ctrl_besteffort': 30,
    'reinstall_ctrl_fallback': 60,
    'clear_switch_state_besteffort': 10,
    'clear_switch_state_fallback': 20,
    'disconnect_switch_port': 5,
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
        print('error: could not find "health_critical_thresh" in config')
        rae.do_command(fail)
    else:
        print('info: will check health for ' + str(len(state.components.keys())) + ' components')
        for component_id in state.components:
            if component_id not in state.stats or 'health' not in state.stats[component_id]:
                print('error: could not find "health" in state.stats["' + component_id + '"]')
                rae.do_command(fail)
            else:
                health_obj = state.stats[component_id]['health']
                if 'value' not in health_obj or 'thresh_exceeded_fn' not in health_obj:
                    print('error: could not find "value" or "thresh_exceeded_fn" in state.stats["'
                          + component_id + '"]["health"]')
                    rae.do_command(fail)
                else:
                    # Check for low health
                    value = health_obj['value']
                    thresh_exceeded_fn = health_obj['thresh_exceeded_fn']
                    if thresh_exceeded_fn(value):
                        print('info: threshold exceeded for stat "health": ' + component_id)
                        print('info: adding new task "fix_component" for "' + component_id + '"')
                        rae.do_task('fix_component', component_id, config)


def fix_ctrl(component_id, config):
    """Method to fix symptoms for a controller."""

    if not is_component_type(component_id, 'CTRL'):
        print('error: component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    elif component_id not in state.stats:
        print('error: could not find "' + component_id + '" in state.stats')
        rae.do_command(fail)
    else:
        # Check stats and determine what needs to be fixed
        stat_obj = state.stats[component_id]
        do_restore_health = False
        do_shrink_hosttable = False
        if 'health' in stat_obj:
            if ('value' not in stat_obj['health']
                    or 'thresh_exceeded_fn' not in stat_obj['health']):
                print('error: could not find "value" or "thresh_exceeded_fn" in state.stats["'
                      + component_id + '"]["health"]')
                rae.do_command(fail)
            else:
                # Check for low health
                value = stat_obj['health']['value']
                thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    print('info: threshold exceeded for stat "health": ' + component_id)
                    do_restore_health = True
        if 'host_table_size' in stat_obj:
            if ('value' not in stat_obj['host_table_size']
                    or 'thresh_exceeded_fn' not in stat_obj['host_table_size']):
                print('error: could not find "value" or "thresh_exceeded_fn" in state.stats["'
                      + component_id + '"]["host_table_size"]')
                rae.do_command(fail)
            else:
                # Check for inflated host table
                value = stat_obj['host_table_size']['value']
                thresh_exceeded_fn = stat_obj['host_table_size']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    print('info: threshold exceeded for stat "host_table_size"')
                    do_shrink_hosttable = True
        else:
            # TODO: probe for missing data ???
            pass

        # TODO: consider history when choosing an action here ???
        if do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            print('info: adding new task "restore_ctrl_health" for "' + component_id + '"')
            rae.do_task('restore_ctrl_health', component_id)
        elif do_shrink_hosttable:
            # Fix problem with inflated host table
            print('info: adding new task "shrink_ctrl_hosttable" for "' + component_id + '"')
            rae.do_task('shrink_ctrl_hosttable', component_id)
        else:
            # No problem could be identified from stats
            print('info: no task to add for "' + component_id + '"')
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            # print('error: could not figure out how to fix controller "' + component_id + '"')
            # rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def fix_switch(component_id, config):
    """Method to fix symptoms for a switch."""

    if not is_component_type(component_id, 'SWITCH'):
        print('error: component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    elif component_id not in state.stats:
        print('error: could not find "' + component_id + '" in state.stats')
        rae.do_command(fail)
    else:
        # Check stats and determine what needs to be fixed
        stat_obj = state.stats[component_id]
        do_restore_health = False
        do_shrink_flowtable = False
        if 'health' in stat_obj:
            if ('value' not in stat_obj['health']
                    or 'thresh_exceeded_fn' not in stat_obj['health']):
                print('error: could not find "value" or "thresh_exceeded_fn" in '
                      + 'state.stats["' + component_id + '"]["health"]')
                rae.do_command(fail)
            else:
                # Check for low health
                value = stat_obj['health']['value']
                thresh_exceeded_fn = stat_obj['health']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    print('info: threshold exceeded for stat "health"')
                    do_restore_health = True
        if 'flow_table_size' in stat_obj:
            if ('value' not in stat_obj['flow_table_size']
                    or 'thresh_exceeded_fn' not in stat_obj['flow_table_size']):
                print('error: could not find "value" or "thresh_exceeded_fn" in '
                      + 'state.stats["' + component_id + '"]["flow_table_size"]')
                rae.do_command(fail)
            else:
                # Check for inflated flow table
                value = stat_obj['flow_table_size']['value']
                thresh_exceeded_fn = stat_obj['flow_table_size']['thresh_exceeded_fn']
                if thresh_exceeded_fn(value):
                    print('info: threshold exceeded for stat "flow_table_size"')
                    do_shrink_flowtable = True
        else:
            # TODO: probe for missing data ???
            pass

        # TODO: consider history when choosing an action here ???
        if do_restore_health:
            # Restore low health (often also fixes CPU over-utilization)
            print('info: adding new task "restore_switch_health" for "' + component_id + '"')
            rae.do_task('restore_switch_health', component_id)
        elif do_shrink_flowtable:
            # Fix problem with inflated flow table
            print('info: adding new task "shrink_switch_flowtable" for "' + component_id + '"')
            rae.do_task('shrink_switch_flowtable', component_id)
        else:
            # No problem could be identified from stats
            # TODO: probe further ???
            # For now, fail
            # TODO: OR... succeed, because nothing was found to be wrong ???
            print('error: could not figure out how to fix switch "' + component_id + '"')
            rae.do_command(fail)

        # TODO: loop and continue checking stats until symptoms are gone ???


def handle_event(event, config):
    """Method to handle a specific anomaly/event."""

    # Handle event types based on their source
    if 'source' not in event:
        print('error: could not find "source" in event')
        rae.do_command(fail)
    else:
        if event['source'] == 'sysmon':
            # SysMon detects events related to high resource consumption
            low_resource_components = []

            # Add component that triggered this event
            component_id = event['component_id']
            low_resource_components.append(component_id)

            # Check stats of all other components
            for component in state.components:
                if component not in low_resource_components:

                    # Check each monitored stat
                    if component not in state.stats:
                        print('error: could not find "' + component + '" in state.stats')
                        rae.do_command(fail)
                    else:
                        for stat in state.stats[component]:
                            stat_obj = state.stats[component][stat]
                            value = stat_obj['value']
                            thresh_exceeded_fn = stat_obj['thresh_exceeded_fn']
                            if thresh_exceeded_fn(value):
                                print(
                                    'trace: stat "' + stat
                                    + '" for component "' + component
                                    + '" is exceeded'
                                )
                                low_resource_components.append(component)
                                break

            # Address symptoms of each affected component
            for component in low_resource_components:
                print('info: adding new task "fix_component" for "' + component + '"')
                rae.do_task('fix_component', component, config)

        # Unhandled event source
        else:
            print('error: unhandled event source "' + event['source'] + '"')
            rae.do_command(fail)


def ctrl_clearstate_besteffort(component_id):
    """Method to clear controller state (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        print('error: component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(clear_ctrl_state_besteffort, component_id)


def ctrl_clearstate_fallback(component_id):
    """Method to clear controller state (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        print('error: component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(clear_ctrl_state_fallback, component_id)


def ctrl_reinstall_besteffort(component_id):
    """Method to reinstall controller software (best effort)."""

    if not is_component_type(component_id, 'CTRL'):
        print('error: component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(reinstall_ctrl_besteffort, component_id)


def ctrl_reinstall_fallback(component_id):
    """Method to reinstall controller software (fallback)."""

    if not is_component_type(component_id, 'CTRL'):
        print('error: component "' + component_id + '" is not a controller')
        rae.do_command(fail)
    else:
        rae.do_command(reinstall_ctrl_fallback, component_id)


def component_restartvm(component_id):
    """Method to restart the virtual machine of a component."""

    rae.do_command(restart_vm, component_id)


def switch_clearstate_besteffort(component_id):
    """Method to clear switch state (best effort)."""

    if not is_component_type(component_id, 'SWITCH'):
        print('error: component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(clear_switch_state_besteffort, component_id)


def switch_clearstate_fallback(component_id):
    """Method to clear switch state (fallback)."""

    if not is_component_type(component_id, 'SWITCH'):
        print('error: component "' + component_id + '" is not a switch')
        rae.do_command(fail)
    else:
        rae.do_command(clear_switch_state_fallback, component_id)


#
# Task-to-method mappings
#

rae.declare_task('fix_sdn', 'config')

rae.declare_task('fix_component', 'component_id', 'config')
rae.declare_task('fix_ctrl', 'component_id', 'config')
rae.declare_task('fix_switch', 'component_id', 'config')

rae.declare_task('handle_event', 'event', 'config')

rae.declare_task('restore_ctrl_health', 'component_id')
rae.declare_task('shrink_ctrl_hosttable', 'component_id')
rae.declare_task('restore_switch_health', 'component_id')
rae.declare_task('shrink_switch_flowtable', 'component_id')

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
    'restore_ctrl_health',
    ctrl_clearstate_besteffort,
    ctrl_clearstate_fallback,
    ctrl_reinstall_besteffort,
    ctrl_reinstall_fallback,
    component_restartvm
)
rae.declare_methods(
    'shrink_ctrl_hosttable',
    ctrl_clearstate_besteffort,
    ctrl_clearstate_fallback,
    ctrl_reinstall_besteffort,
    ctrl_reinstall_fallback
)

rae.declare_methods(
    'restore_switch_health',
    switch_clearstate_besteffort,
    switch_clearstate_fallback,
    component_restartvm
)

rae.declare_methods(
    'shrink_switch_flowtable',
    switch_clearstate_besteffort,
    switch_clearstate_fallback
)
