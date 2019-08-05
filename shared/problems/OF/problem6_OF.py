__author__ = 'mason'

'''
Situation: choose which object to pick up, which robot to use, based on location
'''

from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np


def GetCostOfMove(id, r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(id, item):
    return max(1, np.random.beta(2, 2))


def GetCostOfWrap(id, orderName, m, item):
    return max(1, np.random.normal(5, .5))


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


rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
rv.FACTORY1 = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 9})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {1: [2], 2: [1, 3], 3: [2, 4, 8], 4: [3, 5], 5: [4, 6], 6: [5, 7], 7: [6],
                   8: [3,9], 9: [8]}
rv.GROUND_WEIGHTS = {(1,2): 1, (2,3): 1, (3,4): 5, (3,8): 4, (4,5): 15, (5,6): 50, (6,7): 10, (8,9): 5}

rv.ROBOTS = {'r1': rv.FACTORY1, 'r2': rv.FACTORY1}
rv.ROBOT_CAPACITY = {'r1': 9, 'r2': 10}
rv.MACHINES = {'m1': rv.FACTORY1}

rv.PALLETS = {'p1'}



def ResetState():
    state.OBJECTS = {'o1': True, 'o2': True}
    state.OBJ_WEIGHT = {'o1': 7, 'o2': 7}
    state.OBJ_CLASS = {'type1': ['o1', 'o2']}

    state.loc = {'r1': 8, 'r2': 1, 'm1': 3, 'o1': 2, 'o2': 3,}
    state.load = {'r1': NIL, 'r2': NIL,}
    state.busy = {'r1': False, 'r2': False, 'm1': False,}
    state.numUses = {'m1': 1}
    state.var1 = {'temp': 'r1', 'temp1': 'r1', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}


tasks = {
    1: [['orderStart', ['type1']]],
}

eventsEnv = {
}