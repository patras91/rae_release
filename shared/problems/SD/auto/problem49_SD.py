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
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1, 6, 7], 4: [2, 5], 5: [4], 6: [3], 7: [3, 8], 8: [7]}
rv.DOORLOCATIONS = {(2, 4): 'd1', (1, 3): 'd2', (7, 8): 'd3', (3, 7): 'd4', (4, 5): 'd5', (1, 2): 'd6', (3, 6): 'd7'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'spring', 'd3': 'spring', 'd4': 'ordinary', 'd5': 'ordinary', 'd6': 'ordinary', 'd7': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed', 'd7': 'closed'}
    state.loc = {'r1': 4, 'r2': 3}
    state.pos = {'o1': 6, 'o2': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK, 'd7': UNK}

tasks = {
    2: [['fetch', 'r1', 'o1', 2]]
}

eventsEnv = {}

