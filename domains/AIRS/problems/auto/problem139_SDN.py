__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state, rv

# Attack category number 2 (exhaust switch memory)
# Problem number 139

secmgr_config = {
    'health_warning_thresh': 0.6,
    'health_critical_thresh': 0.5,
    'health_action_thresh': 0.49,
    'cpu_ewma_alpha': 0.5,
    'cpu_perc_warning_thresh': 75,
    'cpu_perc_critical_thresh': 90,
    'host_table_critical_thresh': 10000,
    'flow_table_critical_thresh': 800,
    'switch_table_critical_thresh': 100
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

switch_table_exceeded_fn = functools.partial(
    operator.le,
    secmgr_config['switch_table_critical_thresh']
)

flow_table_exceeded_fn = functools.partial(
    operator.le,
    secmgr_config['flow_table_critical_thresh']
)


is_disconnected_fn = functools.partial(
    operator.eq,
    False
)


def ResetState():

    state.components = {
        'ctrl1': {
            'id': 'ctrl1',
            'type': 'CTRL',
            'critical': True
        },
        'ctrl2': {
            'id': 'ctrl2',
            'type': 'CTRL',
            'critical': False
        },
        'ctrl3': {
            'id': 'ctrl3',
            'type': 'CTRL',
            'critical': False
        },
        'switch1': {
            'id': 'switch1',
            'type': 'SWITCH',
            'critical': False
        },
        'switch2': {
            'id': 'switch2',
            'type': 'SWITCH',
            'critical': True
        },
        'switch3': {
            'id': 'switch3',
            'type': 'SWITCH',
            'critical': False
        },
        'switch4': {
            'id': 'switch4',
            'type': 'SWITCH',
            'critical': True
        },
        'switch5': {
            'id': 'switch5',
            'type': 'SWITCH',
            'critical': True
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
            'critical': True
        },
        'switch9': {
            'id': 'switch9',
            'type': 'SWITCH',
            'critical': True
        },
        'switch10': {
            'id': 'switch10',
            'type': 'SWITCH',
            'critical': False
        },
        'switch11': {
            'id': 'switch11',
            'type': 'SWITCH',
            'critical': True
        },
        'switch12': {
            'id': 'switch12',
            'type': 'SWITCH',
            'critical': False
        },
        'switch13': {
            'id': 'switch13',
            'type': 'SWITCH',
            'critical': False
        },
        'switch14': {
            'id': 'switch14',
            'type': 'SWITCH',
            'critical': False
        },
        'switch15': {
            'id': 'switch15',
            'type': 'SWITCH',
            'critical': False
        },
        'switch16': {
            'id': 'switch16',
            'type': 'SWITCH',
            'critical': True
        },
        'switch17': {
            'id': 'switch17',
            'type': 'SWITCH',
            'critical': False
        },
        'switch18': {
            'id': 'switch18',
            'type': 'SWITCH',
            'critical': True
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 17,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 2166,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 18,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl2': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 41,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 8428,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 17,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl3': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 49,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 7964,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 17,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 77,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 565,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.78,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 95,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 734,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.56,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 61,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 688,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.52,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 744,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 44,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 55,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 40,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 401,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.41,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 90,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 88,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 824,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 10,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 618,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 69,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 348,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.165,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 125,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 819,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.59,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 88,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 186,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 963,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.41,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 65,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 161,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch15': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 930,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.48,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 69,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 925,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 966,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 99,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 263,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
    }


rv.x = []

tasks = {
    1: [['fix_component', 'switch7', secmgr_config, 'A number of components are low on resources, including switch7']],
    2: [['fix_component', 'switch9', secmgr_config, 'A number of components are low on resources, including switch9']],
    3: [['fix_component', 'switch11', secmgr_config, 'A number of components are low on resources, including switch11']],
    4: [['fix_component', 'switch14', secmgr_config, 'A number of components are low on resources, including switch14']],
    5: [['fix_component', 'switch16', secmgr_config, 'A number of components are low on resources, including switch16']]
}

eventsEnv = {}
