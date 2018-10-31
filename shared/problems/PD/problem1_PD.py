__author__ = 'mason'

from domain_packageDelivery import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'lookupDB': 2,
    'move': 5,
    'wrap': 5,
    'pickup': 4,
    'load': 3,
    'groundShip': 15
 }

DURATION.COUNTER = {
    'lookupDB': 2,
    'move': 5,
    'wrap': 3,
    'pickup': 3,
    'load': 5,
    'groundShip': 4
 }

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [2], 2: [3], 3: [4], 4: []}
rv.ROBOTS = {'r1'}
rv.MACHINES = {'m1'}

def ResetState():
    state.loc = {'r1': 1, 'm1': 3}
    state.load = {'r1': NIL}
    state.pos = {'c1': 7, 'o1': UNK, 'o2': UNK}
    state.busy = {'r1': False}
    state.NationalDatabase = {'o1': 2}

tasks = {
    1: ['order', 'o1', 4, 'fast'],
}

eventsEnv = {
}