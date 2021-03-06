__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state, rv

DURATION.TIME = {
    'unlatch1': 5,
    'unlatch2': 5,
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 7,
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
    'move': 7,
    'take': 2,
    'put': 2,
}

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]}
rv.DOORS = ['d1', 'd2']
rv.DOORLOCATIONS = {(3, 4): 'd1', (1, 2): 'd2'}
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring'}
rv.ROBOTS = ['r1', 'r2', 'r3', 'r4']

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL}
    state.status = {'r1': 'free', 'r2': 'free', 'r3': 'free', 'r4': 'free'}
    state.loc = {'r1': 1, 'r2': 2, 'r3': 3, 'r4': 2}
    state.pos = {'o1': 2}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', }
    state.doorType = {'d1': UNK, 'd2': UNK, }

tasks = {
    1: [['fetch', 'r1', 'o1', 2]],
}
eventsEnv = {
}