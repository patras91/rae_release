__author__ = 'patras'
from domain_chargeableRobot import *
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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [5, 3, 6, 7], 5: [4, 9], 6: [4, 10], 7: [4, 8], 8: [7], 9: [5], 10: [6]}
rv.OBJECTS=['o1']

rv.ROBOTS=['r1']

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1': 2}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': 8}
    state.containers = { 1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:['o1'],9:[],10:[],}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    4: [['fetch', 'r1', 'o1']],
}
eventsEnv = {
}