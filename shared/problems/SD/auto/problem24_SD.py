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
rv.EDGES = {1: [2], 2: [1, 3, 8], 3: [2, 4, 5], 4: [3, 6], 5: [3, 6, 7], 6: [5, 4], 7: [5], 8: [2]}
rv.DOORLOCATIONS = {(1, 2): 'd1', (5, 6): 'd2', (3, 4): 'd3', (5, 7): 'd4', (4, 6): 'd5', (2, 8): 'd6', (2, 3): 'd7'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring', 'd3': 'ordinary', 'd4': 'spring', 'd5': 'ordinary', 'd6': 'ordinary', 'd7': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed', 'd7': 'closed'}
    state.loc = {'r1': 2, 'r2': 1, 'r3': 1}
    state.pos = {'o1': 8, 'o2': 6, 'o3': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK, 'd7': UNK}

tasks = {
    2: [['moveTo', 'r3', 7]]
}

eventsEnv = {}

