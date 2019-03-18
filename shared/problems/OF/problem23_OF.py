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
rv.SHIPPING_DOC = {rv.FACTORY1: 2}

rv.GROUND_EDGES = {0: [1, 2, 5], 1: [4, 5, 6, 7, 0, 2, 200], 2: [0, 1, 4, 200, 3, 8], 3: [2, 4, 9, 12], 4: [5, 7, 1, 2, 3, 11], 5: [0, 1, 7, 12, 4, 6, 10], 6: [5, 1, 7, 200], 7: [6, 10, 1, 4, 5, 9], 8: [2], 9: [7, 3], 10: [5, 7, 12], 11: [4], 12: [3, 10, 5], 200: [1, 6, 2]}
rv.GROUND_WEIGHTS = {(0, 1): 9.246459389190116, (0, 2): 4.226809052208356, (0, 5): 8.45623944961215, (1, 4): 7.586636531507634, (1, 5): 5.572511289774625, (1, 6): 11.625607269975013, (1, 7): 12.239218169201287, (1, 2): 10.99170085186352, (1, 200): 13.231457899859542, (2, 4): 1, (2, 200): 7.8912364385819735, (2, 3): 9.123053728989522, (2, 8): 7.389398070010518, (3, 4): 6.116591185093311, (3, 9): 7.80627251023094, (3, 12): 6.5674340650413345, (4, 5): 16.734281818555125, (4, 7): 8.701377132933414, (4, 11): 12.246699815037275, (5, 7): 6.2287662773139045, (5, 12): 9.344386818999833, (5, 6): 11.410699287743308, (5, 10): 3.5235052364330324, (6, 7): 11.458910043446696, (6, 200): 4.375720723133243, (7, 10): 10.12433778642411, (7, 9): 4.87324037403207, (10, 12): 6.081848309169178}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.90794523844985, 'r1': 8.078425521575607, 'r2': 7.881262336038722, 'r3': 9.372212810354702, 'r4': 6.743072928057127, 'r5': 9.310845742951066, 'r6': 6.80271717745783, 'r7': 9.073213476494118, 'r8': 7.616671949795231, 'r9': 9.220026355518772, 'r10': 7.925692469458044}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 9.372212810354702, 'o1': 7.622867126166831, 'o2': 6.650362721666885, 'o3': 9.372212810354702, 'o4': 9.372212810354702, 'o5': 6.029579250661688, 'o6': 7.693701755766513, 'o7': 7.244644555345184, 'o8': 7.361143589793092, 'o9': 7.438637976717269, 'o10': 4.123554107416446, 'o11': 7.932412445434731, 'o12': 8.010624862173426, 'o13': 9.372212810354702, 'o14': 5.820400693123756, 'o15': 6.778213863594489, 'o16': 3.0954261346356953, 'o17': 7.704129760028181, 'o18': 7.090827311119229, 'o19': 4.14247412322689, 'o20': 2.6835436285828775, 'o21': 8.00772562574751}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14', 'o15'], 'type3': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 7, 'r2': 1, 'r3': 4, 'r4': 10, 'r5': 9, 'r6': 0, 'r7': 6, 'r8': 7, 'r9': 11, 'r10': 11, 'm0': 3, 'm1': 3, 'm2': 4, 'm3': 12, 'm4': 9, 'm5': 0, 'm6': 7, 'm7': 12, 'fixer0': 4, 'fixer1': 12, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 9, 'o2': 6, 'o3': 1, 'o4': 4, 'o5': 11, 'o6': 4, 'o7': 12, 'o8': 5, 'o9': 10, 'o10': 7, 'o11': 0, 'o12': 3, 'o13': 11, 'o14': 8, 'o15': 7, 'o16': 3, 'o17': 0, 'o18': 2, 'o19': 10, 'o20': 12, 'o21': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 9, 'm1': 9, 'm2': 10, 'm3': 10, 'm4': 18, 'm5': 9, 'm6': 6, 'm7': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    2: [['order', 'type1', 200]],
    7: [['order', 'type1', 200]],
}
eventsEnv = {
}