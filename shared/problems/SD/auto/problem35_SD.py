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
rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5, 6], 5: [4], 6: [4]}
rv.DOORLOCATIONS = {(4, 5): 'd1', (4, 6): 'd2'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 6, 'r2': 1, 'r3': 1}
    state.pos = {'o1': 2, 'o2': 3, 'o3': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    1: [['moveTo', 'r1', 2]],
    1: [['moveTo', 'r3', 3]]
}

eventsEnv = {}

