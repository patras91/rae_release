__author__ = 'patras'
import globals

class RTNode():
    def __init__(self, n=None):
        self.value = n
        self.children = []

    def Insert(self, m):
        n = RTNode(m)
        self.children = self.children + [n]
        return n

    def GetRetcode(self):
        if self.value == 'FAILURE':
            return "Failure"
        else:
            return self.value.retcode

    def GetPreorderTraversal(self):
        if self.value == None:
            return []
        else:
            res = [self.value]
            for node in self.children:
                res = res + node.GetPreorderTraversal()
            return res

    def IncreaseCost(self, c):
        self.value.cost += 1

    def GetCost(self):
        return self.value.cost

    def GetMethod(self):
        return self.value.method

    def Update(self, result):
        self.value = result

    def UpdateDummy(self, m):
        self.value = globals.G()
        self.value.method = m
        self.value.cost = 0

    def DeleteChild(self, child):
        self.children.remove(child)

    def GetValue(self):
        return self.value

    def GetState(self):
        return self.value.state

    def DeleteChildren(self):
        self.children = []

    def GetChild(self):
        assert(len(self.children) == 1)
        return self.children[0]

    def AddChild(self, node):
        self.children = self.children + [node]

    def SetCost(self, c):
        self.value.cost = c

    def GetPrettyString(self, elem):
        if elem.value == 'ROOT':
            return elem.value
        if elem.value.method != None:
            return elem.value.method.__name__
        else:
            return "NONE"

    def Duplicate(self):
        newNode = RTNode()
        newNode.value = self.value
        for child in self.children:
            newNode.children.append(child.Duplicate())
        return newNode

    def Print(self):
        level = {}
        level[0] = [self]
        level[1] = []
        curr = 0
        next = 1
        while(level[curr] != []):
            print(' '.join(self.GetPrettyString(elem) for elem in level[curr]))
            #if curr == 0 and self.value.method != None:
            #    print(self.GetCost())
            for elem in level[curr]:
                level[next] += elem.children
            curr += 1
            next += 1
            level[next] = []

