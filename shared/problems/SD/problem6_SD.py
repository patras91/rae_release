__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

#_________________
#|  (o2) |       |       
#|   1   |   2   |
#|       |       |       
#|-d1(s)-|-d2(s)-|
#|       |       |       
#|   3     4(o1) |
#|__(r2)_|__(r1)_|
# tests w/ load, w/ knowledge, w/ unlatch

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


rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3],
}
rv.DOORLOCATIONS = {(1, 2): 'd2', (1, 3): 'd1', (2, 4): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = { 'd1': 'spring', 'd2': 'spring', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 4, 'r2': 3}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    1: ['moveTo', 'r2', 1],
    2: ['fetch', 'r1', 'o1', 1]
}

eventsEnv = {
    #3: [closeDoors, []],
}