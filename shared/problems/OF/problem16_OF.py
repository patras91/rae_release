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
rv.SHIPPING_DOC = {rv.FACTORY1: 4.451212398464646}

rv.GROUND_EDGES = {0: [3, 5, 11], 1: [7, 2], 2: [1, 8, 12, 14, 9], 3: [6, 12, 16, 0, 7, 200], 4: [16], 5: [0, 8, 13, 14], 6: [8, 3, 9, 200], 7: [3, 14, 1], 8: [5, 2, 6, 15, 200], 9: [2, 6, 11], 10: [13], 11: [0, 16, 9, 13, 15], 12: [3, 2], 13: [5, 11, 16, 10, 15], 14: [2, 5, 7, 16], 15: [8, 11, 13], 16: [4, 14, 3, 11, 13, 200], 200: [3, 6, 8, 16]}
rv.GROUND_WEIGHTS = {(0, 3): 1, (0, 5): 6.937178995078457, (0, 11): 1.461069787299758, (1, 7): 1.5327883837443208, (1, 2): 2.4916169542169957, (2, 8): 15.069434729867824, (2, 12): 8.967740832017308, (2, 14): 2.1026161848194125, (2, 9): 9.552109688537609, (3, 6): 13.485086334066853, (3, 12): 1.225902679811572, (3, 16): 4.644968357114329, (3, 7): 7.795219646144886, (3, 200): 9.482992313874318, (4, 16): 4.893983491045553, (5, 8): 5.274432151846693, (5, 13): 2.744979058722868, (5, 14): 4.831220583082304, (6, 8): 14.207678586292172, (6, 9): 17.00419809247188, (6, 200): 17.374680281474564, (7, 14): 6.986486676925336, (8, 15): 9.422507399950733, (8, 200): 17.592582834209182, (9, 11): 14.627450296572004, (10, 13): 5.04923230741359, (11, 16): 10.20300615021321, (11, 13): 8.38679367671092, (11, 15): 6.3744567674688515, (13, 16): 5.560710846728888, (13, 15): 5.83517965491033, (14, 16): 6.086521472854756, (16, 200): 7.532536447578449}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4']
rv.ROBOT_CAPACITY = {'r0': 10.591268530013892, 'r1': 6.375307466409092, 'r2': 6.206216522681152, 'r3': 7.279900422657904, 'r4': 10.038705392678407}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']
rv.OBJ_WEIGHT = {'o0': 8.837545004888913, 'o1': 5.836305419737675, 'o2': 5.38071764192833, 'o3': 4.743772917896548, 'o4': 7.08620518062325, 'o5': 4.316660007844366, 'o6': 10.27477426295829, 'o7': 10.220221969982557, 'o8': 7.224066545388779, 'o9': 7.827335419018491, 'o10': 4.275394154511856, 'o11': 5.473605410125407, 'o12': 9.178715837457846, 'o13': 6.028553249888431, 'o14': 4.624022446833967, 'o15': 9.689154513179615, 'o16': 7.235409333789379, 'o17': 5.848544097167677, 'o18': 6.379865814381554, 'o19': 7.871431359102328, 'o20': 6.318887726110657, 'o21': 6.591994571295982, 'o22': 7.168326902629106, 'o23': 6.785977861484281}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5'], 'type2': ['o6', 'o7', 'o8', 'o9', 'o10'], 'type3': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21', 'o22', 'o23']}

def ResetState():
  state.loc = { r0: 3, r1: 0, r2: 11, r3: 15, r4: 11, m0: 12, fixer0: 15, fixer1: 7, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK, o20: UNK, o21: UNK, o22: UNK, o23: UNK,}
    state.storedLoc{'o0': 2, 'o1': 1, 'o2': 7, 'o3': 3, 'o4': 8, 'o5': 3, 'o6': 4, 'o7': 2, 'o8': 15, 'o9': 0, 'o10': 16, 'o11': 6, 'o12': 3, 'o13': 4, 'o14': 7, 'o15': 11, 'o16': 5, 'o17': 10, 'o18': 0, 'o19': 5, 'o20': 5, 'o21': 15, 'o22': 11, 'o23': 5}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL, o20: NIL, o21: NIL, o22: NIL, o23: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses3
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    4: [['order', type0, 200]],
    3: [['order', type0, 200]],
    3: [['order', type1, 200]],
    8: [['order', type2, 200]],
    2: [['order', type2, 200]],
    3: [['order', type2, 200]],
    1: [['order', type2, 200]],
    3: [['order', type2, 200]],
    3: [['order', type4, 200]],
    6: [['order', type4, 200]],
}
eventsEnv = {
}