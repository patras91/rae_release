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
    'critical': True
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
'ctrl4': {
    'id': 'ctrl4',
    'type': 'CTRL',
    'critical': True
    },
'ctrl5': {
    'id': 'ctrl5',
    'type': 'CTRL',
    'critical': True
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
    'critical': True
    },
'ctrl9': {
    'id': 'ctrl9',
    'type': 'CTRL',
    'critical': False
    },
'ctrl10': {
    'id': 'ctrl10',
    'type': 'CTRL',
    'critical': True
    },
'ctrl11': {
    'id': 'ctrl11',
    'type': 'CTRL',
    'critical': True
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
    'critical': False
    },
    }

    state.stats = {
'ctrl0': {
        'health': {
            'value': 0.91,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 41,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 14783,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.73,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 82,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 14646,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl2': {
        'health': {
            'value': 0.37,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 77,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 9145,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl3': {
        'health': {
            'value': 0.24,
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
'ctrl4': {
        'health': {
            'value': 0.82,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 119,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11428,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl5': {
        'health': {
            'value': 0.36,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 86,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 10325,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl6': {
        'health': {
            'value': 0.24,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 119,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 8279,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl7': {
        'health': {
            'value': 0.85,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 30,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 14535,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl8': {
        'health': {
            'value': 0.37,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 68,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11922,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl9': {
        'health': {
            'value': 0.67,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 40,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11882,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl10': {
        'health': {
            'value': 0.68,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 96,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 9778,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl11': {
        'health': {
            'value': 0.58,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 71,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6184,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl12': {
        'health': {
            'value': 0.68,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 83,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 5713,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.84,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 56,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 985,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 0.43,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 120,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 956,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.44,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 41,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1453,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.8,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 110,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1138,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.97,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 61,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 304,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.04,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 45,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 690,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 0.25,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 50,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 461,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch7': {
        'health': {
            'value': 0.26,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 27,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 235,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch8': {
        'health': {
            'value': 0.09,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 77,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 582,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch9': {
        'health': {
            'value': 0.24,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 78,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 627,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch10': {
        'health': {
            'value': 0.87,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 106,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1091,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch11': {
        'health': {
            'value': 0.25,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 88,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 424,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch12': {
        'health': {
            'value': 0.09,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 43,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1390,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'ctrl3'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

