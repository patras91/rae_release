__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from state import state

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
            'critical': True
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
            'critical': True
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
            'critical': False
        },
        'switch18': {
            'id': 'switch18',
            'type': 'SWITCH',
            'critical': False
        },
        'switch19': {
            'id': 'switch19',
            'type': 'SWITCH',
            'critical': False
        },
        'switch20': {
            'id': 'switch20',
            'type': 'SWITCH',
            'critical': False
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
            'critical': True
        },
        'switch27': {
            'id': 'switch27',
            'type': 'SWITCH',
            'critical': True
        },
        'switch28': {
            'id': 'switch28',
            'type': 'SWITCH',
            'critical': False
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
            'critical': False
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
            'critical': True
        },
        'switch47': {
            'id': 'switch47',
            'type': 'SWITCH',
            'critical': True
        },
        'switch48': {
            'id': 'switch48',
            'type': 'SWITCH',
            'critical': False
        },
        'switch49': {
            'id': 'switch49',
            'type': 'SWITCH',
            'critical': False
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
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.33,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 80,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 19727,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 33,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 544,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.66,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 98,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 133,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 701,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 18,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 695,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 37,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 582,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 99,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 429,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 28,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 965,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 71,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 376,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 49,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 556,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.68,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 304,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 414,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 123,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 65,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 37,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.62,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 66,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 113,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 143,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 32,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 364,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.58,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 13,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 435,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.75,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 24,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 703,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch19': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 18,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 957,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.56,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 820,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 42,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 98,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 79,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 259,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 64,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 390,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch24': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 654,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch25': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 56,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 111,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch26': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 437,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch27': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 227,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch28': {
            'health': {
                'value': 0.95,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 520,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch29': {
            'health': {
                'value': 0.9,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 30,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 393,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch30': {
            'health': {
                'value': 0.52,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 42,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch31': {
            'health': {
                'value': 0.66,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 40,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 517,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch32': {
            'health': {
                'value': 0.81,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 73,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 492,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch33': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 713,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch34': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 15,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 830,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch35': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 92,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 822,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch36': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 92,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 181,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch37': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 52,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 583,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch38': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 73,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 501,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch39': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 628,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch40': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 68,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 701,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch41': {
            'health': {
                'value': 0.94,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 55,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 378,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch42': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 86,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 159,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch43': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 81,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 453,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch44': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 776,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch45': {
            'health': {
                'value': 0.47,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 45,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 876,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch46': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 49,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 457,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch47': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 84,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 258,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch48': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 90,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 737,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch49': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 28,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 408,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch50': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 12,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 71,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch51': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 81,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch52': {
            'health': {
                'value': 0.78,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 51,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 149,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch53': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 96,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 161,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch54': {
            'health': {
                'value': 0.8,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 60,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 320,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
    }


rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'ctrl1'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}
