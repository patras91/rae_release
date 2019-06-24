__author__ = 'patras'

class G():
    def __init__(self):
        pass

class RaeArgs():
    def __init__(self):
        pass

g = G()
g.doPlanning = False
g.planningMode = False
g.heuristic = None
g.mode = True

def SetDoPlanning(s):
	g.doPlanning = s

def SetPlanningMode(s):
    g.planningMode = s

def GetPlanningMode():
    return g.planningMode

def GetDoPlanning():
    return g.doPlanning

def GetShowOutputs():
    return g.showOutputs

def SetShowOutputs(o):
    g.showOutputs = o

def Setb(b): # number of methods to look at for every task/sub-task
    g.b = b

def Getb():
    return g.b

def Getk(): # number of outputs of commands to look at
    return g.k

def Setk(k):
    g.k = k

def SetSearchDepth(d):
    g.depth = d

def GetSearchDepth():
    return g.depth

def SetHeuristicName(name):
    g.heuristic = name

def GetHeuristicName():
    return g.heuristic

def GetSDN():
    return g.sdn
    
def SetSDN(sdn):
    if sdn == 'yes':
        g.sdn = True
    else:
        g.sdn = False

def GetOpt():
    return g.opt 

def SetOpt(opt):
    assert(opt == 'min' or opt == 'max')
    g.opt = opt

def SetUCTRuns(v):
    g.runs = v

def GetUCTRuns():
    return g.runs

def SetUCTmode(val):
    if val == 'UCT' or val == "uct" or val == "Uct":
        g.mode = True
    else:
        g.mode = False

def GetUCTmode():
    return g.mode

def GetC():
    return 2