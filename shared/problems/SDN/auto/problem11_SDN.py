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
            'critical': False
        },
        'switch23': {
            'id': 'switch23',
            'type': 'SWITCH',
            'critical': True
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.74,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 52,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 3910,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.59,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 75,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 730,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 31,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 917,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.59,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 761,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.5,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 83,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 876,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.93,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 15,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 714,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 89,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 386,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.14,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 130,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 680,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 940,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 810,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.68,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 61,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 189,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.55,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 16,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 344,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.78,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 50,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 527,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.57,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 13,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 472,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.89,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 23,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 394,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.92,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 831,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.99,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 71,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 310,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.4,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 58,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 537,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch18': {
            'health': {
                'value': 0.95,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 892,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch19': {
            'health': {
                'value': 0.45,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 53,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 585,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch20': {
            'health': {
                'value': 0.96,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 17,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 88,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch21': {
            'health': {
                'value': 0.82,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 23,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 662,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch22': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 74,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 277,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch23': {
            'health': {
                'value': 0.86,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 59,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 987,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
    }


rv.x = []

tasks = {
    1: [['fix_component', 'switch7', secmgr_config]],
    2: [['fix_component', 'switch17', secmgr_config]],
    3: [['fix_component', 'switch19', secmgr_config]]
}

eventsEnv = {}
