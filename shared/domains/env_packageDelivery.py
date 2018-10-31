import globals
import numpy
from state import state
from domain_chargeableRobot import rv
from domain_constants import *

commandProb = {
    'lookupDB': [0.98, 0.02],
}

def Sense(cmd):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE