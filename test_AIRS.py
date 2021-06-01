#!/usr/bin/env python3
__author__ = 'alex, sunandita'
# Last Modified: Sunandita: May 3, 2021

import functools
import operator
import threading

from main import InitializeAIRSDomain
from shared.state import State
#from domains.AIRS.domain_AIRS import *


def beginCommand(cmd, cmdRet, args):
    cmdRet['state'] = cmd(*args)


def exec_cmds(exec_queue, status_queue, domain):
    """TODO: add documentation.
    """

    while True:
        if not exec_queue.empty():
            (id, cmd_name, args) = exec_queue.get()
            # TODO: execute planned command
            print('Got cmd to exec: id=' + str(id) + ', cmd=' + cmd_name + ', args=' + str(args))
            cmdRet = {'state': 'running'}
            t = threading.Thread(target=beginCommand, args=(domain.GetCommand(cmd_name), cmdRet, args))
            t.start()
            t.join()
            print('Done executing cmd: ' + cmd_name)
            status_queue.put([id, cmdRet['state'], state.copy()])


def initialize_state():
    """TODO: add documentation.
    """
    pass


if __name__ == '__main__':

    verbosity = 1
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

    #set the state variables for RAE
    state = State()
    state.components = {
        'ctrl1': {
            'id': 'ctrl1',
            'type': 'CTRL',
            'critical': True
        },
        'switch1': {
            'id': 'switch1',
            'type': 'SWITCH',
            'critical': True
        },
        'switch2': {
            'id': 'switch2',
            'type': 'SWITCH',
            'critical': False
        },
        'switch3': {
            'id': 'switch3',
            'type': 'SWITCH',
            'critical': False
        },
        'switch4': {
            'id': 'switch4',
            'type': 'SWITCH',
            'critical': False
        },
        'switch5': {
            'id': 'switch5',
            'type': 'SWITCH',
            'critical': False
        },
        'switch6': {
            'id': 'switch6',
            'type': 'SWITCH',
            'critical': False
        },
        'switch7': {
            'id': 'switch7',
            'type': 'SWITCH',
            'critical': False
        },
        'switch8': {
            'id': 'switch8',
            'type': 'SWITCH',
            'critical': False
        },
        'switch9': {
            'id': 'switch9',
            'type': 'SWITCH',
            'critical': False
        },
        'switch10': {
            'id': 'switch10',
            'type': 'SWITCH',
            'critical': True
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
        },
        'switch5': {
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
    (task_queue, exec_queue, status_queue, domain) = InitializeAIRSDomain(verbosity, state)
    
    def m_fix_software(self, component_id, config, context):
        """Method to fix symptoms at the software/process level."""

        do_fix_generic = False
        do_fix_sdnctrl = False
        do_fix_switch = False
        if self.is_component_type(component_id, 'CTRL'):
            do_fix_sdnctrl = True
        elif self.is_component_type(component_id, 'SWITCH'):
            do_fix_switch = True
        else:
            do_fix_generic = True

        if do_fix_generic is True:
            self.actor.do_task('try_generic_fix', component_id, config, context)
        elif do_fix_sdnctrl is True:
            self.actor.do_task('fix_sdn_controller', component_id, config, context)
        elif do_fix_switch is True:
            self.actor.do_task('fix_switch', component_id, config, context)
        else:
            self.actor.do_command(self.fail)

    #domain.add_refinement_method('fix_component', m_fix_software)

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
    task_queue.put(['handle_event', event1, secmgr_config, "context"]) # Note to Alex: What should be the context here?

    # Execute planned commands
    exec_thread = threading.Thread(
        target=exec_cmds, args=(exec_queue, status_queue, domain)
    )
    exec_thread.start()
