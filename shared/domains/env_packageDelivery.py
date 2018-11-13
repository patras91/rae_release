import globals
import numpy
from state import state
from domain_chargeableRobot import rv
from domain_constants import *

commandProb = {
    'lookupDB': [0.98, 0.02],
    'moveRobot': [0.97, 0.03],
    'wrap': [0.97, 0.03],
    'pickup': [0.95, 0.05],
    'load': [0.99, 0.01],
    'groundShip': [0.99, 0.01]
}

def Sense(cmd):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE