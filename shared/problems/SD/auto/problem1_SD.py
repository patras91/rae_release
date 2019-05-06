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
rv.EDGES = {1: [2, 7], 2: [1, 3, 6], 3: [2, 4, 5, 7], 4: [3, 8], 5: [3], 6: [2], 7: [1, 3], 8: [4]}
rv.DOORLOCATIONS = {(1, 2): 'd1', (3, 7): 'd2'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'spring', 'd2': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 4, 'r2': 5, 'r3': 7}
    state.pos = {'o1': 5, 'o2': 5, 'o3': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    2: [['fetch', 'r1', 'o1', 8]]
}

eventsEnv = {}

