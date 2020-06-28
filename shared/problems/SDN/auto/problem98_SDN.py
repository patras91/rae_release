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
            'critical': False
        },
        'ctrl2': {
            'id': 'ctrl2',
            'type': 'CTRL',
            'critical': True
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
            'critical': False
        },
        'switch18': {
            'id': 'switch18',
            'type': 'SWITCH',
            'critical': False
        },
    }

    state.stats = {
        'ctrl1': {
            'health': {
                'value': 0.85,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 26,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 8700,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'ctrl2': {
            'health': {
                'value': 0.43,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 39,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 2506,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'ctrl3': {
            'health': {
                'value': 0.4,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 66,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'host_table_size': {
                'value': 3009,
                'thresh_exceeded_fn': host_table_exceeded_fn
            }
        },
        'switch1': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 10,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 113,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch2': {
            'health': {
                'value': 0.42,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 66,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 347,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch3': {
            'health': {
                'value': 0.51,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 56,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 535,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch4': {
            'health': {
                'value': 0.55,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 67,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 304,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch5': {
            'health': {
                'value': 0.6,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 28,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 198,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch6': {
            'health': {
                'value': 0.76,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 82,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 295,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch7': {
            'health': {
                'value': 0.56,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 68,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 500,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch8': {
            'health': {
                'value': 0.72,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 38,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 98,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch9': {
            'health': {
                'value': 0.63,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 62,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 228,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch10': {
            'health': {
                'value': 0.62,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 87,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 487,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch11': {
            'health': {
                'value': 0.46,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 11,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 195,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch12': {
            'health': {
                'value': 0.4,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 25,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 807,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch13': {
            'health': {
                'value': 0.49,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 97,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 850,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch14': {
            'health': {
                'value': 0.125,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 143,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 1050,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch15': {
            'health': {
                'value': 0.83,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 27,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 117,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch16': {
            'health': {
                'value': 0.73,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 85,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 142,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch17': {
            'health': {
                'value': 0.77,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 49,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 621,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
        'switch18': {
            'health': {
                'value': 1.0,
                'thresh_exceeded_fn': health_exceeded_fn
            },
            'cpu_perc_ewma': {
                'value': 85,
                'thresh_exceeded_fn': cpu_perc_exceeded_fn
            },
            'flow_table_size': {
                'value': 791,
                'thresh_exceeded_fn': flow_table_exceeded_fn
            }
        },
    }


rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'switch14'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}
