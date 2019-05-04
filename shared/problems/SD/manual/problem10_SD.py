__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

# The domain is as follows:
#_________________________
#|       |       |       |
#|   1   |   2   |3(o1)  |
#|       |       |       |
#|-d1(s)-|-d2(s)-|-------|
#|       |       |       |
#|   4     5(r2)   6(r1) |
#|_______|_______|_______|
# s is for spring
# This problem tests w/ load, w/unlatch, and w/ door knowledge

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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6]
rv.EDGES = {1: [4], 2: [5], 3: [6], 4: [1, 5], 5: [2, 4, 6], 6: [3, 5]}
rv.DOORLOCATIONS = {(1, 4): 'd1', (2, 5): 'd2'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = { 'd1': 'spring', 'd2': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 6, 'r2': 5}
    state.pos = {'o1': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK }

tasks = {
    2: [['fetch', 'r1', 'o1', 5]],
}

eventsEnv = {
    #1: [closeDoors, []]
}