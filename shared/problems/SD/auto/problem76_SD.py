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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.EDGES = {1: [2, 3], 2: [1, 5], 3: [1, 4, 5], 4: [3, 7], 5: [3, 2, 6, 7], 6: [5], 7: [4, 5]}
rv.DOORLOCATIONS = {(2, 5): 'd1', (1, 2): 'd2', (1, 3): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 1, 'r2': 7}
    state.pos = {'o1': 3, 'o2': 5}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    2: [['moveTo', 'r1', 4]],
    2: [['fetch', 'r2', 'o2', 7]],
    2: [['fetch', 'r2', 'o2', 1]]
}

eventsEnv = {}

