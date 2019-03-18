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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 12}

rv.GROUND_EDGES = {0: [1, 16, 8, 200], 1: [2, 13, 0, 4, 6, 15, 16], 2: [14, 1, 11], 3: [10, 20, 11, 17], 4: [1, 16, 17, 5, 12], 5: [4, 6, 21], 6: [1, 19, 5, 8, 14], 7: [9, 11, 13, 19, 16], 8: [0, 6, 21], 9: [14, 19, 7], 10: [16, 3], 11: [2, 3, 7, 14, 18, 19], 12: [4, 13, 200], 13: [18, 1, 7, 12], 14: [2, 6, 11, 21, 9, 20], 15: [1, 16], 16: [1, 4, 7, 0, 10, 15], 17: [3, 4], 18: [11, 13, 19], 19: [7, 11, 18, 6, 9], 20: [14, 3, 21], 21: [5, 20, 8, 14], 200: [0, 12]}
rv.GROUND_WEIGHTS = {(0, 1): 10.065836755001511, (0, 16): 7.851556754328792, (0, 8): 15.023294651522384, (0, 200): 9.9279829452951, (1, 2): 10.764509103838844, (1, 13): 10.314413386683139, (1, 4): 9.025957561510154, (1, 6): 9.221130064055389, (1, 15): 1, (1, 16): 9.287399172441146, (2, 14): 7.076552286392532, (2, 11): 4.887993355922128, (3, 10): 7.9331163375148375, (3, 20): 12.513005000039776, (3, 11): 12.758504677179356, (3, 17): 1.5889735345262164, (4, 16): 2.040612678953906, (4, 17): 10.674987157857819, (4, 5): 8.128863282500287, (4, 12): 6.410690412053497, (5, 6): 8.254861449138552, (5, 21): 8.988477579052667, (6, 19): 5.817828793672975, (6, 8): 12.227888355476503, (6, 14): 3.3236275039343735, (7, 9): 13.896415665126739, (7, 11): 6.814687699245715, (7, 13): 6.692149265531029, (7, 19): 4.66320613883814, (7, 16): 10.542911525558338, (8, 21): 8.888240074775082, (9, 14): 9.033156679777647, (9, 19): 10.586462571920286, (10, 16): 9.892105355426919, (11, 14): 1, (11, 18): 1.5561848947073402, (11, 19): 12.443325768405316, (12, 13): 8.35651532279384, (12, 200): 13.96141384616197, (13, 18): 8.362480503311009, (14, 21): 2.84966014759664, (14, 20): 2.446588976023242, (15, 16): 5.569099809253283, (18, 19): 7.142737653914103, (20, 21): 10.466603390936097}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 9.964072939274615, 'r1': 6.890644907517011, 'r2': 4.299452436757143, 'r3': 11.920342912361829, 'r4': 7.506445872347021, 'r5': 6.636347427193917, 'r6': 5.894364468230615, 'r7': 9.004428319018652}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
rv.OBJ_WEIGHT = {'o0': 6.418325950650936, 'o1': 10.03649325672478, 'o2': 6.43705359804444, 'o3': 10.785457729931887, 'o4': 5.126015745732529, 'o5': 5.967234149065465, 'o6': 7.206028932428506, 'o7': 7.209312419697645, 'o8': 7.359904939393201, 'o9': 7.259889243063012, 'o10': 8.666796830648188, 'o11': 2.667965352058985, 'o12': 8.812185580391828, 'o13': 8.618239682413721, 'o14': 9.820291749301848}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7'], 'type1': ['o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14']}

def ResetState():
    state.loc = { 'r0': 3, 'r1': 0, 'r2': 20, 'r3': 5, 'r4': 10, 'r5': 4, 'r6': 21, 'r7': 4, 'm0': 16, 'fixer0': 4, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK,}
    state.storedLoc = {'o0': 18, 'o1': 8, 'o2': 4, 'o3': 21, 'o4': 13, 'o5': 7, 'o6': 20, 'o7': 19, 'o8': 4, 'o9': 20, 'o10': 18, 'o11': 17, 'o12': 12, 'o13': 4, 'o14': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 5}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    8: [['order', 'type0', 200]],
    6: [['order', 'type0', 200]],
}
eventsEnv = {
}