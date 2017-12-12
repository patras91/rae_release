__author__ = 'patras'

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

    def GetCost(self):
        return self.value.cost

    def GetMethod(self):
        return self.value.method

    def Update(self, result):
        self.value = result

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