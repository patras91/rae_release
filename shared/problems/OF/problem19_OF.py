__author__ = 'mason'
from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

def GetCostOfMove(id, r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(id, item):
    return max(1, np.random.beta(2, 2))

def GetCostOfWrap(id, m, item):
    return max(1, np.random.normal(5, .5))

def GetCostOfPickup(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfPutdown(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfLoad(id, r, m, item):
    return max(1, np.random.normal(3, .5))

DURATION.TIME = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'repair': 5,
    'wait': 1
}

DURATION.COUNTER = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'repair': 5,
    'wait': 1
}

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1}

rv.GROUND_EDGES = {0: [12, 1, 2, 5, 6, 8, 11, 13, 15], 1: [0, 4, 9], 2: [0, 9], 3: [4], 4: [3, 14, 1, 7], 5: [0], 6: [0, 12, 16], 7: [4, 11], 8: [0, 200], 9: [2, 11, 1], 10: [12], 11: [0, 7, 9, 200], 12: [0, 6, 13, 10], 13: [0, 12, 14], 14: [13, 4, 200], 15: [0], 16: [6], 200: [8, 11, 14]}
rv.GROUND_WEIGHTS = {(0, 12): 9.599762038837014, (0, 1): 12.034208508320457, (0, 2): 8.410984398045002, (0, 5): 11.972436886854382, (0, 6): 16.18272758373579, (0, 8): 6.5873726408017275, (0, 11): 10.447276990560342, (0, 13): 7.160037269440641, (0, 15): 3.5485420403391954, (1, 4): 10.948154653322426, (1, 9): 9.634272494065428, (2, 9): 10.995436154565091, (3, 4): 3.8619925937563595, (4, 14): 8.555748261306809, (4, 7): 18.232052503268243, (6, 12): 1, (6, 16): 5.052460036113978, (7, 11): 10.245812243331795, (8, 200): 3.1418469426492805, (9, 11): 12.906955408516815, (10, 12): 7.499519711780797, (11, 200): 10.17059236515908, (12, 13): 10.938171888473754, (13, 14): 5.068672186902813, (14, 200): 12.60599818338044}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.356972728881884, 'r1': 8.154892257418613, 'r2': 11.051422060149045, 'r3': 4.999875901003659, 'r4': 11.230356424792811, 'r5': 7.5144515151619835, 'r6': 9.575230975924393, 'r7': 9.20445712077529}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 8.510914267103988, 'o1': 9.351465891649525, 'o2': 3.654450376612638, 'o3': 3.6013829801766786, 'o4': 7.846133180449132, 'o5': 6.903848067245053, 'o6': 4.525283476486873, 'o7': 7.424899622315078, 'o8': 7.066432529668013, 'o9': 7.743967479129639, 'o10': 7.56537370916891, 'o11': 7.590123535254684, 'o12': 7.553621807805415, 'o13': 5.715979198733492, 'o14': 8.067415520824847, 'o15': 6.129523140434537, 'o16': 4.308221469450086, 'o17': 5.980132537232045, 'o18': 7.609985834937499}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15', 'o16', 'o17', 'o18']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 12, 'r2': 6, 'r3': 13, 'r4': 15, 'r5': 15, 'r6': 13, 'r7': 9, 'm0': 14, 'm1': 8, 'm2': 16, 'm3': 15, 'm4': 10, 'm5': 8, 'm6': 10, 'm7': 7, 'fixer0': 10, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK,}
    state.storedLoc = {'o0': 12, 'o1': 0, 'o2': 1, 'o3': 12, 'o4': 4, 'o5': 7, 'o6': 14, 'o7': 5, 'o8': 12, 'o9': 14, 'o10': 13, 'o11': 10, 'o12': 10, 'o13': 13, 'o14': 12, 'o15': 8, 'o16': 14, 'o17': 14, 'o18': 0}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False}
    state.numUses = {'m0': 8, 'm1': 11, 'm2': 13, 'm3': 5, 'm4': 14, 'm5': 9, 'm6': 4, 'm7': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    7: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
}
eventsEnv = {
}