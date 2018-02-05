__author__ = 'patras'

from domain_exploreEnv import *
from timer import DURATION
from rae1 import state

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
rv.LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4']
rv.EDGES = {
    'base': {
        'z1': 20,
        'z2': 10,
        'z3': 20,
        'z4': 10
    },
    'z1': {
        'base': 20,
        'z2': 30,
        'z4': 50
    },
    'z2': {
        'base': 10,
        'z1': 30,
        'z3': 30
    },
    'z3': {
        'base': 20,
        'z2': 50,
        'z4': 30
    },
    'z4': {
        'base': 10,
        'z3': 30,
        'z1': 50
    }
}

def ResetState():
    state.loc = {'r1': 'base', 'UAV': 'base'}
    state.charge = {'r1':75, 'UAV': 75}
    state.data = {'r1': 0, 'UAV': 0}
    state.load = {'r1': NIL, 'UAV': NIL}
    state.pos = {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base'}

tasks =  {
    1: ['doActivities', 'UAV', [['survey', 'z1'], ['survey', 'z3'], ['survey', 'z4']]],
    2: ['doActivities', 'r1', [['process', 'z1'], ['screen', 'z4'], ['sample', 'z2']]],
    5: ['handleEmergency', 'r1', 'z2']
}

eventsEnv = {
    1: [alienSpotted, ['z2']],
}