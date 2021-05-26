__author__ = 'patras'
from domains.fetch.domain_fetch import *
from shared.timer import DURATION

DURATION.TIME = {
    'put': 5,
    'take': 5,
    'perceive': 3,
    'charge': 10,
    'move': 10,
    'moveToEmergency': 20,
    'moveCharger': 15,
    'addressEmergency': 20,
    'wait': 10,
}

DURATION.COUNTER = {
    'put': 5,
    'take': 5,
    'perceive': 3,
    'charge': 10,
    'move': 10,
    'moveToEmergency': 20,
    'moveCharger': 15,
    'addressEmergency': 20,
    'wait': 10,
}

def SetInitialStateVariables(state, rv):
    rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [5, 3, 6, 7], 5: [4, 9], 6: [4, 10], 7: [4, 8], 8: [7], 9: [5], 10: [6]}
    rv.OBJECTS=['o1']

    rv.ROBOTS=['r1']

    state.loc = {'r1': 1}
    state.charge = {'r1': 3}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': 10}
    state.containers = { 1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:['o1'],}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    4: [['fetch', 'r1', 'o1']],
}
eventsEnv = {
}