__author__ = 'patras'

from domain_chargeableRobot import *
from timer import DURATION
from ape import state

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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
rv.EDGES = {
    1: [3],
    2: [3, 9],
    3: [1, 2, 4, 5],
    4: [3, 6],
    5: [3, 6],
    6: [4, 5, 7, 8],
    7: [6],
    8: [6],
    9: [2]
}

def ResetState():
    state.loc = {'r1': 3, 'r2': 6}
    state.charge = {'r1': 2, 'r2': 3}
    state.load = {'r1': NIL, 'r2': NIL}
    state.pos = {'c1': 3, 'o1': UNK, 'o2': UNK}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:['o1'], 9: ['o2']}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1'],
    2: ['fetch', 'r2', 'o2'],
    3: ['emergency', 'r1', 5, 1]

}

eventsEnv = {
}