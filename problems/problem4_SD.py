__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from ape import state



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
    'openDoor': 1, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 1,
    'closeDoors': 3,
    'move': 1,
    'take': 1,
    'put': 1,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.EDGES = {
    1: [2],
    2: [1, 3, 4],
    3: [2],
    4: [2, 6],
    5: [6],
    6: [5, 7, 4],
    7: [6]
}
rv.DOORLOCATIONS = {(1, 2): 'd1', (2, 3): 'd2', (2, 4): 'd3', (7, 4): 'd4', (6, 7): 'd5'}
rv.ROBOTS = ['r1', 'r2', 'r3', 'r4']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5']

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed'}
    state.loc = {'r1': 1, 'r2': 4, 'r3': 2, 'r4': 7}
    state.pos = {'o1': 7, 'o2': 5}
    state.done = {0: False}

tasks = {
#    1: ['fetch', 'r1', 'o1', 2],
    1: ['fetch', 'r2', 'o2', 3]
}

eventsEnv = {
    1: [closeDoors, []]
}