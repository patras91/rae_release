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
    'critical': True
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
    'critical': True
    },
'ctrl7': {
    'id': 'ctrl7',
    'type': 'CTRL',
    'critical': True
    },
'ctrl8': {
    'id': 'ctrl8',
    'type': 'CTRL',
    'critical': False
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
'switch0': {
    'id': 'switch0',
    'type': 'SWITCH',
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
    'critical': True
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
            'value': 0.4,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 34,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11636,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.01,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 54,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13136,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl2': {
        'health': {
            'value': 0.49,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 74,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 10857,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl3': {
        'health': {
            'value': 1.0,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 36,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6938,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl4': {
        'health': {
            'value': 0.75,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 58,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 8769,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl5': {
        'health': {
            'value': 0.34,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 35,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 14359,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl6': {
        'health': {
            'value': 0.76,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 75,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 9532,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl7': {
        'health': {
            'value': 0.84,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 95,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11303,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl8': {
        'health': {
            'value': 0.62,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 111,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 10575,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl9': {
        'health': {
            'value': 0.16,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 55,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6969,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl10': {
        'health': {
            'value': 0.22,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 90,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 14623,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl11': {
        'health': {
            'value': 0.92,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 65,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13699,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl12': {
        'health': {
            'value': 0.87,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 103,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 7576,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.3,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 77,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1280,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 0.55,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 104,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 577,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.95,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 63,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1308,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.19,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 50,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 500,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.9,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 71,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 435,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.23,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 42,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 493,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 0.42,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 31,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 876,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch7': {
        'health': {
            'value': 0.74,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 119,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 224,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch8': {
        'health': {
            'value': 0.94,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 68,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1215,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch9': {
        'health': {
            'value': 0.01,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 83,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 202,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch10': {
        'health': {
            'value': 0.5,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 100,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1070,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch11': {
        'health': {
            'value': 0.34,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 83,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 401,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch12': {
        'health': {
            'value': 0.4,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 43,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 231,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch13': {
        'health': {
            'value': 0.76,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 54,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 326,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch14': {
        'health': {
            'value': 0.18,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 52,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 243,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'switch3'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

