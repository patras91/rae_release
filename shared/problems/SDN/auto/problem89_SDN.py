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
            'critical': True
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
            'critical': True
        },
        'switch26': {
            'id': 'switch26',
            'type': 'SWITCH',
            'critical': True
        },
        'switch27': {
            'id': 'switch27',
            'type': 'SWITCH',
            'critical': False
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
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.36,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 136,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 2203,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'ctrl2': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 15,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 6350,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'ctrl3': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 63,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 9935,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 808,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.88,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 79,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 986,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.61,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 27,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 625,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 46,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 818,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 71,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 24,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 441,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.75,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 36,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 451,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.54,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 32,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 782,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.59,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 24,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 493,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.58,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 94,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 550,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 93,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 762,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 292,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.91,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 903,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.94,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 23,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 666,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.97,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 29,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 641,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 110,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.41,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 44,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 703,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.87,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 77,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 371,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch19': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 55,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 311,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 655,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 393,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.56,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 92,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 330,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.71,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 83,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 75,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch24': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 21,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 695,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch25': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 53,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 788,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch26': {
            'health': {
                'value': 0.8,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 57,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 43,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch27': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 80,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 278,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch28': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 99,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 952,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch29': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 336,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch30': {
            'health': {
                'value': 0.65,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 80,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 195,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch31': {
            'health': {
                'value': 0.88,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 489,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch32': {
            'health': {
                'value': 0.44,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 39,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 893,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch33': {
            'health': {
                'value': 0.99,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 86,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch34': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 146,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch35': {
            'health': {
                'value': 0.67,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 72,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 186,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch36': {
            'health': {
                'value': 0.53,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 40,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 481,
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

context = 'A security event was detected on ctrl1'
tasks = {
    1: [['handle_event', event1, secmgr_config, context]]
}

eventsEnv = {}
