__author__ = 'patras'

import threading

class rL():
    def __init__(self):
        self.rL = threading.local()

    def SetStackId(self, id):
        self.rL.stackid = id

    def GetStackId(self):
        return self.rL.stackid

class rL_APE(rL):

    def SetRetryCount(self, count):
        self.rL.rC = count

    def GetRetryCount(self):
        return self.rL.rC

    def GetRefinementList(self):
        return self.rL.refinementList

    def SetRefinementList(self, l):
        self.rL.refinementList = l

    def SetConcManagerList(self, l):
        self.rL.cml = l

    def GetConcManagerList(self):
        return self.rL.concManagerList

    def SetCommandCount(self, c):
        self.rL.commCount = c

    def GetCommandCount(self):
        return self.rL.commCount

    def SetCurrentNode(self, node):
        self.rL.currentNode = node 

    def GetCurrentNode(self):
        return self.rL.currentNode

    def SetRootNode(self, root):
        self.rL.rootNode = root

    def GetRootNode(self):
        return self.rL.rootNode

    def SetMainTask(self, t):
        self.rL.mainTask = t

    def GetMainTask(self):
        return self.rL.mainTask

    def SetMainTaskArgs(self, args):
        self.rL.taskArgs = args

    def GetMainTaskArgs(self):
        return self.rL.taskArgs

    def SetCommandDone(self, d):
        self.rL.commandDone = d

    def GetCommandDone(self):
        return self.rL.commandDone

class rL_PLAN(rL):

    def __init__(self):
        self.rL = threading.local()
        self.rL.firstChoice = None

    def GetMethod(self):
        return self.rL.method

    def SetMethod(self, m):
        self.rL.method = m

    def GetCandidates(self):
        return self.rL.candidates

    def SetCandidates(self, c):
        self.rL.candidates = c

    def SetCurrentNode(self, n):
        self.rL.currentNode = n

    def GetCurrentNode(self):
        return self.rL.currentNode

    def GetDepth(self):
        return self.rL.depth

    def SetDepth(self, d):
        self.rL.depth = d

    #def SetRTree(self, T):
    #    self.rL.rTree = T

    #def GetRTree(self):
    #    return self.rL.rTree

    def SetFirstChoice(self, m):
        if self.rL.firstChoice == None:
            self.rL.firstChoice = m

    def ResetFirstChoice(self):
        self.rL.firstChoice = None

    def GetFirstChoice(self):
        return self.rL.firstChoice 

    def SetActingTree(self, t):
        self.rL.actingTree = t

    def GetActingTree(self):
        return self.rL.actingTree

    def SetActingTreeCurrPtr(self, ptr):
        self.rL.atcp = ptr

    def GetActingTreeCurrPtr(self):
        return self.rL.atcp

class PlanArgs():
    def __init__(self):
        pass

    def GetMethod(self):
        return self.method

    def SetMethod(self, m):
        self.method = m

    def SetCandidates(self, cand):
        self.candidates = cand

    def GetCandidates(self):
        return self.candidates

    def GetStackId(self):
        return self.stackid

    def SetStackId(self, id):
        self.stackid = id

    def GetTask(self):
        return self.task

    def SetTask(self, t):
        self.task = t

    def GetTaskArgs(self):
        return self.taskArgs

    def SetTaskArgs(self, args):
        self.taskArgs = args

    def SetActingTree(self, t):
        self.actingTree = t

    def GetActingTree(self):
        return self.actingTree
