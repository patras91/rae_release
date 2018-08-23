__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

#_________________________#
#|       |  (r3) |       |        
#| 1(r1)d1   2  d2   3   | 
#|       |       |       |        
#|-------|--d3---|-------|
#        |       |               
#        | 4(r2) |   
# _______|___d4__|________
#|       |       |       |        
#| 5(o2)     6  d5  7(o1)| 
#|       | (r2)  |  (r4) |        
#|_______|_______|_______|
# tests w/ load w/ unlatch

DURATION.TIME = {
    'unlatch1': 5, #for domain SD
    'unlatch2': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

DURATION.COUNTER = {
    'unlatch1': 5, #for domain SD
    'unlatch2': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.EDGES = {
    1: [2],
    2: [1, 3, 4],
    3: [2],
    4: [2, 6],
    5: [6],
    6: [5, 7, 4],
    7: [6]
}
rv.DOORLOCATIONS = {(1, 2): 'd1', (2, 3): 'd2', (2, 4): 'd3', (7, 4): 'd4', (6, 7): 'd5'}
rv.ROBOTS = ['r1', 'r2', 'r3', 'r4']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5']
rv.DOORTYPES = { 'd1': 'spring', 'd2': 'spring', 'd3': 'spring', 'd4': 'spring', 'd5': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed'}
    state.loc = {'r1': 1, 'r2': 4, 'r3': 2, 'r4': 7}
    state.pos = {'o1': 7, 'o2': 5}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK}

tasks = {
    1: ['fetch', 'r4', 'o1', 5]
}

eventsEnv = {
    #1: [closeDoors, []]
}