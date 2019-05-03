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
rv.EDGES = {1: [2, 4], 2: [1, 3], 3: [2, 4, 5, 6], 4: [1, 3], 5: [3, 7], 6: [3, 7], 7: [6, 5]}
rv.DOORLOCATIONS = {(6, 7): 'd1', (5, 7): 'd2', (3, 4): 'd8', (1, 4): 'd7', (3, 6): 'd6'}
rv.ROBOTS = ['r1']
rv.DOORS = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
rv.DOORTYPES = {'d1': 'ordinary', 'd2': 'spring', 'd3': 'spring', 'd4': 'ordinary', 'd5': 'ordinary', 'd6': 'spring', 'd7': 'spring', 'd8': 'ordinary'}

def ResetState():
    state.load = {'r1': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed', 'd4': 'closed', 'd5': 'closed', 'd6': 'closed', 'd7': 'closed', 'd8': 'closed'}
    state.loc = {'r1': 7}
    state.pos = {'o1': 2}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK, 'd4': UNK, 'd5': UNK, 'd6': UNK, 'd7': UNK, 'd8': UNK}

tasks = {
    5: [['moveTo', 'r1', 2]]
}

eventsEnv = {}

