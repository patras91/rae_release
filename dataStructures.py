__author__ = 'patras'

from rTree import RTNode
import threading

class TVPair():
    def __init__(self):
        self.T = None
        self.V = float('int')

    def SetT(self, tree):
        self.T = tree

    def GetT(self):
        return self.T

    def SetV(self, value):
        self.V = value

    def GetV(self):
        return self.V

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

class rL_PLAN(rL):

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

