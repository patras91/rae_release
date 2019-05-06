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
rv.EDGES = {1: [2, 5], 2: [1, 3, 4], 3: [2, 6], 4: [2, 6], 5: [1, 8], 6: [3, 4, 7], 7: [6], 8: [5]}
rv.DOORLOCATIONS = {(2, 3): 'd1', (3, 6): 'd2', (5, 8): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 2, 'r2': 2}
    state.pos = {'o1': 5, 'o2': 4}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    1: [['fetch', 'r1', 'o2', 7]]
}

eventsEnv = {}

