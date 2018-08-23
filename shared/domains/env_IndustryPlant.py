import numpy
from domain_constants import *

commandProb = {
    'paint': [0.99, 0.01],
    'assemble': [0.95, 0.05],
    'pack': [1, 0.0],
    'wrap': [0.94, 0.06],
    'take': [1, 0],
    'put': [1, 0],
    'move': [0.95, 0.05],
}

def Sense(cmd):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE