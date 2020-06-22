__author__ = 'patras'

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
    'critical': False
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
    }

    state.stat = {
'ctrl0': {
        'health': {
            'value': 11,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 42,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 62,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 34,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 89,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 61,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl2': {
        'health': {
            'value': 84,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 1,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 61,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl3': {
        'health': {
            'value': 57,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 45,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 77,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl4': {
        'health': {
            'value': 87,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 84,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 40,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 25,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 91,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 56,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 61,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 49,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 98,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 25,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 94,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 14,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 72,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 46,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 47,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 46,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 40,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 44,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 86,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 32,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 10,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 89,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 78,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 32,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

