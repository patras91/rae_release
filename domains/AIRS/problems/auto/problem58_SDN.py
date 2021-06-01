__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state, rv

# Attack category number 1 (exhaust ctrl memory)
# Problem number 58

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
            'critical': True
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
            'critical': False
        },
        'switch21': {
            'id': 'switch21',
            'type': 'SWITCH',
            'critical': False
        },
        'switch22': {
            'id': 'switch22',
            'type': 'SWITCH',
            'critical': True
        },
        'switch23': {
            'id': 'switch23',
            'type': 'SWITCH',
            'critical': True
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
            'critical': True
        },
        'switch33': {
            'id': 'switch33',
            'type': 'SWITCH',
            'critical': True
        },
        'switch34': {
            'id': 'switch34',
            'type': 'SWITCH',
            'critical': True
        },
        'switch35': {
            'id': 'switch35',
            'type': 'SWITCH',
            'critical': False
        },
        'switch36': {
            'id': 'switch36',
            'type': 'SWITCH',
            'critical': False
        },
        'switch37': {
            'id': 'switch37',
            'type': 'SWITCH',
            'critical': True
        },
        'switch38': {
            'id': 'switch38',
            'type': 'SWITCH',
            'critical': False
        },
        'switch39': {
            'id': 'switch39',
            'type': 'SWITCH',
            'critical': True
        },
        'switch40': {
            'id': 'switch40',
            'type': 'SWITCH',
            'critical': False
        },
        'switch41': {
            'id': 'switch41',
            'type': 'SWITCH',
            'critical': True
        },
        'switch42': {
            'id': 'switch42',
            'type': 'SWITCH',
            'critical': False
        },
        'switch43': {
            'id': 'switch43',
            'type': 'SWITCH',
            'critical': False
        },
        'switch44': {
            'id': 'switch44',
            'type': 'SWITCH',
            'critical': True
        },
        'switch45': {
            'id': 'switch45',
            'type': 'SWITCH',
            'critical': False
        },
        'switch46': {
            'id': 'switch46',
            'type': 'SWITCH',
            'critical': False
        },
        'switch47': {
            'id': 'switch47',
            'type': 'SWITCH',
            'critical': True
        },
        'switch48': {
            'id': 'switch48',
            'type': 'SWITCH',
            'critical': True
        },
        'switch49': {
            'id': 'switch49',
            'type': 'SWITCH',
            'critical': True
        },
        'switch50': {
            'id': 'switch50',
            'type': 'SWITCH',
            'critical': False
        },
        'switch51': {
            'id': 'switch51',
            'type': 'SWITCH',
            'critical': True
        },
        'switch52': {
            'id': 'switch52',
            'type': 'SWITCH',
            'critical': False
        },
        'switch53': {
            'id': 'switch53',
            'type': 'SWITCH',
            'critical': True
        },
        'switch54': {
            'id': 'switch54',
            'type': 'SWITCH',
            'critical': False
        },
        'switch55': {
            'id': 'switch55',
            'type': 'SWITCH',
            'critical': False
        },
        'switch56': {
            'id': 'switch56',
            'type': 'SWITCH',
            'critical': True
        },
        'switch57': {
            'id': 'switch57',
            'type': 'SWITCH',
            'critical': True
        },
        'switch58': {
            'id': 'switch58',
            'type': 'SWITCH',
            'critical': True
        },
        'switch59': {
            'id': 'switch59',
            'type': 'SWITCH',
            'critical': False
        },
        'switch60': {
            'id': 'switch60',
            'type': 'SWITCH',
            'critical': True
        },
        'switch61': {
            'id': 'switch61',
            'type': 'SWITCH',
            'critical': False
        },
        'switch62': {
            'id': 'switch62',
            'type': 'SWITCH',
            'critical': False
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 56,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 6624,
                'thresh_exceeded_fn': host_table_exceeded_fn
            },
            'switch_table_size': {
                'value': 798,
                'thresh_exceeded_fn': switch_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 107,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.48,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 89,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 740,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.57,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
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
        'switch4': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 66,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 292,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.58,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 34,
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
        'switch6': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 215,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.95,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 338,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.88,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 224,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 45,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 105,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.66,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 272,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 45,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 891,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.52,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 739,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 91,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 310,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 73,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 659,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 18,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 165,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 53,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 116,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 462,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 66,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 423,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch19': {
            'health': {
                'value': 0.72,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 640,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 600,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 90,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 410,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 31,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 18,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 194,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch24': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 44,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 393,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch25': {
            'health': {
                'value': 0.59,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 47,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 725,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch26': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 64,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 709,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch27': {
            'health': {
                'value': 0.98,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 53,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 56,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch28': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 185,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch29': {
            'health': {
                'value': 0.99,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
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
        'switch30': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 807,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch31': {
            'health': {
                'value': 0.62,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 47,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 85,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch32': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 40,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 570,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch33': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 77,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 347,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch34': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 28,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 609,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch35': {
            'health': {
                'value': 0.55,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 48,
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
        'switch36': {
            'health': {
                'value': 0.68,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 87,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 598,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch37': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 749,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch38': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 61,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 145,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch39': {
            'health': {
                'value': 0.75,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 16,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 425,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch40': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 99,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 216,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch41': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 43,
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
        'switch42': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 91,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 402,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch43': {
            'health': {
                'value': 0.94,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 10,
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
        'switch44': {
            'health': {
                'value': 0.7,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 83,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 881,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch45': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 70,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 680,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch46': {
            'health': {
                'value': 0.61,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 98,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 779,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch47': {
            'health': {
                'value': 0.75,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 72,
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
        'switch48': {
            'health': {
                'value': 0.77,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 534,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch49': {
            'health': {
                'value': 0.72,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 68,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch50': {
            'health': {
                'value': 0.8,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 24,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 134,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch51': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 34,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 405,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch52': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 95,
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
        'switch53': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 29,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 581,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch54': {
            'health': {
                'value': 0.64,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 23,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 980,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch55': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 43,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 526,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch56': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 550,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch57': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 934,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch58': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 982,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch59': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 29,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 189,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch60': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 868,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch61': {
            'health': {
                'value': 0.98,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 478,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
        'switch62': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 24,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 156,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            },
            'is_conn_to_ctrl': {
                'value': True,
                'thresh_exceeded_fn': is_disconnected_fn
            }
        },
    }


rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'ctrl1'
}

context = 'A security event was detected on ctrl1'
tasks = {
    1: [['handle_event', event1, secmgr_config, context]]
}

eventsEnv = {}
