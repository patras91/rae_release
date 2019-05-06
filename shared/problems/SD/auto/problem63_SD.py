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
rv.EDGES = {1: [2], 2: [1, 3, 4], 3: [2, 6], 4: [2, 5], 5: [4, 7], 6: [3], 7: [5, 8], 8: [7]}
rv.DOORLOCATIONS = {(2, 4): 'd1', (2, 3): 'd2', (4, 5): 'd3', (1, 2): 'd4'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'spring', 'd4': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed'}
    state.loc = {'r1': 7, 'r2': 3}
    state.pos = {'o1': 1, 'o2': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK}

tasks = {
    1: [['fetch', 'r1', 'o1', 2]]
}

eventsEnv = {}

