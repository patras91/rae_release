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
rv.EDGES = {1: [2, 4], 2: [1, 3, 5], 3: [2], 4: [1, 5, 6], 5: [2, 4, 7], 6: [4, 7], 7: [6, 5, 8], 8: [7]}
rv.DOORLOCATIONS = {(5, 7): 'd1', (6, 7): 'd4', (1, 2): 'd8', (4, 6): 'd5', (1, 4): 'd6', (7, 8): 'd7'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'ordinary', 'd4': 'spring', 'd5': 'spring', 'd6': 'spring', 'd7': 'ordinary', 'd8': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed', 'd7': 'closed', 'd8': 'closed'}
    state.loc = {'r1': 1, 'r2': 2, 'r3': 1}
    state.pos = {'o1': 6, 'o2': 3, 'o3': 7}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK, 'd7': UNK, 'd8': UNK}

tasks = {
    1: [['fetch', 'r1', 'o3', 6]],
    3: [['moveTo', 'r3', 8]]
}

eventsEnv = {}

