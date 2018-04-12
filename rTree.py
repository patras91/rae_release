__author__ = 'patras'
import globals
import pipes

class RTNode():
    def __init__(self, n, args, type):
        self.label = n
        self.args = args
        self.type = type
        self.cost = 0
        self.children = []

    def GetLabel(self):
        return self.label

    def GetArgs(self):
        return self.args

    def GetRetcode(self):
        if self.label == "Failure":
            return "Failure"
        else:
            return "Success"

    def GetPreorderTraversal(self):
        if self.label == None:
            return []
        else:
            res = [self.label]
            for node in self.children:
                res = res + node.GetPreorderTraversal()
            return res

    def IncreaseCost(self, c):
        self.cost += 1

    def GetCost(self):
        return self.cost

    def GetMethod(self):
        return self.label

    def DeleteChild(self, child):
        self.children.remove(child)

    def DeleteChildren(self):
        self.children = []

    def GetChild(self):
        assert(len(self.children) == 1)
        return self.children[0]

    def AddChild(self, node):
        self.children = self.children + [node]

    def SetCost(self, c):
        self.cost = c

    def GetPrettyString(self, elem):
        if elem.label == 'root':
            return elem.label
        if elem.label != None:
            return elem.label.__name__
        else:
            return "NONE"

    def Duplicate(self):
        newNode = RTNode()
        newNode.value = self.value
        for child in self.children:
            newNode.children.append(child.Duplicate())
        return newNode

    def GetInEtcFormat(self):
        if self.children == []:
            return self.GetPrettyString(self)
        else:
            res =  "("
            for elem in self.children:
                res += elem.GetInEtcFormat()
            res += ")"
        return res

    def Print(self):
        treeString = self.GetInEtcFormat() + ";"
        t = pipes.Template()
        f = t.open('pipefile', 'w')
        f.write(treeString)
        f.close()

    def Print_old(self):
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

def CreateFailureNode():
    return RTNode('Failure', 'Failure', 'Failure')