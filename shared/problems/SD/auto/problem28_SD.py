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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6]
rv.EDGES = {1: [2, 4], 2: [1, 3], 3: [2, 5], 4: [1], 5: [3, 6], 6: [5]}
rv.DOORLOCATIONS = {(2, 3): 'd1', (1, 2): 'd2', (1, 4): 'd3'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'ordinary', 'd3': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 6, 'r2': 1, 'r3': 6}
    state.pos = {'o1': 6, 'o2': 3, 'o3': 5}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    2: [['moveTo', 'r3', 2]],
    4: [['moveTo', 'r1', 4]]
}

eventsEnv = {}

