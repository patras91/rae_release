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
rv.EDGES = {1: [2, 3], 2: [1, 4, 5], 3: [1, 7], 4: [2, 6], 5: [2], 6: [4, 8], 7: [3], 8: [6]}
rv.DOORLOCATIONS = {(1, 3): 'd1'}
rv.ROBOTS = ['r1', 'r2', 'r3']
rv.DOORS = ['d1']
rv.DOORTYPES = {'d1': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL}
    state.doorStatus = {'d1': 'closed'}
    state.loc = {'r1': 2, 'r2': 1, 'r3': 8}
    state.pos = {'o1': 2, 'o2': 8, 'o3': 4}
    state.done = {0: False}
    state.doorType = {'d1': UNK}

tasks = {
    3: [['moveTo', 'r3', 1]]
}

eventsEnv = {}

