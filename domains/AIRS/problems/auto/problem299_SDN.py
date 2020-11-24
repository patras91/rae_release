__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state, rv

# Attack category number 3 (disconnect switch from ctrl)
# Problem number 299

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
            'critical': True
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
            'critical': True
        },
        'switch12': {
            'id': 'switch12',
            'type': 'SWITCH',
            'critical': True
        },
        'switch13': {
            'id': 'switch13',
            'type': 'SWITCH',
            'critical': False
        },
        'switch14': {
            'id': 'switch14',
            'type': 'SWITCH',
            'critical': True
        },
        'switch15': {
            'id': 'switch15',
            'type': 'SWITCH',
            'critical': True
        },
        'switch16': {
            'id': 'switch16',
            'type': 'SWITCH',
            'critical': True
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
            'critical': False
        },
        'switch26': {
            'id': 'switch26',
            'type': 'SWITCH',
            'critical': False
        },
        'switch27': {
            'id': 'switch27',
            'type': 'SWITCH',
            'critical': True
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
            'critical': False
        },
        'switch31': {
            'id': 'switch31',
            'type': 'SWITCH',
            'critical': True
        },
        'switch32': {
            'id': 'switch32',
            'type': 'SWITCH',
            'critical': False
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.77,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 60,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 8646,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 28,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 27,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 512,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 97,
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
        'switch3': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 96,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 16,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 957,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 924,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 54,
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
        'switch7': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 63,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 41,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 46,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 284,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.45,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 32,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 949,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': False,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 562,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.48,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 41,
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
        'switch12': {
            'health': {
                'value': 0.84,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 83,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 874,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.68,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 44,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 245,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 547,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 96,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 290,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 71,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 49,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.64,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 851,
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
                'value': 41,
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
        'switch19': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 57,
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
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 33,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 46,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 771,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.88,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 80,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 775,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.79,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 876,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch24': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 66,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch25': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 126,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch26': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 139,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch27': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 29,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 569,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch28': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 53,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 965,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch29': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 929,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch30': {
            'health': {
                'value': 0.55,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 763,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch31': {
            'health': {
                'value': 0.99,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 83,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 489,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch32': {
            'health': {
                'value': 0.91,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 60,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 388,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
    }


rv.x = []

context = 'The component switch9 is disconnected from its ctrl'
tasks = {
    1: [['fix_component', 'switch9', secmgr_config, context]]
}

eventsEnv = {}
