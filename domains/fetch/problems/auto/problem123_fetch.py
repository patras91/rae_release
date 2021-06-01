__author__ = 'patras'
from domains.fetch.domain_fetch import *
from shared.timer import DURATION

DURATION.TIME = {
    'put': 2,
    'take': 2,
    'perceive': 2,
    'charge': 2,
    'move': 2,
    'moveToEmergency': 2,
    'moveCharger': 2,
    'addressEmergency': 2,
    'wait': 2,
}

DURATION.COUNTER = {
    'put': 2,
    'take': 2,
    'perceive': 2,
    'charge': 2,
    'move': 2,
    'moveToEmergency': 2,
    'moveCharger': 2,
    'addressEmergency': 2,
    'wait': 2,
}

def SetInitialStateVariables(state, rv):
    rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rv.EDGES = {1: [7], 2: [8], 3: [8], 4: [8, 9], 5: [7], 6: [7], 7: [1, 5, 6, 8], 8: [2, 3, 4, 7], 9: [4, 10], 10: [9]}
    rv.OBJECTS=['o1']

    rv.ROBOTS=['r1']

    state.loc = {'r1': 1}
    state.charge = {'r1': 3}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': 7}
    state.containers = { 1:[],2:[],3:[],4:[],5:[],6:[],7:['o1'],8:[],9:[],10:[],}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    6: [['fetch', 'r1', 'o1']],
    8: [['emergency', 'r1', 2, 1]],
}
eventsEnv = {
}