__author__ = 'patras'
from domains.fetch.domain_fetch import *
from shared.timer import DURATION

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

def SetInitialStateVariables(state, rv):
    rv.LOCATIONS = [1, 2, 3, 4]
    rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]}
    rv.OBJECTS=['o1']

    rv.ROBOTS=['r1']

    state.loc = {'r1': 3}
    state.charge = {'r1': 4}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': UNK}
    state.containers = { 1:[],2:[],3:[],4:['o1'],}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    8: [['fetch', 'r1', 'o1']],
}
eventsEnv = {
}