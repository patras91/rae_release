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
rv.EDGES = {1: [2], 2: [1, 3, 4], 3: [2, 5], 4: [2, 6], 5: [3], 6: [4, 7], 7: [6]}
rv.DOORLOCATIONS = {(1, 2): 'd1', (3, 5): 'd2', (2, 3): 'd3', (2, 4): 'd4', (4, 6): 'd5', (6, 7): 'd6'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'ordinary', 'd3': 'ordinary', 'd4': 'ordinary', 'd5': 'spring', 'd6': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed'}
    state.loc = {'r1': 6, 'r2': 3, 'r3': 7}
    state.pos = {'o1': 6, 'o2': 6, 'o3': 7}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK}

tasks = {
    5: [['fetch', 'r3', 'o1', 7]]
}

eventsEnv = {}

