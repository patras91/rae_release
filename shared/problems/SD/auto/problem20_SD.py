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

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [2, 3], 2: [1], 3: [1, 4], 4: [3]}
rv.DOORLOCATIONS = {(1, 3): 'd1', (1, 2): 'd2'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 3, 'r2': 4}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    4: [['moveTo', 'r2', 4]],
    3: [['moveTo', 'r2', 2]]
}

eventsEnv = {}

