__author__ = 'mason'

from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

'''
One robot, multiple machines, increased wrapping time

Same as problem 5 but multiple machines, increased wrapping
'''


def GetCostOfMove(id, r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(id, item):
    return max(1, np.random.beta(2, 2))


def GetCostOfWrap(id, orderName, m, item):
    return max(1, np.random.normal(10, .5))


def GetCostOfPickup(id, r, item):
    return max(1, np.random.normal(4, 1))


def GetCostOfPutdown(id, r, item):
    return max(1, np.random.normal(4, 1))


def GetCostOfLoad(id, orderName, r, m, item):
    return max(1, np.random.normal(3, .5))



DURATION.TIME = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'acquireRobot': 1,
    'freeRobot': 1,
    'wait': 5
 }

DURATION.COUNTER = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'acquireRobot': 1,
    'freeRobot': 1,
    'wait': 5
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7]
rv.FACTORY1 = frozenset({1, 2, 3, 4, 5, 6, 7})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5, 7], 7: [6]}
rv.GROUND_WEIGHTS = {(1,2): 1, (2,3): 1, (3,4): 5, (4,5): 8, (5,6): 5, (6,7): 1}

rv.ROBOTS = {'r1': rv.FACTORY1}
rv.ROBOT_CAPACITY = {'r1': 10}
rv.MACHINES = {'m1': rv.FACTORY1, 'm2': rv.FACTORY1}

rv.PALLETS = {'p1'}



def ResetState():
    state.OBJECTS = {'o1': True, 'o2': True, 'o3': True, 'o4': True, 'o5': True}
    state.OBJ_WEIGHT = {'o1': 7, 'o2': 3, 'o3': 1, 'o4': 6, 'o5': 3}
    state.OBJ_CLASS = {'type1': ['o1', 'o4'], 'type2': ['o2', 'o3', 'o5']}

    state.loc = {'r1': 2, 'r2': 1, 'm1': 3, 'm2': 3, 'o1': 2, 'o2': 1, 'o3':7, 'o4': 1, 'o5': 6, 'p1': 4}
    state.load = {'r1': NIL,}
    state.busy = {'r1': False, 'm1': False, 'm2': False}
    state.numUses = {'m1': 1, 'm2': 20}
    state.var1 = {'temp': 'r1', 'temp1': 'r1', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}


tasks = {
    1: [['orderStart', ['type1', 'type2']]],
    2: [['orderStart', ['type2', 'type1']]],
}

eventsEnv = {
}