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
 }

DURATION.COUNTER = {
    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1':1}
    state.load = {'r1': NIL}
    state.pos = {'c1': 7, 'o1': UNK, 'o2': UNK}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:['o2'], 7:[], 8:['o1']}

    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1'],
    2: ['fetch', 'r1', 'o2'],

}

eventsEnv = {
    3: [RelocateCharger, ['c1', 8]]
}