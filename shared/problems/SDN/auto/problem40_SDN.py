__author__ = 'patras'

import functools
import operator
from domain_AIRS import *
from timer import DURATION
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
'ctrl0': {
    'id': 'ctrl0',
    'type': 'CTRL',
    'critical': True
    },
'ctrl1': {
    'id': 'ctrl1',
    'type': 'CTRL',
    'critical': False
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
'ctrl4': {
    'id': 'ctrl4',
    'type': 'CTRL',
    'critical': True
    },
'ctrl5': {
    'id': 'ctrl5',
    'type': 'CTRL',
    'critical': False
    },
'ctrl6': {
    'id': 'ctrl6',
    'type': 'CTRL',
    'critical': False
    },
'ctrl7': {
    'id': 'ctrl7',
    'type': 'CTRL',
    'critical': False
    },
'ctrl8': {
    'id': 'ctrl8',
    'type': 'CTRL',
    'critical': True
    },
'ctrl9': {
    'id': 'ctrl9',
    'type': 'CTRL',
    'critical': True
    },
'ctrl10': {
    'id': 'ctrl10',
    'type': 'CTRL',
    'critical': False
    },
'ctrl11': {
    'id': 'ctrl11',
    'type': 'CTRL',
    'critical': False
    },
'ctrl12': {
    'id': 'ctrl12',
    'type': 'CTRL',
    'critical': False
    },
'ctrl13': {
    'id': 'ctrl13',
    'type': 'CTRL',
    'critical': True
    },
'switch0': {
    'id': 'switch0',
    'type': 'SWITCH',
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
    }

    state.stats = {
'ctrl0': {
        'health': {
            'value': 0.77,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 101,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6390,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.88,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 112,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 12285,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl2': {
        'health': {
            'value': 0.6,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 34,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 5682,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl3': {
        'health': {
            'value': 0.74,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 109,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 9646,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl4': {
        'health': {
            'value': 0.76,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 70,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 12853,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl5': {
        'health': {
            'value': 0.84,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 39,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13600,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl6': {
        'health': {
            'value': 0.59,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 111,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13997,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl7': {
        'health': {
            'value': 0.71,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 90,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13254,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl8': {
        'health': {
            'value': 0.94,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 30,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11950,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl9': {
        'health': {
            'value': 0.33,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 57,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6625,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl10': {
        'health': {
            'value': 0.86,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 105,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 7993,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl11': {
        'health': {
            'value': 1.0,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 51,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 10573,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl12': {
        'health': {
            'value': 0.05,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 100,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 10181,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl13': {
        'health': {
            'value': 0.13,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 50,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 5000,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.13,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 73,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1160,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 0.62,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 54,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 213,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.52,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 95,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1121,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.32,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 78,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 807,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.12,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 70,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 565,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.66,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 79,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 778,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 0.73,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 32,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 974,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch7': {
        'health': {
            'value': 0.78,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 45,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1442,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch8': {
        'health': {
            'value': 0.99,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 115,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1215,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch9': {
        'health': {
            'value': 0.51,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 101,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1010,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch10': {
        'health': {
            'value': 0.4,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 59,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1193,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch11': {
        'health': {
            'value': 0.3,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 117,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1341,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch12': {
        'health': {
            'value': 0.04,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 102,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 209,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch13': {
        'health': {
            'value': 0.16,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 91,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 486,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch14': {
        'health': {
            'value': 0.64,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 89,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1447,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'ctrl13'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

