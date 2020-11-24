__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state, rv

# Attack category number 2 (exhaust switch memory)
# Problem number 131

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
            'critical': True
        },
        'switch3': {
            'id': 'switch3',
            'type': 'SWITCH',
            'critical': True
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
            'critical': True
        },
        'switch7': {
            'id': 'switch7',
            'type': 'SWITCH',
            'critical': True
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
            'critical': False
        },
        'switch11': {
            'id': 'switch11',
            'type': 'SWITCH',
            'critical': False
        },
        'switch12': {
            'id': 'switch12',
            'type': 'SWITCH',
            'critical': True
        },
        'switch13': {
            'id': 'switch13',
            'type': 'SWITCH',
            'critical': True
        },
        'switch14': {
            'id': 'switch14',
            'type': 'SWITCH',
            'critical': True
        },
        'switch15': {
            'id': 'switch15',
            'type': 'SWITCH',
            'critical': False
        },
        'switch16': {
            'id': 'switch16',
            'type': 'SWITCH',
            'critical': False
        },
        'switch17': {
            'id': 'switch17',
            'type': 'SWITCH',
            'critical': True
        },
        'switch18': {
            'id': 'switch18',
            'type': 'SWITCH',
            'critical': True
        },
        'switch19': {
            'id': 'switch19',
            'type': 'SWITCH',
            'critical': True
        },
        'switch20': {
            'id': 'switch20',
            'type': 'SWITCH',
            'critical': True
        },
        'switch21': {
            'id': 'switch21',
            'type': 'SWITCH',
            'critical': False
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
        'switch26': {
            'id': 'switch26',
            'type': 'SWITCH',
            'critical': False
        },
        'switch27': {
            'id': 'switch27',
            'type': 'SWITCH',
            'critical': False
        },
        'switch28': {
            'id': 'switch28',
            'type': 'SWITCH',
            'critical': True
        },
        'switch29': {
            'id': 'switch29',
            'type': 'SWITCH',
            'critical': True
        },
        'switch30': {
            'id': 'switch30',
            'type': 'SWITCH',
            'critical': True
        },
        'switch31': {
            'id': 'switch31',
            'type': 'SWITCH',
            'critical': False
        },
        'switch32': {
            'id': 'switch32',
            'type': 'SWITCH',
            'critical': False
        },
        'switch33': {
            'id': 'switch33',
            'type': 'SWITCH',
            'critical': True
        },
        'switch34': {
            'id': 'switch34',
            'type': 'SWITCH',
            'critical': False
        },
        'switch35': {
            'id': 'switch35',
            'type': 'SWITCH',
            'critical': True
        },
        'switch36': {
            'id': 'switch36',
            'type': 'SWITCH',
            'critical': True
        },
        'switch37': {
            'id': 'switch37',
            'type': 'SWITCH',
            'critical': True
        },
        'switch38': {
            'id': 'switch38',
            'type': 'SWITCH',
            'critical': True
        },
        'switch39': {
            'id': 'switch39',
            'type': 'SWITCH',
            'critical': True
        },
        'switch40': {
            'id': 'switch40',
            'type': 'SWITCH',
            'critical': True
        },
        'switch41': {
            'id': 'switch41',
            'type': 'SWITCH',
            'critical': True
        },
        'switch42': {
            'id': 'switch42',
            'type': 'SWITCH',
            'critical': True
        },
        'switch43': {
            'id': 'switch43',
            'type': 'SWITCH',
            'critical': False
        },
        'switch44': {
            'id': 'switch44',
            'type': 'SWITCH',
            'critical': False
        },
        'switch45': {
            'id': 'switch45',
            'type': 'SWITCH',
            'critical': True
        },
        'switch46': {
            'id': 'switch46',
            'type': 'SWITCH',
            'critical': False
        },
        'switch47': {
            'id': 'switch47',
            'type': 'SWITCH',
            'critical': False
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 32,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 10490,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 19,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl2': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 46,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 6651,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 20,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'ctrl3': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 3111,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 28,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 13,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 841,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.62,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 37,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.61,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 65,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 283,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 504,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.95,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 361,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.235,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 109,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 1179,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.52,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 42,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 320,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 96,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 177,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.78,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 418,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.91,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 55,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 265,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.57,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 60,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 786,
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
                'value': 35,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 433,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.41,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 100,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 259,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 353,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 295,
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
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 523,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 42,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 64,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.68,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 30,
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
        'switch19': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 24,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 191,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 32,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 411,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.79,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 663,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 89,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 604,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.41,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 10,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 37,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch24': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 31,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 496,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch25': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 35,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 488,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch26': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 426,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch27': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 376,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch28': {
            'health': {
                'value': 0.45,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 47,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 53,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch29': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 32,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch30': {
            'health': {
                'value': 0.45,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 228,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch31': {
            'health': {
                'value': 0.48,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 241,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch32': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 445,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch33': {
            'health': {
                'value': 0.8,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 27,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 336,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch34': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 834,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch35': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 972,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch36': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 83,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch37': {
            'health': {
                'value': 0.64,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 57,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 228,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch38': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 47,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 852,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch39': {
            'health': {
                'value': 0.66,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 629,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch40': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 63,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 25,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch41': {
            'health': {
                'value': 0.66,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 14,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 557,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch42': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 902,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch43': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 51,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 37,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch44': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 88,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 909,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch45': {
            'health': {
                'value': 0.52,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 69,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 493,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch46': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 42,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 499,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch47': {
            'health': {
                'value': 0.8,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 943,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
    }


rv.x = []

context = 'The component switch6 is low on resources'
tasks = {
    1: [['fix_component', 'switch6', secmgr_config, context]]
}

eventsEnv = {}
