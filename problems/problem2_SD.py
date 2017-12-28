__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from rae1 import state

# The domain is as follows:
#_________________________________#
#|       |       |       |        |
#|   1   |   2   |   3   |   7    |
#|       |       |       |        |
#|--d1---|--d2---|--d3---|---d4---|
#|       |       |       |        |
#|   4       5       6        8   |
#|_______|_______|_______|________|


DURATION.TIME = {
    'openDoor': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

DURATION.COUNTER = {
    'openDoor': 5, #for domain SD
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

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed'}
    state.loc = {'r1': 1, 'r2': 4}
    state.pos = {'o1': 7, 'o2': 2}
    state.done = False

tasks = {
    1: ['fetch', 'r1', 'o1', 5],
    2: ['fetch', 'r2', 'o2', 8]
}

eventsEnv = {
    1: [closeDoors, []]
}