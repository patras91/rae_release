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
    'critical': False
    },
'ctrl1': {
    'id': 'ctrl1',
    'type': 'CTRL',
    'critical': False
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
    'critical': True
    },
'switch9': {
    'id': 'switch9',
    'type': 'SWITCH',
    'critical': True
    },
    }

    state.stats = {
'ctrl0': {
        'health': {
            'value': 1,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 50,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 11505,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.46,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 74,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 8095,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.68,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 78,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 397,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 0.25,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 71,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 419,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.8,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 75,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1171,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.44,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 89,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 553,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.65,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 54,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 209,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.71,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 49,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1150,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 0.09,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 115,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1496,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch7': {
        'health': {
            'value': 0.02,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 57,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 932,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch8': {
        'health': {
            'value': 0.35,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 57,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 688,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch9': {
        'health': {
            'value': 0.53,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 81,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 556,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'ctrl0'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

