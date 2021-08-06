__author__ = 'patras'

class G():
    def __init__(self):
        pass

class RaeArgs():
    def __init__(self):
        pass

g = G()
g.planningMode = False
g.heuristic = None
g.backupUCT = False

def SetPlanningMode(s):
    g.planningMode = s

def GetPlanningMode():
    return g.planningMode

def SetHeuristicName(name):
    g.heuristic = name

def GetHeuristicName():
    return g.heuristic

def GetUtility():
    return g.opt 

def SetUtility(opt):
    g.opt = opt

def SetTimeLimit(t):
    g.timeLimit = t

def GetTimeLimit():
    return g.timeLimit

def SetDataGenerationMode(a):
    g.dataGenMode = a

def GetDataGenerationMode():
    return g.dataGenMode

def SetModelPath(p):
    g.modelPath = p

def GetModelPath():
    return g.modelPath

def SetBackupUCT(b):
    g.backupUCT = b

def GetBackupUCT():
    return g.backupUCT

def SetDoIterativeDeepening(s):
    g.iterativeDeepening = s

def GetDoIterativeDeepening():
    return g.iterativeDeepening