#!/usr/bin/env python3


# Imports
import functools
import operator
import threading

from testRAEandRAEplan import InitializeSecurityDomain
from state import state
from domain_AIRS import *


def exec_cmds(exec_queue, status_queue):
    """TODO: add documentation.
    """

    while True:
        if not exec_queue.empty():
            (id, cmd, args) = exec_queue.get()
            # TODO: execute planned command
            print('Got cmd to exec: id=' + str(id) + ', cmd=' + str(cmd) + ', args=' + str(args))
            t = threading.Thread(target=cmd, args=args)
            t.start()
            t.join()
            print('Done executing cmd: ' + str(cmd.__name__))
            status_queue.put([id, 'Success', state.copy()])


if __name__ == '__main__':

    verbosity = 2
    secmgr_config = {
        'health_warning_thresh': 0.6,
        'health_critical_thresh': 0.5,
        'health_action_thresh': 0.49,
        'cpu_ewma_alpha': 0.5,
        'cpu_perc_warning_thresh': 75,
        'cpu_perc_critical_thresh': 90,
        'host_table_critical_thresh': 10000,
        'flow_table_critical_thresh': 800
    }
    health_exceeded_fn = functools.partial(
        operator.ge,
        secmgr_config['health_action_thresh']
    )
    cpu_perc_exceeded_fn = functools.partial(
        operator.le,
        secmgr_config['cpu_perc_critical_thresh']
    )
    host_table_exceeded_fn = functools.partial(
        operator.le,
        secmgr_config['host_table_critical_thresh']
    )
    flow_table_exceeded_fn = functools.partial(
        operator.le,
        secmgr_config['flow_table_critical_thresh']
    )
    state.components = {
        'ctrl1': {
            'id': 'ctrl1',
            'type': 'CTRL'
        },
        'switch1': {
            'id': 'switch1',
            'type': 'SWITCH'
        },
        'switch2': {
            'id': 'switch2',
            'type': 'SWITCH'
        },
        'switch3': {
            'id': 'switch3',
            'type': 'SWITCH'
        },
        'switch4': {
            'id': 'switch4',
            'type': 'SWITCH'
        }
    }
    state.stats = {
        'ctrl1': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 100.0,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 32451,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 15.8,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 6,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch2': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 73.2,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 1200,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch3': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12.5,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 6,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch4': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 2.0,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 6,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        }
    }
    (task_queue, exec_queue, status_queue) = InitializeSecurityDomain(verbosity, state)

    # Invoke the planner
    # task_queue.put(['fix_sdn', secmgr_config])
    # task_queue.put(['fix_component', 'ctrl1', secmgr_config])
    # task_queue.put(['fix_ctrl', 'ctrl1', secmgr_config])
    # task_queue.put(['fix_switch', 'ctrl1', secmgr_config])  # should fail
    event1 = {
        'source': 'sysmon',
        'type': 'alarm',
        'component_id': 'ctrl1'
    }
    task_queue.put(['handle_event', event1, secmgr_config])

    # Execute planned commands
    exec_thread = threading.Thread(
        target=exec_cmds, args=(exec_queue, status_queue)
    )
    exec_thread.start()
