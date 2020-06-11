__author__ = "alex"

import numpy
from domain_constants import *
from state import state, rv
import GLOBALS

commandProb = {
    'applyRestart': [0.90, 0.1],
    'applyAlternative': [0.80, 0.20],
}

def Sense(cmd):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE