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

rv.LOCATIONS = [1, 2, 3, 4, 5]
rv.EDGES = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2, 5], 5: [4]}
rv.DOORLOCATIONS = {(4, 5): 'd1', (2, 4): 'd2'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1', 'd2']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed'}
    state.loc = {'r1': 1, 'r2': 1, 'r3': 5}
    state.pos = {'o1': 1, 'o2': 4, 'o3': 3}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK}

tasks = {
    4: [['moveTo', 'r3', 3]],
    2: [['moveTo', 'r3', 1]],
    3: [['moveTo', 'r1', 4]]
}

eventsEnv = {}

