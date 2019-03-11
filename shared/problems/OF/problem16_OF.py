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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [6, 14, 2, 11, 12, 13, 18, 200], 1: [6, 3, 19], 2: [0, 17, 19], 3: [1, 4, 10, 17, 5, 15], 4: [11, 3, 8], 5: [3, 9], 6: [1, 7, 8, 15, 0, 14, 16], 7: [9, 6, 15, 19], 8: [4, 6], 9: [19, 5, 7, 10, 20], 10: [9, 11, 3, 20], 11: [0, 4, 10, 16, 19], 12: [0, 13, 17], 13: [0, 12, 19], 14: [6, 15, 0, 16], 15: [3, 7, 16, 6, 14, 17, 20], 16: [6, 11, 14, 15, 19, 20], 17: [2, 12, 15, 18, 3], 18: [0, 17], 19: [1, 2, 7, 9, 11, 13, 16], 20: [9, 10, 15, 16], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 6): 1, (0, 14): 1.4958164366431754, (0, 2): 7.624828905204398, (0, 11): 9.327874918457269, (0, 12): 4.178207816675842, (0, 13): 8.599078687956965, (0, 18): 1.020945558074974, (0, 200): 6.102502112247915, (1, 6): 2.7017477919842143, (1, 3): 8.514868319057003, (1, 19): 9.91363267569843, (2, 17): 11.66924503852793, (2, 19): 2.012780983230166, (3, 4): 12.202327229106505, (3, 10): 10.60895485600225, (3, 17): 7.071926583130897, (3, 5): 5.434913532422893, (3, 15): 7.696745799206043, (4, 11): 10.1137803420455, (4, 8): 2.223071550942813, (5, 9): 3.984516436838538, (6, 7): 1, (6, 8): 1.9999879215623961, (6, 15): 6.949074455237894, (6, 14): 8.595488511765627, (6, 16): 6.780192406302709, (7, 9): 9.218593377889317, (7, 15): 8.570213158989738, (7, 19): 3.309435242583594, (9, 19): 8.886510193042477, (9, 10): 13.77921449400441, (9, 20): 8.745039483170384, (10, 11): 5.489445800162224, (10, 20): 6.200111533646726, (11, 16): 2.7537051429831827, (11, 19): 12.364762453227014, (12, 13): 10.628928954465177, (12, 17): 1.6120794867591455, (13, 19): 20.34745851132648, (14, 15): 11.270865807121444, (14, 16): 13.536567003961881, (15, 16): 11.290550471747348, (15, 17): 9.8614445586914, (15, 20): 6.6440120447591395, (16, 19): 1, (16, 20): 8.760836890257327, (17, 18): 10.536755335892643}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.721333085110105, 'r1': 6.464460505619757, 'r2': 7.309729589313092, 'r3': 7.400108167737869, 'r4': 5.446793859731249, 'r5': 3.1402733871056894, 'r6': 7.1092184062349, 'r7': 5.194348395298261, 'r8': 12.539340524908155, 'r9': 10.215043558458103, 'r10': 10.369086226757862, 'r11': 11.612875556275613, 'r12': 11.421916847722613}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1', 'fixer2']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']
rv.OBJ_WEIGHT = {'o0': 10.217501180894361, 'o1': 8.024276412521317, 'o2': 3.0361133740800805, 'o3': 5.838284393771618, 'o4': 6.7565607862364825, 'o5': 6.512613026022873, 'o6': 6.622489300127394, 'o7': 7.961867953323354, 'o8': 4.925277629469177, 'o9': 7.006416681837795, 'o10': 9.255001913775397, 'o11': 5.535874376646533, 'o12': 7.393393551865281, 'o13': 5.698251677440581, 'o14': 8.354998346889316, 'o15': 2.976313974063852, 'o16': 8.87259377228695, 'o17': 2.309712229483421, 'o18': 4.9119222971639775, 'o19': 8.224572217533506, 'o20': 4.8147958388162495, 'o21': 3.19867375278813, 'o22': 8.548482224484284, 'o23': 5.309768392983053}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19'], 'type4': ['o20', 'o21', 'o22', 'o23']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 5, 'r2': 17, 'r3': 18, 'r4': 17, 'r5': 3, 'r6': 18, 'r7': 4, 'r8': 11, 'r9': 13, 'r10': 6, 'r11': 20, 'r12': 5, 'm0': 11, 'm1': 9, 'm2': 9, 'm3': 4, 'm4': 12, 'm5': 16, 'fixer0': 16, 'fixer1': 4, 'fixer2': 9, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 0, 'o2': 15, 'o3': 12, 'o4': 7, 'o5': 11, 'o6': 3, 'o7': 9, 'o8': 16, 'o9': 15, 'o10': 19, 'o11': 7, 'o12': 15, 'o13': 19, 'o14': 4, 'o15': 17, 'o16': 14, 'o17': 19, 'o18': 9, 'o19': 16, 'o20': 5, 'o21': 19, 'o22': 10, 'o23': 19}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 12, 'm1': 13, 'm2': 14, 'm3': 9, 'm4': 12, 'm5': 6}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    11: [['order', 'type0', 200]],
    33: [['order', 'type0', 200]],
}
eventsEnv = {
}