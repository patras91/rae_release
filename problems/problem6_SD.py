__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from rae1 import state



DURATION.TIME = {
    'openDoor': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

DURATION.COUNTER = {
    'openDoor': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3],
}
rv.DOORLOCATIONS = {(1, 2): 'd2', (1, 3): 'd1', (2, 4): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 2, 'r2': 3}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = False

tasks = {
    1: ['fetch', 'r1', 'o1', 2],
}

eventsEnv = {
    3: [closeDoors, []],
}