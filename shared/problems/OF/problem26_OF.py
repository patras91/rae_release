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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 10.502378629118219}

rv.GROUND_EDGES = {0: [1, 5, 7, 8, 10, 11], 1: [0, 2, 5, 11], 2: [4, 1], 3: [8], 4: [6, 2], 5: [0, 1, 7], 6: [10, 4, 200], 7: [0, 5, 11], 8: [0, 3, 9], 9: [8, 11], 10: [0, 6], 11: [0, 1, 7, 9], 200: [6]}
rv.GROUND_WEIGHTS = {(0, 1): 7.1455434293429665, (0, 5): 1, (0, 7): 7.7743366834337895, (0, 8): 12.209114034371048, (0, 10): 13.060156232675304, (0, 11): 7.105523048394172, (1, 2): 3.455382588818737, (1, 5): 3.0282533728469057, (1, 11): 6.000301948110241, (2, 4): 5.463643054666836, (3, 8): 14.213507525193034, (4, 6): 9.176582739174036, (5, 7): 2.5998666080048647, (6, 10): 13.938210972718979, (6, 200): 15.24352070901666, (7, 11): 9.11163877723404, (8, 9): 3.462255415280091, (9, 11): 5.529717312321466}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
rv.ROBOT_CAPACITY = {'r0': 5.823996240852354, 'r1': 9.750442031295297, 'r2': 10.67973182151093, 'r3': 7.225847921205504, 'r4': 8.757941177051235, 'r5': 5.4552781593628925, 'r6': 4.719597824773933, 'r7': 10.098345121608054, 'r8': 5.360883011349402, 'r9': 4.965746790105371, 'r10': 10.469119957453408, 'r11': 5.763191375887615, 'r12': 8.405175962282003, 'r13': 7.792687724081032, 'r14': 12.065511698242567, 'r15': 9.014380226281157}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 6.953247066836295, 'o1': 8.310707987139379, 'o2': 2.1597382673679038, 'o3': 7.3106680003959434, 'o4': 8.013323321244147, 'o5': 5.306347362161507, 'o6': 11.481168896604924, 'o7': 5.953193174612722, 'o8': 11.348677598332861, 'o9': 8.015466790313555, 'o10': 6.899853458668863, 'o11': 6.425607621521133, 'o12': 6.628397910958162, 'o13': 2.399785209335989, 'o14': 7.120387224837438, 'o15': 9.117079075965336}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4'], 'type2': ['o5', 'o6', 'o7', 'o8', 'o9'], 'type3': ['o10', 'o11', 'o12', 'o13'], 'type4': ['o14', 'o15']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 3, 'r2': 10, 'r3': 11, 'r4': 10, 'r5': 0, 'r6': 2, 'r7': 9, 'r8': 9, 'r9': 4, 'r10': 5, 'r11': 2, 'r12': 2, 'r13': 10, 'r14': 0, 'r15': 7, 'm0': 10, 'm1': 5, 'm2': 8, 'm3': 6, 'm4': 5, 'm5': 8, 'fixer0': 10, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 1, 'o2': 11, 'o3': 11, 'o4': 3, 'o5': 4, 'o6': 1, 'o7': 9, 'o8': 10, 'o9': 7, 'o10': 6, 'o11': 3, 'o12': 6, 'o13': 9, 'o14': 3, 'o15': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'r14'": False, "'r15'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'m4'": False, "'m5'": False, "'fixer0'": False}
    state.numUses = {'m0': 15, 'm1': 5, 'm2': 8, 'm3': 11, 'm4': 4, 'm5': 10, 'fixer0': 8}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    2: [['order', 'type0', 200]],
    16: [['order', 'type0', 200]],
    22: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
    1: [['order', 'type1', 200]],
    7: [['order', 'type2', 200]],
    21: [['order', 'type2', 200]],
    27: [['order', 'type2', 200]],
    12: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
    25: [['order', 'type3', 200]],
    5: [['order', 'type3', 200]],
    3: [['order', 'type4', 200]],
    8: [['order', 'type4', 200]],
}
eventsEnv = {
}