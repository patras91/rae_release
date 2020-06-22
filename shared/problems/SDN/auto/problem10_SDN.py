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
    'critical': False
    },
'ctrl1': {
    'id': 'ctrl1',
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
    'critical': True
    },
'switch5': {
    'id': 'switch5',
    'type': 'SWITCH',
    'critical': True
    },
    }

    state.stat = {
'ctrl0': {
        'health': {
            'value': 0.09,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 90,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 13742,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'ctrl1': {
        'health': {
            'value': 0.9,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 97,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'host_table_size': {
            'value': 9826,
            'thresh_exceeded_fn': host_table_exceeded_fn
        }
    },
'switch0': {
        'health': {
            'value': 0.41,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 88,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 683,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch1': {
        'health': {
            'value': 1,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 50,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 958,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch2': {
        'health': {
            'value': 0.24,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 104,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 324,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch3': {
        'health': {
            'value': 0.69,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 47,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 463,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch4': {
        'health': {
            'value': 0.36,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 70,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 496,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
'switch5': {
        'health': {
            'value': 0.95,
            'thresh_exceeded_fn': health_exceeded_fn
        },
        'cpu_perc_ewma': {
            'value': 96,
            'thresh_exceeded_fn': cpu_perc_exceeded_fn
        },
        'flow_table_size': {
            'value': 787,
            'thresh_exceeded_fn': flow_table_exceeded_fn
        }
    },
    }

rv.x = []

event1 = {
    'source': 'sysmon',
    'type': 'alarm',
    'component_id': 'switch1'
}

tasks = {
    1: [['handle_event', event1, secmgr_config]]
}

eventsEnv = {}

