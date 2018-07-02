__author__ = 'patras'

from domain_exploreEnv import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'survey': 5, # for domain EE
    'monitor': 5,
    'screen': 5,
    'sample': 5,
    'process': 5,
    'fly': 3,
    'deposit': 1,
    'transferData': 1,
    'take': 2,
    'put': 2,
    'move': 10,
    'charge': 5,
    'negotiate': 5
 }

DURATION.COUNTER = {
    'survey': 1, # for domain EE
    'monitor': 1,
    'screen': 1,
    'sample': 1,
    'process': 1,
    'fly': 1,
    'deposit': 1,
    'transferData': 1,
    'take': 1,
    'put': 1,
    'move': 1,
    'charge': 1,
    'negotiate': 1
 }

rv.TYPE = {'e1': 'survey', 'e2': 'monitor', 'e3': 'screen', 'e4': 'sample', 'e5':'process'}
rv.EQUIPMENT = {'survey': 'e1', 'monitor': 'e2', 'screen': 'e3', 'sample': 'e4', 'process': 'e5'}
rv.LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8']
rv.EDGES = {
    'base': {
        'z1': 50,
        'z3': 20,
        'z6': 40,
        'z7': 10
    },
    'z1': {
        'base': 50,
        'z2': 20,
    },
    'z2': {
        'z1': 20,
    },
    'z3': {
        'base': 20,
        'z4': 20
    },
    'z4': {
        'z3': 20,
        'z5': 20,
    },
    'z5': {
        'z4': 20,
    },
    'z6': {
        'base': 40
    },
    'z7': {
        'base': 10,
        'z8': 10
    },
    'z8': {
        'z7': 10
    }
}

def ResetState():
    state.loc = {'r1': 'base', 'UAV': 'base', 'r2': 'z6'}
    state.charge = {'r1':100, 'UAV': 100, 'r2': 75}
    state.data = {'r1': 0, 'UAV': 0, 'r2': 0}
    state.load = {'r1': NIL, 'UAV': NIL, 'r2': 'e3'}
    state.pos = {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'r2', 'e4': 'base', 'e5': 'base'}

tasks =  {
    1: ['doActivities', 'UAV', [['survey', 'z1'], ['survey', 'z3'], ['survey', 'z4'], ['survey', 'z1'], ['survey', 'z3'], ['survey', 'z7']]],
    2: ['doActivities', 'r1', [['process', 'z1'], ['screen', 'z4'], ['sample', 'z2']]],
}

eventsEnv = {
    2: [alienSpotted, ['z5']]
}