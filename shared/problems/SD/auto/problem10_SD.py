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
rv.EDGES = {1: [2], 2: [1, 3, 8], 3: [2, 4, 5, 6], 4: [3], 5: [3, 7], 6: [3, 8], 7: [5], 8: [6, 2]}
rv.DOORLOCATIONS = {(5, 7): 'd1'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1']
rv.DOORTYPES = {'d1': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed'}
    state.loc = {'r1': 2, 'r2': 7}
    state.pos = {'o1': 3, 'o2': 5}
    state.done = {0: False}
    state.doorType = {'d1': UNK}

tasks = {
    1: [['fetch', 'r2', 'o1', 1]],
    1: [['fetch', 'r1', 'o2', 6]]
}

eventsEnv = {}

