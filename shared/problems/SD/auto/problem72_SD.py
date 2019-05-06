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
rv.EDGES = {1: [2, 3], 2: [1], 3: [1, 4], 4: [3, 5, 6], 5: [4, 8], 6: [4, 7, 8], 7: [6], 8: [6, 5]}
rv.DOORLOCATIONS = {(4, 5): 'd1', (6, 8): 'd2', (1, 3): 'd3', (1, 2): 'd4', (6, 7): 'd5', (4, 6): 'd6', (5, 8): 'd7', (3, 4): 'd8'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'spring', 'd4': 'spring', 'd5': 'ordinary', 'd6': 'spring', 'd7': 'ordinary', 'd8': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed', 'd7': 'closed', 'd8': 'closed'}
    state.loc = {'r1': 6, 'r2': 5}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK, 'd7': UNK, 'd8': UNK}

tasks = {
    1: [['fetch', 'r2', 'o1', 1]],
    1: [['fetch', 'r2', 'o1', 1]],
    2: [['moveTo', 'r1', 5]]
}

eventsEnv = {}

