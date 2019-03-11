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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [8, 16, 1, 3], 1: [0, 2, 10, 13, 14], 2: [1, 9, 12, 5], 3: [0, 7, 8], 4: [11, 10], 5: [2, 6, 13, 7, 15, 16], 6: [12, 5], 7: [3, 5, 15, 14], 8: [3, 15, 0], 9: [15, 2, 12, 13], 10: [1, 4, 12, 13, 14], 11: [12, 4], 12: [9, 10, 2, 6, 11, 200], 13: [1, 9, 16, 5, 10, 15], 14: [1, 7, 10, 15], 15: [5, 13, 14, 7, 8, 9], 16: [5, 0, 13], 200: [12]}
rv.GROUND_WEIGHTS = {(0, 8): 12.66630119282469, (0, 16): 5.54699273813743, (0, 1): 4.6158279446497, (0, 3): 1, (1, 2): 9.19290700985111, (1, 10): 1, (1, 13): 13.060758953779654, (1, 14): 12.107687561851634, (2, 9): 10.713251819588923, (2, 12): 7.9783739905972695, (2, 5): 3.669822490392052, (3, 7): 10.919237803174052, (3, 8): 12.689876814650681, (4, 11): 12.448413512069752, (4, 10): 11.622627210599376, (5, 6): 7.879484317928433, (5, 13): 3.081981321873023, (5, 7): 10.776283693795797, (5, 15): 8.077081347583436, (5, 16): 12.904053384028021, (6, 12): 8.076121064130795, (7, 15): 6.788583714123112, (7, 14): 8.157064469217403, (8, 15): 11.29240668996922, (9, 15): 12.215260816983152, (9, 12): 5.2685347200341806, (9, 13): 8.582253069518048, (10, 12): 5.0688913882958895, (10, 13): 7.320165173857454, (10, 14): 5.081531143751981, (11, 12): 12.91972035640799, (12, 200): 3.8019894354243977, (13, 16): 5.443982853478245, (13, 15): 7.743396438108937, (14, 15): 5.303914268981885}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 12.513073818770827, 'r1': 10.362804428721294, 'r2': 7.012873837263764, 'r3': 7.832392173043945, 'r4': 8.94668096597994, 'r5': 10.287452354584776, 'r6': 9.0108655187364, 'r7': 5.014142771898371}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']
rv.OBJ_WEIGHT = {'o0': 6.9420792150174195, 'o1': 7.251302548995293, 'o2': 9.16570431391587, 'o3': 6.912244919063797, 'o4': 8.98584669404988, 'o5': 2.897351353414521, 'o6': 9.711130826692553, 'o7': 6.922232697632312, 'o8': 6.832072105689597, 'o9': 8.974537777404068, 'o10': 6.289896675930464, 'o11': 10.700415128052052, 'o12': 7.703478853012862, 'o13': 9.685957651970261, 'o14': 9.342571201098654, 'o15': 8.048444919837538, 'o16': 6.561581618283539, 'o17': 7.2406310135631715, 'o18': 5.2906629481278635, 'o19': 7.871940377445649, 'o20': 8.459611670562534, 'o21': 5.608795254612756, 'o22': 8.971804526894157, 'o23': 5.6559919541051755, 'o24': 7.7338349901459456, 'o25': 7.613416533560182}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type3': ['o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 16, 'r2': 13, 'r3': 4, 'r4': 6, 'r5': 9, 'r6': 12, 'r7': 12, 'm0': 3, 'm1': 7, 'fixer0': 11, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK,}
    state.storedLoc = {'o0': 1, 'o1': 12, 'o2': 12, 'o3': 9, 'o4': 11, 'o5': 0, 'o6': 10, 'o7': 5, 'o8': 8, 'o9': 11, 'o10': 5, 'o11': 11, 'o12': 7, 'o13': 4, 'o14': 14, 'o15': 13, 'o16': 8, 'o17': 13, 'o18': 8, 'o19': 0, 'o20': 14, 'o21': 9, 'o22': 11, 'o23': 11, 'o24': 5, 'o25': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'm1': False, 'fixer0': False}
    state.numUses = {'m0': 9, 'm1': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    5: [['order', 'type0', 200]],
    35: [['order', 'type0', 200]],
}
eventsEnv = {
}