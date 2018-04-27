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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {
    1: [2],
    2: [1, 3, 5],
    3: [2, 4],
    4: [3, 5, 6],
    5: [2, 4, 7, 8],
    6: [4],
    7: [5, 8],
    8: [5, 7]
}

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1': 3}
    state.load = {'r1': NIL}
    state.pos = {'c1': 4, 'o1': UNK, 'o2': UNK}
    state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:[], 6:[], 7:['o1'], 8:[]}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1']

}

eventsEnv = {
}