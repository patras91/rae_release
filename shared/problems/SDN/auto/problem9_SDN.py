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
    'critical': True
    },
'ctrl3': {
    'id': 'ctrl3',
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
    'critical': True
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
    }

    state.stat = {
'ctrl0': {
        'health': {
            'value': 0.54,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 95,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6072,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.29,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 103,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6195,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl2': {
        'health': {
            'value': 0.35,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 28,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 5718,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl3': {
        'health': {
            'value': 1.0,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 71,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 6264,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.36,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 35,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1026,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 0.38,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 84,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 485,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.87,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 87,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 315,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.59,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 27,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 1295,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.11,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 87,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 654,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.43,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 102,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 894,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch6': {
        'health': {
            'value': 0.24,
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
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'switch6'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

