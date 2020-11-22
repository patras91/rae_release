__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state, rv

# Attack category number 1 (exhaust ctrl memory)
# Problem number 57

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
            'critical': True
        },
        'switch11': {
            'id': 'switch11',
            'type': 'SWITCH',
            'critical': False
        },
        'switch12': {
            'id': 'switch12',
            'type': 'SWITCH',
            'critical': False
        },
        'switch13': {
            'id': 'switch13',
            'type': 'SWITCH',
            'critical': True
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
        'switch19': {
            'id': 'switch19',
            'type': 'SWITCH',
            'critical': False
        },
        'switch20': {
            'id': 'switch20',
            'type': 'SWITCH',
            'critical': True
        },
        'switch21': {
            'id': 'switch21',
            'type': 'SWITCH',
            'critical': True
        },
        'switch22': {
            'id': 'switch22',
            'type': 'SWITCH',
            'critical': False
        },
        'switch23': {
            'id': 'switch23',
            'type': 'SWITCH',
            'critical': False
        },
        'switch24': {
            'id': 'switch24',
            'type': 'SWITCH',
            'critical': False
        },
        'switch25': {
            'id': 'switch25',
            'type': 'SWITCH',
            'critical': True
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 4097,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 18,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl2': {
            'health': {
                'value': 0.75,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 69,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 1571,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 17,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl3': {
            'health': {
                'value': 0.05,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 2732,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 264,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.88,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 63,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 480,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 42,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 362,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 79,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 541,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 27,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 956,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 317,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.55,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 370,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.7,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 969,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.72,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 80,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 658,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 795,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 575,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 51,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 860,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 96,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 179,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 10,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 339,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 97,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 92,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 718,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 28,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 635,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 55,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 606,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 795,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch19': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 14,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 879,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.81,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 50,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 481,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.81,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 31,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 960,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 68,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 365,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 64,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 178,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch24': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 85,
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
        'switch25': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 69,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 205,
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
    1: [['fix_component', 'ctrl3', secmgr_config, 'A number of components are low on resources, including ctrl3']],
    2: [['fix_component', 'switch15', secmgr_config, 'A number of components are low on resources, including switch15']],
    3: [['fix_component', 'switch18', secmgr_config, 'A number of components are low on resources, including switch18']]
}

eventsEnv = {}
