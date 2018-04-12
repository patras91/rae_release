__author__ = 'patras'

class G():
    def __init__(self):
        pass

class RaeArgs():
    def __init__(self):
        pass

g = G()
g.doSampling = False
g.samplingMode = False
g.simulationMode = 'on'
g.K = 3

def SetDoSampling(s):
	g.doSampling = s

def SetSamplingMode(s):
    g.samplingMode = s

def GetSamplingMode():
    return g.samplingMode

def GetDoSampling():
    return g.doSampling

def SetK(k):
    g.K = k

def getK():
    return g.K

def GetSimulationMode():
    return g.simulationMode

def SetSimulationMode(mode):
    g.simulationMode = mode

def SetConcurrent(mode):
    if mode == 'y':
        g.concurrentMode = True
    else:
        g.concurrentMode = False

def GetConcurrentMode():
    return g.concurrentMode

def SetLazy(val):
    if val == 'y':
        g.lazy = True
    else:
        g.lazy = False

def GetLazy():
    return g.lazy

def SetSampleBreadth(b):
    g.sample_b = b

def GetSampleBreadth():
    return g.sample_b

def SetSearchDepth(d):
    g.searchDepth = d

def GetSearchDepth():
    return g.searchDepth

def GetSampleCount():
    return 5