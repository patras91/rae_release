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
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1, 6, 7], 4: [2, 5], 5: [4, 7, 8], 6: [3], 7: [3, 5], 8: [5]}
rv.DOORLOCATIONS = {(3, 7): 'd1', (3, 6): 'd2', (4, 5): 'd3', (5, 8): 'd4', (5, 7): 'd5'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'ordinary', 'd3': 'ordinary', 'd4': 'ordinary', 'd5': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed'}
    state.loc = {'r1': 2, 'r2': 8, 'r3': 1}
    state.pos = {'o1': 7, 'o2': 3, 'o3': 7}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK}

tasks = {
    5: [['fetch', 'r1', 'o2', 6]]
}

eventsEnv = {}

