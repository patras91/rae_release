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
    'moveToEmergency': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5
 }

DURATION.COUNTER = {
    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveToEmergency': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5,
 }

 #  1  2   
 #   \ |      
 #    \|
 #     3
 #     |
 #     |
 #     4
 # Tests search when there is enough charge with o1 in location 2

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [3], 2: [3], 3: [1, 2, 4], 4: [3]}
rv.OBJECTS =  {'o1'}
rv.ROBOTS = {'r1'}

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1':10}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': UNK}
    state.containers = {1:[], 2:['o1'], 3:[], 4:[]}
    state.emergencyHandling = {'r1': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    3: [['search', 'r1', 'o1']]
}

eventsEnv = {
    #3: [RelocateCharger, ['c1', 8]]
}