__author__ = 'mason'

from domain_orderFulfillment import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'lookupDB': 2,
    'wrap': 5,
    'pickup': 4,
    'putdown': 4,
    'load': 3,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': 3,
    'dummyAction': 1,
    'moveRobot': 1
 }

DURATION.COUNTER = {
    'lookupDB': 2,
    'wrap': 5,
    'pickup': 4,
    'putdown': 4,
    'load': 3,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': 3,
    'dummyAction': 1,
    'moveRobot': 1
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.FACTORY1 = frozenset({1, 2, 3, 4})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5, 7], 5: [4, 6], 6: [5, 7], 7: [4, 6]}
rv.GROUND_WEIGHTS = {(1,2): 1, (2,3): 1, (3,4): 5, (4,5): 15, (4,7): 80, (5,6): 50, (6,7): 10}

rv.ROBOTS = {'r1': rv.FACTORY1, 'r2': rv.FACTORY1}
rv.ROBOT_CAPACITY = {'r1': 3, 'r2': 10}
rv.MACHINES = {'m1': rv.FACTORY1}

rv.OBJECTS = {'o1', 'o2'}
rv.OBJ_WEIGHT = {'o1': 7, '02':2}

def ResetState():
    state.loc = {'r1': 2, 'r2': 1, 'm1': 3, 'o1': UNK, 'o2': UNK}
    state.load = {'r1': NIL, 'r2': NIL}
    state.busy = {'r1': False, 'r2': False, 'm1': False}
    state.NationalDatabase = {'o1': 2, 'o2': 1}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    1: [['order', 'o2', 7]],
    2: [['order', 'o1', 7]],
}

eventsEnv = {
}