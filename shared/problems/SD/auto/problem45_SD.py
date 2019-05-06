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
rv.EDGES = {1: [2, 3], 2: [1, 5], 3: [1, 4], 4: [3, 7], 5: [2, 6], 6: [5], 7: [4]}
rv.DOORLOCATIONS = {(1, 3): 'd1', (5, 6): 'd2', (2, 5): 'd3', (4, 7): 'd4', (1, 2): 'd5'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'spring', 'd4': 'ordinary', 'd5': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed'}
    state.loc = {'r1': 5, 'r2': 5}
    state.pos = {'o1': 1, 'o2': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK}

tasks = {
    5: [['fetch', 'r1', 'o1', 4]],
    2: [['fetch', 'r1', 'o2', 5]],
    4: [['fetch', 'r1', 'o1', 2]]
}

eventsEnv = {}

