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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9}

rv.GROUND_EDGES = {0: [2, 8, 9, 1, 3, 4, 17, 200], 1: [0, 7, 9], 2: [3, 12, 15, 0, 8, 9], 3: [0, 2, 16], 4: [0, 12, 15], 5: [9], 6: [7, 9, 12, 200], 7: [1, 6], 8: [2, 0], 9: [1, 2, 17, 0, 5, 6], 10: [14], 11: [15, 14], 12: [4, 6, 2], 13: [14, 15], 14: [11, 16, 17, 10, 13, 15], 15: [4, 13, 14, 17, 2, 11], 16: [3, 14, 200], 17: [0, 9, 14, 15], 200: [0, 6, 16]}
rv.GROUND_WEIGHTS = {(0, 2): 2.452722544097621, (0, 8): 4.95108224595468, (0, 9): 10.348527713693437, (0, 1): 8.11082906017636, (0, 3): 7.7048248855067545, (0, 4): 4.444341025390024, (0, 17): 6.3049336029969645, (0, 200): 1.0481111451530447, (1, 7): 9.235735608346543, (1, 9): 8.422665900817158, (2, 3): 4.254543137914009, (2, 12): 13.35822833739066, (2, 15): 1, (2, 8): 7.979857767392749, (2, 9): 6.962891774933599, (3, 16): 11.665191355066362, (4, 12): 14.76216883519476, (4, 15): 11.102069029401253, (5, 9): 11.630365908830324, (6, 7): 10.568910186483857, (6, 9): 3.4727890893376525, (6, 12): 11.232063868704232, (6, 200): 6.385820385422862, (9, 17): 10.045630914092184, (10, 14): 10.106400131854258, (11, 15): 14.035024788534452, (11, 14): 4.524962774302022, (13, 14): 13.922537918300677, (13, 15): 6.193184463924412, (14, 16): 10.490022548180317, (14, 17): 12.457083816196658, (14, 15): 3.6495357943612277, (15, 17): 9.953402254500357, (16, 200): 13.749794189100456}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.565609610135766, 'r1': 7.4584015649106155, 'r2': 5.969381684464247, 'r3': 5.700407264299685, 'r4': 8.919238276906684, 'r5': 8.5148129627826, 'r6': 7.550711624127549, 'r7': 7.011879597900299, 'r8': 7.9875690945080615}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1,  'fixer2': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
rv.OBJ_WEIGHT = {'o0': 7.447510665527767, 'o1': 5.805454460039332, 'o2': 7.116802410302919, 'o3': 8.919238276906684, 'o4': 8.793842990150088, 'o5': 7.6509220428567515, 'o6': 7.21807553749064, 'o7': 7.2504874239545325, 'o8': 8.465118506576308, 'o9': 8.051912857580993, 'o10': 7.182812347991375, 'o11': 5.503374584927705, 'o12': 8.413401200124307, 'o13': 7.110726645590392, 'o14': 3.585646580062195}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3'], 'type2': ['o4', 'o5'], 'type3': ['o6', 'o7', 'o8', 'o9'], 'type4': ['o10', 'o11', 'o12', 'o13', 'o14']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 9, 'r2': 7, 'r3': 12, 'r4': 9, 'r5': 3, 'r6': 1, 'r7': 0, 'r8': 3, 'm0': 2, 'm1': 17, 'm2': 9, 'm3': 0, 'm4': 16, 'm5': 17, 'm6': 12, 'm7': 17, 'fixer0': 6, 'fixer1': 12, 'fixer2': 13, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK,}
    state.storedLoc = {'o0': 14, 'o1': 10, 'o2': 0, 'o3': 3, 'o4': 2, 'o5': 11, 'o6': 17, 'o7': 13, 'o8': 2, 'o9': 6, 'o10': 0, 'o11': 3, 'o12': 10, 'o13': 12, 'o14': 7}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 7, 'm1': 15, 'm2': 7, 'm3': 12, 'm4': 11, 'm5': 8, 'm6': 12, 'm7': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    6: [['order', 'type0', 200]],
    24: [['order', 'type1', 200]],
}
eventsEnv = {
}