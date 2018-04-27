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
    'put': 1, #for domain CR
    'take': 1,
    'perceive': 1,
    'charge': 1,
    'move': 1,
    'moveCharger': 1,
    'addressEmergency': 1,
    'wait': 1,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1':1}
    state.load = {'r1': NIL}
    state.pos = {'c1': 7, 'o1': 5, 'o2': 2}
    state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:['o1'], 6:[], 7:[], 8:[]}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1'],
    #2: ['fetch', 'r1', 'o2'],

}

eventsEnv = {
    #3: [RelocateCharger, ['c1', 8]]
}