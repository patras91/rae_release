__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

# The domain is as follows:
#_________________________________#
#|       |       |       |        |
#| 1(r1) |   2   | 3(r2) | 7(o1)  |
#|       |       |       |        |
#|--d1---|--d2---|--d3---|---d4---|
#|       |       |       |        |
#|    4      5       6     8(o2)  |
#|_______|_______|_______|________|
# tests w/ unlatch

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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {1: [4], 2: [5], 3: [6], 4: [1, 5], 5: [2, 4, 6], 6: [3, 5, 8], 7: [8], 8: [6, 7]}
rv.DOORLOCATIONS = {(1, 4): 'd1', (2, 5): 'd2', (3, 6): 'd3', (7, 8): 'd4'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4']
rv.DOORTYPES = { 'd1': 'spring', 'd2': 'spring', 'd3': 'spring', 'd4': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed'}
    state.loc = {'r1': 1, 'r2': 3}
    state.pos = {'o1': 7, 'o2': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK}

tasks = {
    5: [['fetch', 'r2', 'o2', 6]]
}

eventsEnv = {
    #1: [closeDoors, []]
}