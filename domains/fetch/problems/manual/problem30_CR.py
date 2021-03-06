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

 #  1  5  6 
 #   \ | /      
 #    \|/
 #     7
 #     |
 #     |
 #     8
 #    /|\
 #   / | \
 #  2  3  4
 # Tests search with not enough charge and position of object unknown (at location 6)

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}
rv.OBJECTS =  {'o1'}
rv.ROBOTS = {'r1'}

def ResetState():
    state.loc = {'r1': 7}
    state.charge = {'r1':2}
    state.load = {'r1': NIL}
    state.pos = {'c1': 7, 'o1': UNK}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:['o1'], 7:[], 8:[]}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    2: [['search', 'r1', 'o1']]
}

eventsEnv = {
    #3: [RelocateCharger, ['c1', 8]]
}