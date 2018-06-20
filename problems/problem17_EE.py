__author__ = 'patras'

from domain_exploreEnv import *
from timer import DURATION
from ape import state

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
        'z2': 10,
        'z8': 50,
    },
    'z1': {
        'z2': 10,
    },
    'z2': {
        'z1': 10,
        'z3': 5,
        'base': 10
    },
    'z3': {
        'z2': 5,
        'z4': 10
    },
    'z4': {
        'z3': 10,
        'z5': 5,
    },
    'z5': {
        'z4': 5,
        'z6': 20,
    },
    'z6': {
        'z5': 20,
        'z8': 30
    },
    'z7': {
        'z8': 40
    },
    'z8': {
        'base': 50,
        'z6': 30,
        'z7': 40
    }
}

def ResetState():
    state.loc = {'r1': 'base', 'UAV': 'base', 'r2': 'base'}
    state.charge = {'r1':75, 'UAV': 75, 'r2': 75}
    state.data = {'r1': 0, 'UAV': 0, 'r2': 0}
    state.load = {'r1': NIL, 'UAV': NIL, 'r2': NIL}
    state.pos = {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base'}

tasks =  {
    1: ['doActivities', 'UAV', [['survey', 'z1'], ['survey', 'z3'], ['survey', 'z4']]],
    #2: ['doActivities', 'r1', [['process', 'z1'], ['screen', 'z4'], ['sample', 'z2']]],
    #3: ['handleEmergency', 'r2', 'z5']
}

eventsEnv = {
    2: [alienSpotted, ['z5']]
}