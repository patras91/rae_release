__author__ = 'mason'
from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

def GetCostOfMove(r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(item):
    return max(1, np.random.beta(2, 2))

def GetCostOfWrap(m, item):
    return max(1, np.random.normal(5, .5))

def GetCostOfPickup(r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfPutdown(r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfLoad(r, m, item):
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
    'repair': 8,
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
    'repair': 8,
    'wait': 1
}

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 14}

rv.GROUND_EDGES = {0: [6, 17, 19, 2, 3, 8, 9, 18, 200], 1: [11, 16], 2: [0, 9], 3: [0, 4, 15, 18, 21], 4: [20, 21, 3, 6, 7, 12], 5: [15, 12], 6: [4, 0, 10], 7: [4, 200], 8: [0], 9: [0, 2, 18, 21, 16], 10: [6], 11: [18, 1, 12, 14, 17, 200], 12: [4, 5, 11], 13: [16, 20, 200], 14: [11, 20], 15: [21, 3, 5, 200], 16: [1, 9, 13, 200], 17: [11, 0], 18: [0, 3, 9, 11], 19: [0], 20: [4, 13, 14, 21], 21: [3, 20, 4, 9, 15], 200: [0, 7, 11, 13, 15, 16]}
rv.GROUND_WEIGHTS = {(0, 6): 10.684694760855374, (0, 17): 1, (0, 19): 9.535662736983143, (0, 2): 5.2398541886043315, (0, 3): 6.726524624705721, (0, 8): 3.2638589153944606, (0, 9): 4.9591946623460945, (0, 18): 9.548934236522285, (0, 200): 7.455049580584654, (1, 11): 10.31429975260227, (1, 16): 2.70243754542627, (2, 9): 9.875156567808263, (3, 4): 10.48929117403036, (3, 15): 12.278276584791453, (3, 18): 8.093280973355634, (3, 21): 12.941681496317042, (4, 20): 4.565895293330177, (4, 21): 3.7627272639308895, (4, 6): 9.092266815424862, (4, 7): 5.187319149170091, (4, 12): 6.115737209692435, (5, 15): 8.82497288390524, (5, 12): 9.278403769461551, (6, 10): 11.875510119779323, (7, 200): 8.988657188477704, (9, 18): 1.7952494326220263, (9, 21): 13.725486607631556, (9, 16): 12.705866110749401, (11, 18): 14.140728763471735, (11, 12): 11.095713206064426, (11, 14): 6.985101669769829, (11, 17): 8.02546068246125, (11, 200): 5.677594955401899, (13, 16): 15.843352558605808, (13, 20): 11.974214020342403, (13, 200): 8.460600015513888, (14, 20): 7.3345957931792425, (15, 21): 7.375884609588601, (15, 200): 3.1438271706954657, (16, 200): 9.072557957354043, (20, 21): 11.90575244463064}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.138852221385532, 'r1': 7.650742570333959, 'r2': 6.520556392467352, 'r3': 12.567257976825108, 'r4': 7.204841682903215, 'r5': 9.699792119585709, 'r6': 9.338353481013128, 'r7': 9.885804136026437, 'r8': 8.184030073082681, 'r9': 7.54315444642756}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19']
rv.OBJ_WEIGHT = {'o0': 9.823104998019247, 'o1': 7.5460957450200326, 'o2': 5.850835253869085, 'o3': 7.407515618786984, 'o4': 9.56270576665308, 'o5': 4.649020579770527, 'o6': 6.5228030419368705, 'o7': 5.118058274274643, 'o8': 9.956241962065189, 'o9': 8.825862309472493, 'o10': 7.426251635931848, 'o11': 6.107080526557564, 'o12': 8.721518143446332, 'o13': 3.556050489596786, 'o14': 6.794188686469185, 'o15': 4.228781468234154, 'o16': 6.023507875607643, 'o17': 6.983909637614552, 'o18': 7.702956563290512, 'o19': 7.690568418433372}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13'], 'type2': ['o14', 'o15', 'o16'], 'type3': ['o17', 'o18', 'o19']}

def ResetState():
    state.loc = { 'r0': 17, 'r1': 17, 'r2': 2, 'r3': 20, 'r4': 8, 'r5': 14, 'r6': 15, 'r7': 12, 'r8': 19, 'r9': 15, 'm0': 4, 'm1': 8, 'm2': 2, 'm3': 17, 'm4': 13, 'm5': 18, 'm6': 13, 'm7': 15, 'fixer0': 6, 'fixer1': 2, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK,}
    state.storedLoc = {'o0': 13, 'o1': 18, 'o2': 9, 'o3': 5, 'o4': 8, 'o5': 6, 'o6': 11, 'o7': 12, 'o8': 8, 'o9': 7, 'o10': 14, 'o11': 0, 'o12': 1, 'o13': 19, 'o14': 1, 'o15': 9, 'o16': 2, 'o17': 11, 'o18': 18, 'o19': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 1, 'm1': 9, 'm2': 9, 'm3': 10, 'm4': 13, 'm5': 13, 'm6': 8, 'm7': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    15: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
}
eventsEnv = {
}