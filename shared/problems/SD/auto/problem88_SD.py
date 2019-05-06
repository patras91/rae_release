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
rv.EDGES = {1: [2, 3], 2: [1, 4, 7], 3: [1, 5], 4: [2, 6], 5: [3], 6: [4, 7, 8], 7: [2, 6], 8: [6]}
rv.DOORLOCATIONS = {(3, 5): 'd1', (2, 7): 'd2'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 4, 'r2': 4}
    state.pos = {'o1': 1, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    1: [['moveTo', 'r2', 7]],
    1: [['fetch', 'r2', 'o1', 1]]
}

eventsEnv = {}

