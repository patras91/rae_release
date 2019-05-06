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
rv.EDGES = {1: [2, 6], 2: [1, 3, 4], 3: [2], 4: [2, 5], 5: [4], 6: [1]}
rv.DOORLOCATIONS = {(4, 5): 'd1', (2, 3): 'd2'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 5, 'r2': 2}
    state.pos = {'o1': 4, 'o2': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    4: [['fetch', 'r1', 'o1', 4]],
    2: [['fetch', 'r2', 'o2', 5]]
}

eventsEnv = {}

