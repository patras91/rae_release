__author__ = 'patras'

from domain_chargeableRobot import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5,
    'moveToEmergency': 10,
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
    'moveToEmergency': 10,
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
rv.OBJECTS =  {'o1', 'o2'}
rv.ROBOTS = {'r1', 'r2'}

def ResetState():
    state.loc = {'r1': 1, 'r2': 6}
    state.charge = {'r1': 2, 'r2': 2}
    state.load = {'r1': NIL, 'r2': 'o3'}
    state.pos = {'c1': 4, 'o1': 7, 'o2': 8, 'o3': 'r2'}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:['o1'], 8:['o2']}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    3: [['fetch', 'r1', 'o1']],
    5: [['fetch', 'r2', 'o2']]

}

eventsEnv = {
}