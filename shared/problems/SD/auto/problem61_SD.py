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
rv.EDGES = {1: [2, 4], 2: [1, 3, 5], 3: [2], 4: [1], 5: [2, 6], 6: [5, 7], 7: [6]}
rv.DOORLOCATIONS = {(1, 2): 'd1', (5, 6): 'd2', (6, 7): 'd3'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 6, 'r2': 3, 'r3': 2}
    state.pos = {'o1': 6, 'o2': 1, 'o3': 7}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    1: [['moveTo', 'r1', 2]],
    4: [['fetch', 'r1', 'o2', 3]],
    2: [['fetch', 'r3', 'o2', 4]]
}

eventsEnv = {}

