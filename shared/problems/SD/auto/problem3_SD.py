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
rv.EDGES = {1: [2, 3], 2: [1, 4, 6], 3: [1, 5], 4: [2, 7, 8], 5: [3, 7], 6: [2], 7: [4, 5], 8: [4]}
rv.DOORLOCATIONS = {(1, 3): 'd1', (2, 6): 'd2'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 8, 'r2': 1, 'r3': 7}
    state.pos = {'o1': 2, 'o2': 7, 'o3': 8}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    3: [['fetch', 'r1', 'o2', 3]],
    1: [['moveTo', 'r2', 4]]
}

eventsEnv = {}

