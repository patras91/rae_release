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

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1, 5, 7], 4: [2], 5: [3, 6], 6: [5], 7: [3]}
rv.DOORLOCATIONS = {(2, 4): 'd1', (1, 3): 'd2', (3, 7): 'd3', (5, 6): 'd4', (1, 2): 'd5'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'ordinary', 'd3': 'ordinary', 'd4': 'spring', 'd5': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed'}
    state.loc = {'r1': 3, 'r2': 3}
    state.pos = {'o1': 6, 'o2': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK}

tasks = {
    1: [['moveTo', 'r1', 2]],
    2: [['moveTo', 'r2', 7]]
}

eventsEnv = {}

