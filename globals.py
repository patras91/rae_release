__author__ = 'patras'

class G():
    def __init__(self):
        pass

g = G()
g.doSampling = False
g.samplingMode = False

def SetDoSampling(s):
	g.doSampling = s

def SetSamplingMode(s):
    g.samplingMode = s

def GetSamplingMode():
    return g.samplingMode

def GetDoSampling():
    return g.doSampling