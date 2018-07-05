__author__ = 'patras'
import globals
import pipes

class PlanningTree():
    def __init__(self, n, args, type1):
        self.label = n # name of the method or task corresponding to this node
        self.args = args # arguments of the method corresponding to this node
        self.type = type1 # whether this is a task or a method or command
        self.eff = float("inf") # efficiency of this node
        self.children = [] # list of children of this node

    def GetLabel(self):
        return self.label

    def GetArgs(self):
        return self.args

    def SetRemainingCandidates(self, mList):
        self.remCands = mList

    def RemoveFromCandidates(self, m):
        self.remCands.remove(m)

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

    def AddEfficiency(self, e2):
        e1 = self.eff
        if e1 == float("inf"):
            res = e2
        elif e2 == float("inf"):
            res = e1
        else:
            res = (e1 * e2) / (e1 + e2)
        self.eff = res

    def GetEff(self):
        return self.eff

    def GetMethod(self):
        if self.type == 'method':
            return self.label
        else:
            print("ERR MSG: Type mistach in Refinement Tree")
            print("ERR MSG: Asking for method when the type is ", self.type)
            return None

    def DeleteChild(self, child):
        self.children.remove(child)

    def DeleteAllChildren(self):
        self.children = []

    def GetChild(self):
        assert(len(self.children) == 1)
        return self.children[0]

    def AddChild(self, node):
        self.children = self.children + [node]

    def SetEff(self, e):
        self.eff = e

    def GetPrettyString(self):
        if self.label == 'root' or self.label == 'Failure':
            return self.label
        if self.label != None:
            return self.label.__name__
        else:
            return "NONE"

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
        print("EFFICIENCY = ", self.GetEff())
        while(level[curr] != []):
            print(' '.join(elem.GetPrettyString() for elem in level[curr]))
            for elem in level[curr]:
                level[next] += elem.children
            curr += 1
            next += 1
            level[next] = []
        print("\n------------------------")

    def copy(self):
        r = PlanningTree(self.label, self.args, self.type)
        r.SetEff(self.eff)
        if self.children == []:
            return r
        else:
            for child in self.children:
                c_copy = child.copy()
                r.children = r.children + [c_copy]
        return r

def CreateFailureNode():
    tnode = PlanningTree('Failure', 'Failure', 'Failure')
    tnode.SetEff(0)
    return tnode

class ActingTree():
    def __init__(self, m):
        self.label = m
        self.type = 'method'
        self.children = []
        self.parent = None

    def SetLabelAndType(self, l, ty):
        self.label = l
        assert(ty == 'method' or ty == 'command')
        self.type = ty

    def GetLabel(self):
        return self.label

    def Clear(self):
        self.children = []
        self.label = None

    def AddChild(self):
        newNode = ActingTree(None)
        newNode.parent = self
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
            return self.children[0] # the first child of this node
        else:
            # travel upwards in the tree until you find an ancestor with a next child
            parent = self.parent
            curr_child = self
            while(True):
                if parent == None:
                    return None # No possible successor, you have reached the end of the tree
                else:
                    index = parent.children.index(curr_child)
                    if index < len(parent.children) - 1: # found the successor!
                        return parent.children[index + 1]
                curr_child = parent
                parent = parent.parent

    def GetSize(self):
        "returns the number of nodes of the tree with this as root"
        if self.type == 'method':
            count = 1
            for c in self.children:
                count += c.GetSize()
            return count
        else:
            return 1

class GuideTree():
    def __init__(self, m):
        self.label = m
        self.children = []
        self.parent = None

    def SetLabel(self, l):
        self.label = l

    def GetLabel(self):
        return self.label

    def Clear(self):
        self.children = []
        self.label = None

    def AddChild(self):
        newNode = GuideTree(None)
        newNode.parent = self
        self.children.append(newNode)
        return newNode

    def DeleteChild(self, child):
        self.children.remove(child)

    def GetPrettyString(self, elem):
        if elem.label == 'root' or elem.label == "END":
            return elem.label
        if elem.label != None:
            return elem.label.__name__
        else:
            return "NONE"

    def Print(self):
        level = {}
        level[0] = [self]
        level[1] = []
        curr = 0
        next = 1
        print("\n------GUIDE TREE-------")
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
            return self.children[0] # the first child of this node
        else:
            # travel upwards in the tree until you find an ancestor with a next child
            parent = self.parent
            curr_child = self
            while(True):
                if parent == None:
                    return None # No possible successor, you have reached the end of the tree
                else:
                    index = parent.children.index(curr_child)
                    if index < len(parent.children) - 1: # found the successor!
                        return parent.children[index + 1]
                curr_child = parent
                parent = parent.parent
