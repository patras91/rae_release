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

rv.LOCATIONS = [1, 2, 3, 4, 5]
rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}
rv.DOORLOCATIONS = {(1, 2): 'd1'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1']
rv.DOORTYPES = {'d1': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed'}
    state.loc = {'r1': 4, 'r2': 3, 'r3': 4}
    state.pos = {'o1': 1, 'o2': 2, 'o3': 4}
    state.done = {0: False}
    state.doorType = {'d1': UNK}

tasks = {
    1: [['fetch', 'r1', 'o3', 4]],
    3: [['moveTo', 'r3', 5]]
}

eventsEnv = {}

