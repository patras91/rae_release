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
rv.EDGES = {1: [2, 3], 2: [1, 5, 6], 3: [1, 4], 4: [3, 7], 5: [2], 6: [2, 8], 7: [4], 8: [6]}
rv.DOORLOCATIONS = {(2, 6): 'd1', (1, 2): 'd2', (2, 5): 'd3', (4, 7): 'd4', (1, 3): 'd5', (6, 8): 'd6'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring', 'd3': 'spring', 'd4': 'spring', 'd5': 'ordinary', 'd6': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed'}
    state.loc = {'r1': 8, 'r2': 3, 'r3': 7}
    state.pos = {'o1': 3, 'o2': 4, 'o3': 5}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK}

tasks = {
    2: [['fetch', 'r1', 'o2', 1]]
}

eventsEnv = {}

