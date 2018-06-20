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


rv.LOCATIONS = [1, 2, 3, 4, 5, 6]
rv.EDGES = {
    1: [3],
    2: [3, 5],
    3: [1, 2, 4],
    4: [6, 3],
    5: [2],
    6: [4]
}
rv.DOORLOCATIONS = {(4, 6): 'd2', (2, 5): 'd1', (1, 3): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 5, 'r2': 6}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = {0: False}

tasks = {
    1: ['fetch', 'r1', 'o1', 2],
  #  2: ['fetch', 'r2', 'o2', 3]
}

eventsEnv = {
    1: [closeDoors, []]
}