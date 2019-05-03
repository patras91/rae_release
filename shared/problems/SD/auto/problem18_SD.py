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
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1, 5], 4: [2, 6], 5: [3], 6: [4]}
rv.DOORLOCATIONS = {(3, 5): 'd1'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1']
rv.DOORTYPES = {'d1': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed'}
    state.loc = {'r1': 1, 'r2': 6, 'r3': 5}
    state.pos = {'o1': 5, 'o2': 6, 'o3': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK}

tasks = {
    1: [['fetch', 'r1', 'o1', 1]]
}

eventsEnv = {}

