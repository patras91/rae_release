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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9}

rv.GROUND_EDGES = {0: [5, 9], 1: [4, 7, 10, 9, 11], 2: [8, 5], 3: [5, 11], 4: [5, 1, 6, 9], 5: [2, 0, 3, 4, 7, 10, 200], 6: [4, 8, 10, 11], 7: [5, 1, 8, 9], 8: [7, 2, 6], 9: [0, 1, 4, 7, 200], 10: [5, 6, 11, 1, 12], 11: [1, 6, 3, 10], 12: [10], 200: [5, 9]}
rv.GROUND_WEIGHTS = {(0, 5): 5.745125905585944, (0, 9): 13.298287823537969, (1, 4): 8.561480255082932, (1, 7): 6.579848119490338, (1, 10): 15.06768218495591, (1, 9): 14.831968745986119, (1, 11): 1.8939442393464034, (2, 8): 8.611993424334752, (2, 5): 14.852808990270809, (3, 5): 10.851177362998731, (3, 11): 12.34885292185169, (4, 5): 6.540086068995485, (4, 6): 7.186951743742461, (4, 9): 13.985802627470587, (5, 7): 13.394251109883395, (5, 10): 8.416736561759159, (5, 200): 5.4677584276243945, (6, 8): 13.87084261951463, (6, 10): 6.6058642024107055, (6, 11): 2.9291110929464548, (7, 8): 2.7364531736936275, (7, 9): 11.67737232607731, (9, 200): 11.971961760309634, (10, 11): 6.966416529379174, (10, 12): 8.545650079961614}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 9.257503748436145, 'r1': 6.753043283035309, 'r2': 9.021923988788615, 'r3': 11.144389719055436, 'r4': 8.480861653985967, 'r5': 8.462691300435461, 'r6': 7.6763668570120895, 'r7': 6.599706300893755}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1,  'm11': rv.FACTORY1,  'm12': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1,  'fixer2': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26']
rv.OBJ_WEIGHT = {'o0': 7.805951404638131, 'o1': 6.520128753042993, 'o2': 8.849295653606184, 'o3': 7.776607842403836, 'o4': 6.204154877270066, 'o5': 8.597189148184825, 'o6': 10.221483356555193, 'o7': 6.398802926239199, 'o8': 8.565505347627266, 'o9': 7.26016061702338, 'o10': 6.338146820187542, 'o11': 3.2822322320207404, 'o12': 8.675136251463439, 'o13': 7.050845315053401, 'o14': 6.9654271713885185, 'o15': 4.261169779516877, 'o16': 4.0962660567903875, 'o17': 7.979321656868674, 'o18': 8.164258003028415, 'o19': 6.4652247887445355, 'o20': 6.098247938680066, 'o21': 8.151672501571682, 'o22': 9.28689771159595, 'o23': 7.563293138824724, 'o24': 5.2064991256157755, 'o25': 6.5954299120761455, 'o26': 7.089795113597486}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15'], 'type4': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21'], 'type5': ['o22', 'o23', 'o24', 'o25', 'o26']}

def ResetState():
    state.loc = { 'r0': 10, 'r1': 3, 'r2': 8, 'r3': 3, 'r4': 8, 'r5': 6, 'r6': 7, 'r7': 0, 'm0': 12, 'm1': 7, 'm2': 12, 'm3': 6, 'm4': 10, 'm5': 5, 'm6': 8, 'm7': 0, 'm8': 6, 'm9': 12, 'm10': 5, 'm11': 2, 'm12': 2, 'fixer0': 3, 'fixer1': 6, 'fixer2': 1, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK,}
    state.storedLoc = {'o0': 12, 'o1': 10, 'o2': 10, 'o3': 12, 'o4': 7, 'o5': 12, 'o6': 4, 'o7': 1, 'o8': 6, 'o9': 5, 'o10': 11, 'o11': 0, 'o12': 3, 'o13': 9, 'o14': 11, 'o15': 12, 'o16': 4, 'o17': 4, 'o18': 8, 'o19': 8, 'o20': 7, 'o21': 2, 'o22': 1, 'o23': 1, 'o24': 4, 'o25': 8, 'o26': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'm11': False, 'm12': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 12, 'm1': 11, 'm2': 10, 'm3': 9, 'm4': 10, 'm5': 10, 'm6': 5, 'm7': 12, 'm8': 9, 'm9': 5, 'm10': 9, 'm11': 2, 'm12': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    15: [['order', 'type0', 200]],
    1: [['order', 'type1', 200]],
}
eventsEnv = {
}