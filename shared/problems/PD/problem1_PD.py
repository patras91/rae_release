__author__ = 'mason'

from domain_packageDelivery import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'lookupDB': 2,
    'moveRobot': 5,
    'wrap': 5,
    'pickup': 4,
    'load': 3,
    'groundShip': 15,
    'acquireRobot': 2,
    'loadMachine': 3
 }

DURATION.COUNTER = {
    'lookupDB': 2,
    'moveRobot': 5,
    'wrap': 3,
    'pickup': 3,
    'load': 5,
    'groundShip': 4,
    'acquireRobot': 2,
    'loadMachine': 5
 }

rv.LOCATIONS = [1, 2, 3, 4]
rv.EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: []}
rv.ROBOTS = {'r1'}
rv.MACHINES = {'m1'}

def ResetState():
    state.loc = {'r1': 1, 'm1': 3, 'o1': UNK}
    state.load = {'r1': NIL}
    state.busy = {'r1': False}
    state.NationalDatabase = {'o1': 2}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    1: ['order', 'o1', 4, 'fast'],
}

eventsEnv = {
}