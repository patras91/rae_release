__author__ = 'patras'

class G():
    def __init__(self):
        pass

g = G()
g.doSampling = False
g.samplingMode = False
g.K = 2

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