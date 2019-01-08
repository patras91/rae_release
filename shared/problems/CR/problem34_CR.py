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
 #         \
 #          \
 #           9----10
 #        
 # Tests fetch with not enough charge and position of object known, robot needs to carry the charger

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rv.EDGES = {1: [7], 2: [8], 3: [8], 4: [8, 9], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7], 9:[4, 10], 10:[9]}
rv.OBJECTS =  {'o1', 'o2'}
rv.ROBOTS = {'r1', 'r2'}

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1':1}
    state.load = {'r1': NIL}
    state.pos = {'c1': 1, 'o1': 10, 'o2': UNK}
    state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:['o1']}
    state.emergencyHandling = {'r1': False, 'r2': False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False

tasks = {
    3: [['fetch', 'r1', 'o1']],
    5: [['emergency', 'r1', 1, 1]],
}

eventsEnv = {
    #3: [RelocateCharger, ['c1', 8]]
}