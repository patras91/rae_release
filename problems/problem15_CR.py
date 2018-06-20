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
rv.EDGES = {
    1: [3],
    2: [3],
    3: [1, 2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [7]
}
rv.OBJECTS =  {'o1', 'o2'}
InitProb()

def ResetState():
    state.loc = {'r1': 2}
    state.charge = {'r1':2}
    state.load = {'r1': NIL}
    state.pos = {'c1': 3, 'o1': 8, 'o2': 2}
    state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:[], 6:[], 7:[], 8:['o1']}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    1: ['fetch', 'r1', 'o1']

}

eventsEnv = {
}