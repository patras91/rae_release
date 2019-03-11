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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 10}

rv.GROUND_EDGES = {0: [7, 8, 10, 1, 3, 4, 11, 12, 13, 200], 1: [0, 5, 9], 2: [13, 5, 10], 3: [0], 4: [0, 6, 12], 5: [1, 2], 6: [4, 13, 7], 7: [6, 0], 8: [9, 0, 10], 9: [1, 8, 13], 10: [2, 8, 0], 11: [0], 12: [0, 4], 13: [0, 2, 6, 9], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 7): 6.6690511592256225, (0, 8): 10.107275148119665, (0, 10): 3.9598288902907077, (0, 1): 4.989980275821962, (0, 3): 9.869816309322575, (0, 4): 9.824176451192155, (0, 11): 11.712068979009851, (0, 12): 4.923835775339196, (0, 13): 1, (0, 200): 8.698639582008, (1, 5): 10.719531103609, (1, 9): 7.122308902599998, (2, 13): 16.11551815834821, (2, 5): 6.45010593840472, (2, 10): 8.460064452963453, (4, 6): 8.43785093489937, (4, 12): 3.217453534612617, (6, 13): 7.721938750293126, (6, 7): 6.432777607455998, (8, 9): 7.087126723696562, (8, 10): 2.9556081855740484, (9, 13): 8.702999965172056}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1,  'r15': rv.FACTORY1,  'r16': rv.FACTORY1,  'r17': rv.FACTORY1,  'r18': rv.FACTORY1,  'r19': rv.FACTORY1,  'r20': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.239033602040173, 'r1': 5.000957076588925, 'r2': 8.14726616366299, 'r3': 7.530858904602768, 'r4': 8.5169565348229, 'r5': 7.453992530885658, 'r6': 9.213180348006277, 'r7': 9.206185726464799, 'r8': 9.654307850611563, 'r9': 9.413462751130115, 'r10': 6.687635514639733, 'r11': 10.246471641981039, 'r12': 6.269529423181431, 'r13': 8.595075604169834, 'r14': 8.973183865454105, 'r15': 7.788329065477217, 'r16': 6.930753083768686, 'r17': 7.967538727414449, 'r18': 7.194630311878275, 'r19': 7.04318473293259, 'r20': 6.702391379776632}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 9.216933440999588, 'o1': 4.787689235349045, 'o2': 4.742124364278277, 'o3': 4.3418837915877155, 'o4': 6.104859684573844, 'o5': 7.463850091142419, 'o6': 10.246471641981039, 'o7': 4.127910801556082, 'o8': 7.592402116641618, 'o9': 7.994612293370208, 'o10': 7.661338297071165, 'o11': 7.177020164547295, 'o12': 4.40166472210589, 'o13': 8.769867782510078, 'o14': 3.8811977002967732, 'o15': 9.113169953417483, 'o16': 10.246471641981039, 'o17': 5.762073148190554, 'o18': 6.544250122455605, 'o19': 9.226993050576734, 'o20': 3.955407541430766, 'o21': 5.818484695361477, 'o22': 4.848334371065047}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 1, 'r2': 9, 'r3': 0, 'r4': 1, 'r5': 5, 'r6': 7, 'r7': 11, 'r8': 5, 'r9': 2, 'r10': 1, 'r11': 5, 'r12': 2, 'r13': 9, 'r14': 3, 'r15': 5, 'r16': 9, 'r17': 10, 'r18': 3, 'r19': 8, 'r20': 5, 'm0': 4, 'fixer0': 12, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 0, 'o1': 2, 'o2': 7, 'o3': 6, 'o4': 6, 'o5': 9, 'o6': 7, 'o7': 10, 'o8': 11, 'o9': 2, 'o10': 13, 'o11': 10, 'o12': 6, 'o13': 0, 'o14': 10, 'o15': 7, 'o16': 11, 'o17': 13, 'o18': 2, 'o19': 0, 'o20': 3, 'o21': 9, 'o22': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'r16': NIL, 'r17': NIL, 'r18': NIL, 'r19': NIL, 'r20': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'r15': False, 'r16': False, 'r17': False, 'r18': False, 'r19': False, 'r20': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    20: [['order', 'type0', 200]],
    14: [['order', 'type1', 200]],
}
eventsEnv = {
}