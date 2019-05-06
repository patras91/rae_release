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
rv.EDGES = {1: [2, 4], 2: [1, 3], 3: [2, 4, 5], 4: [1, 3, 6], 5: [3], 6: [4]}
rv.DOORLOCATIONS = {(4, 6): 'd1', (3, 5): 'd2', (1, 4): 'd3', (1, 2): 'd4'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring', 'd3': 'ordinary', 'd4': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed'}
    state.loc = {'r1': 4, 'r2': 4}
    state.pos = {'o1': 6, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK}

tasks = {
    2: [['moveTo', 'r1', 6]],
    4: [['moveTo', 'r2', 6]]
}

eventsEnv = {}

