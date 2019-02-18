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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 10.54840018783987}

rv.GROUND_EDGES = {0: [12, 14, 17, 7, 15, 18], 1: [10, 18, 5, 14], 2: [7, 15, 4, 8, 14, 16], 3: [6, 14, 13], 4: [2, 15], 5: [1], 6: [3, 9, 11, 14, 7, 200], 7: [0, 6, 14, 2], 8: [2, 12, 17], 9: [10, 6], 10: [15, 16, 1, 9, 12], 11: [15, 6, 13], 12: [10, 0, 8], 13: [3, 11, 16, 17], 14: [1, 2, 0, 3, 6, 7], 15: [0, 2, 4, 10, 11], 16: [2, 13, 10], 17: [8, 13, 18, 0], 18: [0, 1, 17], 200: [6]}
rv.GROUND_WEIGHTS = {(0, 12): 14.718613040133693, (0, 14): 10.696560962419905, (0, 17): 6.387364282717152, (0, 7): 1, (0, 15): 8.791465263147693, (0, 18): 9.046268200324068, (1, 10): 13.502334992472626, (1, 18): 11.54869512782622, (1, 5): 10.638303264051391, (1, 14): 2.801327938068467, (2, 7): 7.241824256712318, (2, 15): 9.945223193230543, (2, 4): 2.911819855162345, (2, 8): 11.863412109639732, (2, 14): 8.412919206164121, (2, 16): 13.193369756327325, (3, 6): 1, (3, 14): 8.224840670915961, (3, 13): 9.050049007353083, (4, 15): 6.099348251095755, (6, 9): 3.167389725401658, (6, 11): 4.571138778523833, (6, 14): 14.534243104586267, (6, 7): 13.608229411127184, (6, 200): 1.2255310743259429, (7, 14): 10.07275050201761, (8, 12): 7.593364196743781, (8, 17): 8.605265985276674, (9, 10): 8.64766981765108, (10, 15): 5.493844379626203, (10, 16): 8.25279021937629, (10, 12): 14.33169996840809, (11, 15): 12.61050453441519, (11, 13): 14.332717856000905, (13, 16): 15.089186468712033, (13, 17): 2.1652766852183074, (17, 18): 9.627111705804008}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12']
rv.ROBOT_CAPACITY = {'r0': 7.6431096357829995, 'r1': 6.732491260651133, 'r2': 8.80105653672453, 'r3': 6.245217992690186, 'r4': 7.92055558403102, 'r5': 8.316460397929022, 'r6': 8.044830559009071, 'r7': 10.080934302076777, 'r8': 4.532184670061984, 'r9': 8.708554219467542, 'r10': 9.83112127505754, 'r11': 7.597223485639637, 'r12': 10.055009042869996}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'fixer0', 'fixer1', 'fixer2']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28']
rv.OBJ_WEIGHT = {'o0': 8.474715275947228, 'o1': 4.7250799579550495, 'o2': 8.57659288735234, 'o3': 7.468059106828898, 'o4': 5.3810459643355815, 'o5': 7.4713573442401255, 'o6': 9.524597137765792, 'o7': 8.559594970100436, 'o8': 7.568322137011056, 'o9': 10.080934302076777, 'o10': 5.857485823605948, 'o11': 6.498768241654528, 'o12': 5.185610415703189, 'o13': 5.6915652368116785, 'o14': 7.2498775899102545, 'o15': 3.86208251075078, 'o16': 6.690173091507244, 'o17': 9.704778463854353, 'o18': 9.543686693953248, 'o19': 8.449609841483111, 'o20': 6.588880197973192, 'o21': 9.05141317830421, 'o22': 7.118086583727048, 'o23': 3.684321917233231, 'o24': 5.544106466588904, 'o25': 9.115840514715579, 'o26': 7.18244536088573, 'o27': 8.373565110705183, 'o28': 7.576038852237265}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13'], 'type2': ['o14', 'o15', 'o16', 'o17'], 'type3': ['o18', 'o19', 'o20'], 'type4': ['o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28']}

def ResetState():
  state.loc = { r0: 11, r1: 4, r2: 16, r3: 10, r4: 4, r5: 0, r6: 13, r7: 0, r8: 15, r9: 13, r10: 8, r11: 14, r12: 5, m0: 3, m1: 15, m2: 8, m3: 4, m4: 15, m5: 14, m6: 8, m7: 2, m8: 13, m9: 6, fixer0: 10, fixer1: 17, fixer2: 16, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK, o20: UNK, o21: UNK, o22: UNK, o23: UNK, o24: UNK, o25: UNK, o26: UNK, o27: UNK, o28: UNK,}
    state.storedLoc{'o0': 16, 'o1': 8, 'o2': 0, 'o3': 8, 'o4': 3, 'o5': 7, 'o6': 2, 'o7': 4, 'o8': 5, 'o9': 3, 'o10': 0, 'o11': 8, 'o12': 4, 'o13': 12, 'o14': 11, 'o15': 9, 'o16': 2, 'o17': 1, 'o18': 4, 'o19': 9, 'o20': 18, 'o21': 0, 'o22': 8, 'o23': 12, 'o24': 2, 'o25': 12, 'o26': 3, 'o27': 1, 'o28': 13}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL, o20: NIL, o21: NIL, o22: NIL, o23: NIL, o24: NIL, o25: NIL, o26: NIL, o27: NIL, o28: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses8
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', type0, 200]],
    3: [['order', type0, 200]],
    6: [['order', type0, 200]],
    5: [['order', type0, 200]],
    5: [['order', type0, 200]],
    1: [['order', type0, 200]],
    1: [['order', type0, 200]],
    2: [['order', type1, 200]],
    4: [['order', type1, 200]],
    1: [['order', type2, 200]],
    2: [['order', type2, 200]],
    3: [['order', type2, 200]],
    5: [['order', type2, 200]],
    8: [['order', type3, 200]],
    6: [['order', type3, 200]],
    2: [['order', type3, 200]],
    1: [['order', type4, 200]],
    3: [['order', type4, 200]],
    7: [['order', type4, 200]],
    3: [['order', type4, 200]],
    2: [['order', type4, 200]],
    4: [['order', type4, 200]],
    5: [['order', type4, 200]],
    2: [['order', type4, 200]],
}
eventsEnv = {
}