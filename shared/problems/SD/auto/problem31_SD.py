__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'unlatch1': 5,
    'unlatch2': 5,
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
}

DURATION.COUNTER = {
    'unlatch1': 5,
    'unlatch2': 5,
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
}

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
rv.EDGES = {1: [2, 6], 2: [1, 3], 3: [2, 4, 6, 7], 4: [3, 5, 8], 5: [4, 6], 6: [1, 5, 3], 7: [3, 8], 8: [7, 4]}
rv.DOORLOCATIONS = {(4, 5): 'd1', (1, 6): 'd2', (3, 7): 'd3'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 3, 'r2': 4, 'r3': 7}
    state.pos = {'o1': 2, 'o2': 5, 'o3': 6}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    1: [['fetch', 'r2', 'o1', 7]],
    1: [['fetch', 'r1', 'o2', 6]],
    4: [['moveTo', 'r2', 4]]
}

eventsEnv = {}

