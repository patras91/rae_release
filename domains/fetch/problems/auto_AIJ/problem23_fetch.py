__author__ = 'patras'
from domain_fetch import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'put': 2,
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveToEmergency': 5,
    'moveCharger': 15,
    'addressEmergency': 10,
    'wait': 5,
}

DURATION.COUNTER = {
    'put': 2,
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveToEmergency': 5,
    'moveCharger': 15,
    'addressEmergency': 10,
    'wait': 5,
}

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]}
rv.OBJECTS=['o1']

rv.ROBOTS=['r1']

def ResetState():
    state.loc = {'r1': 4}
    state.charge = {'r1': 4}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': UNK}
    state.containers = { 1:[],2:[],3:[],4:['o1'],}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    7: [['fetch', 'r1', 'o1']],
}
eventsEnv = {
}