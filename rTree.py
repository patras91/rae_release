__author__ = 'patras'
import globals
import pipes

class RTNode():
    def __init__(self, n, args, type1):
        self.label = n # name of the method or task corresponding to this node
        self.args = args # arguments of the method corresponding to this node
        self.type = type1 # whether this is a task or a method or command
        self.cost = 0 # total cost of the children of the node
        self.children = [] # list of children of this node

    def GetLabel(self):
        return self.label

    def GetArgs(self):
        return self.args

    def GetRetcode(self):
        if self.label == "Failure" or self.args == "Failure":
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

    def GetPrettyString(self):
        if self.label == 'root' or self.label == 'Failure':
            return self.label
        if self.label != None:
            return self.label.__name__
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
            return self.GetPrettyString()
        else:
            res = "(" + ",".join(elem.GetInEtcFormat() for elem in self.children)
            res += ")" + self.GetPrettyString()            
        return res

    def Print(self):
        treeString = self.GetInEtcFormat() + ";"
        #print(treeString)
        t = pipes.Template()
        f = t.open('pipefile', 'w')
        f.write(treeString)
        f.close()

    def PrintInTerminal(self):
        level = {}
        level[0] = [self]
        level[1] = []
        curr = 0
        next = 1
        print("\n------PLANNING TREE-------")
        print("COST = ", self.GetCost())
        while(level[curr] != []):
            print(' '.join(self.GetPrettyString() for elem in level[curr]))
            #if curr == 0 and self.value.method != None:
            #    print(self.GetCost())
            for elem in level[curr]:
                level[next] += elem.children
            curr += 1
            next += 1
            level[next] = []
        print("\n------------------------")

def CreateFailureNode(m):
    tnode = RTNode(m, 'Failure', 'Failure')
    tnode.SetCost(float("inf"))
    return tnode

class RT_ape():
    def __init__(self, m, parent):
        self.label = m
        self.type = True
        self.children = []
        self.parent = parent

    def SetLabel(self, l, ty):
        self.label = l
        self.type = ty

    def GetLabel(self):
        return self.label

    def Clear(self):
        self.children = []
        self.label = None

    def AddChild(self):
        newNode = RT_ape(None, self)
        self.children.append(newNode)
        return newNode

    def GetPrettyString(self, elem):
        if elem.label == 'root' or elem.label == "END":
            return elem.label
        if elem.label != None:
            return elem.label.__name__
        else:
            return "NONE"

    def SetNextState(self, s):
        self.nextState = s

    def GetNextState(self):
        return self.nextState

    def GetChild(self):
        assert(len(self.children) == 1)
        return self.children[0]

    def Print(self):
        level = {}
        level[0] = [self]
        level[1] = []
        curr = 0
        next = 1
        print("\n------ACTING TREE-------")
        while(level[curr] != []):
            print(' '.join(self.GetPrettyString(elem) for elem in level[curr]))
            for elem in level[curr]:
                level[next] += elem.children
            curr += 1
            next += 1
            level[next] = []
        print("\n------------------------")

    def GetSuccessor(self):
        if self.children != []:
            return self.children[0]
        else:
            node = self.parent
            nodec = self
            while(True):
                if node == None:
                    return None
                else:
                    index = node.children.index(nodec)
                    if index < len(node.children) - 1:
                        return node.children[index + 1]
                nodec = node
                node = node.parent

    def GetNumberOfMethods(self):
        if self.type == True:
            count = 1
            for c in self.children:
                count += c.GetNumberOfMethods()
            return count
        else:
            return 0

    def GetNumberOfNodes(self):
        if self.type == True:
            count = 1
            for c in self.children:
                count += c.GetNumberOfNodes()
            return count
        else:
            return 1