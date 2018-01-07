__author__ = 'patras'

from domain_chargeableRobot import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5,
 }

DURATION.COUNTER = {
    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.EDGES = {
    1: [3],
    2: [3],
    3: [1, 2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6]
}

def ResetState():
    state.loc = {'r1': 1, 'r2': 2}
    state.charge = {'r1': 1, 'r2': 4}
    state.load = {'r1': NIL, 'r2': NIL}
    state.pos = {'c1': 3, 'o1': 7, 'o2': 7}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:['o1', 'o2']}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1'],
    2: ['fetch', 'r2', 'o2']

}

eventsEnv = {
}