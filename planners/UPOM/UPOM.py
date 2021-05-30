__author__ = 'patras'
from planners.opPlanner import OpPlanner
from shared.dataStructures import rL_PLAN
from shared.timer import globalTimer, DURATION
from shared import rTree
from shared.utility import Utility
import random
from shared.exceptions import *
import types
from shared import GLOBALS
import math
import numpy

class UPOMChoice(OpPlanner):
    
    def __init__(self, l, methods, m, domain, RestoreState, GetDomainState):
        self.n_ro = l[0]
        if len(l) > 1:
            assert(GLOBALS.GetHeuristicName() not in [None, 'None'])
            self.maxSearchDepth = l[1]
        self._C = 2
        self._fallback_max_depth = 80
        self._fallback_heuristic = 'zero'
        self.planLocals = rL_PLAN()
        self.name = "UPOM"
        self.methods = methods
        self.GetMethodInstances = m
        self.domain = domain
        self.RestoreState = RestoreState
        self.GetDomainState = GetDomainState

    def UPOMChoiceMain(self, task, planArgs):

        #planLocals is the set of variables local to this call to RAEplanChoice but used throughout
        self.planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is not important.
                                                     # This will be useful if we decide to simulate multiple stacks in future.
        self.planLocals.SetCandidates(planArgs.GetCandidates())

        self.planLocals.SetState(planArgs.state)

        taskArgs = planArgs.GetTaskArgs()
        self.planLocals.SetHeuristicArgs(task, taskArgs)
        self.planLocals.SetRolloutDepth(planArgs.GetDepth())

        globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
        
        searchTreeRoot = planArgs.GetSearchTree("UPOM")
        self.planLocals.SetSearchTreeRoot(searchTreeRoot)
        self.planLocals.SetTaskToRefine(-1)
            
        self.InitializePlanningTree() 

        i = 1
        while (i <= self.n_ro): # all rollouts not explored
            try:
                self.planLocals.SetDepth(0)
                self.planLocals.SetRefDepth(float("inf"))
                self.planLocals.SetUtilRollout(Utility('Success'))
                self.planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
                self.planLocals.SetFlip(False)
                self.RestoreState(searchTreeRoot.GetNext().GetPrevState())
                searchTreeRoot.updateIndex = 0
                self.do_task(task, *taskArgs) 
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())   
            except Failed_Rollout as e:
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())
            except DepthLimitReached as e:
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())
                pass
            else:
                pass
            i += 1

        taskToRefine = self.planLocals.GetTaskToRefine()
        if GLOBALS.GetDataGenerationMode() == "learnH":
            taskToRefine.UpdateAllUtilities()
            taskToRefine.GetTrainingItems(
                trainingDataRecords, 
                planArgs.GetCurUtil(), 
                planArgs.GetTask())

        #taskToRefine.PrintMethodsAndUtilities()
        return self.GetBestTillNow()

    def DoTaskUPOM(self, task, taskArgs):
        searchTreeNode = self.planLocals.GetSearchTreeNode()
        
        if searchTreeNode.children == []:
            # add new nodes with this task and its applicable method instances
            taskNode = rTree.SearchTreeNode(task, 'task', taskArgs, "UPOM")
            searchTreeNode.AddChild(taskNode)
            # Need to look through several candidates for this task
            cand, state, flag = self.GetCandidates(task, taskArgs)
            if flag == 1:
                self.planLocals.SetTaskToRefine(taskNode)
                self.planLocals.SetRefDepth(self.planLocals.GetDepth())
                self.planLocals.SetFlip(True)
            if self.planLocals.GetRefDepth() + self.planLocals.GetRolloutDepth() <= self.planLocals.GetDepth():
                newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs, "UPOM")

                util1 = self.planLocals.GetUtilRollout()
                util2 = Utility(GetHeuristicEstimate(task, taskArgs))
                self.planLocals.SetUtilRollout(util1 + util2)

                # Is this node needed?
                taskNode.AddChild(newNode)
                taskNode.updateIndex = 0
                raise DepthLimitReached()

            for m in cand:
                newSearchTreeNode = rTree.SearchTreeNode(m, 'method', taskArgs, "UPOM")
                newSearchTreeNode.SetPrevState(state)
                taskNode.AddChild(newSearchTreeNode)
        else:
            taskNode = searchTreeNode.children[0]
            assert(taskNode.type == 'task')
            if taskNode == self.planLocals.GetTaskToRefine():
                self.planLocals.SetFlip(True)
                self.planLocals.SetRefDepth(self.planLocals.GetDepth())

            if self.planLocals.GetRefDepth() + self.planLocals.GetRolloutDepth() <= self.planLocals.GetDepth():
                newNode = taskNode.children[0]
                taskNode.updateIndex = 0
                util1 = self.planLocals.GetUtilRollout()
                util2 = Utility(GetHeuristicEstimate(task, taskArgs))
                self.planLocals.SetUtilRollout(util1 + util2)

                raise DepthLimitReached()
        
        untried = []

        if taskNode.N == 0:
            untried = taskNode.children
        else:
            for child in taskNode.children:
                if child.children == []:
                    untried.append(child)

        if untried != []:
            mNode = random.choice(untried)
            index = taskNode.children.index(mNode)
        else:
            vmax = 0
            mNode = None
            index = None
            for i in range(0, len(taskNode.children)):
                v = taskNode.Q[i].GetValue() + \
                    self._C * math.sqrt(math.log(taskNode.N)/taskNode.n[i])
                if v >= vmax:
                    vmax = v
                    mNode = taskNode.children[i]
                    index = i

        m = mNode.GetLabel()
        self.RestoreState(mNode.GetPrevState())
        self.planLocals.SetSearchTreeNode(mNode)
        failed = False
        depthLimReached = False
        try:
            self.DoMethod(m, task, taskArgs)
        except Failed_Rollout as e:
            failed = True
        except DepthLimitReached as e:
            depthLimReached = True

        taskNode.updateIndex = index

        if m.cost > 0:
            self.planLocals.SetUtilRollout(self.planLocals.GetUtilRollout() + GetUtilityforMethod(m.cost))
        
        if failed:
            raise Failed_Rollout()
        elif depthLimReached:
            raise DepthLimitReached()

    def DoCommandUPOM(self, cmd, cmdArgs):

        searchTreeNode = self.planLocals.GetSearchTreeNode()
        #self.planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
        if searchTreeNode.children == []:
            commandNode = rTree.SearchTreeNode(cmd, 'command', None, "UPOM")
            searchTreeNode.AddChild(commandNode)
        else:
            commandNode = searchTreeNode.children[0]
            assert(commandNode.GetType() == 'command')
            assert(commandNode.GetLabel() == cmd)

        if self.planLocals.GetFlip() == False:
            retcode = 'Success'
            nextState = commandNode.GetNext().GetLabel()
            self.RestoreState(nextState)
        else:
            retcode = self.CallCommand_OperationalModel(cmd, cmdArgs)
            nextState = self.GetDomainState().copy()

        if retcode == 'Failure':
            nextStateNode = rTree.SearchTreeNode(nextState, 'state', None, "UPOM")
            nextStateNode.SetUtility(Utility('Failure'))
            commandNode.AddChild(nextStateNode)
            self.planLocals.SetUtilRollout(Utility('Failure'))
            commandNode.updateChild = nextStateNode
            raise Failed_Rollout()
        else:
            nextStateNode = commandNode.FindAmongChildren(nextState) 
            if nextStateNode == None:
                nextStateNode = rTree.SearchTreeNode(nextState, 'state', None, "UPOM")

                commandNode.AddChild(nextStateNode)
            
            util1 = self.planLocals.GetUtilRollout()
            util2 = self.GetUtility(cmd, cmdArgs)
            self.planLocals.SetUtilRollout(util1 + util2)
            commandNode.updateChild = nextStateNode
            nextStateNode.SetUtility(self.GetUtility(cmd, cmdArgs))
            self.planLocals.SetSearchTreeNode(nextStateNode)

    def beginCommand(self, cmd, cmdRet, cmdArgs):
        cmdRet['state'] = cmd(*cmdArgs)

    def GetBestTillNow(self):
        taskToRefine = self.planLocals.GetTaskToRefine()
        return (taskToRefine.GetBestMethodAndUtility_UPOM(), globalTimer.GetSimulationCounter())

    def do_task(self, task, *taskArgs):
        self.planLocals.IncreaseDepthBy1()
        self.DoTaskUPOM(task, taskArgs)

    def do_command(self, cmd, *cmdArgs):
        self.planLocals.IncreaseDepthBy1()
        self.DoCommandUPOM(cmd, cmdArgs)

    def GetUtility(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "SD" and cmd.__name__ == "helpRobot": 
            # kluge because I forgot to add this cost in the auto-gen problems
            cost = 7
        else:
            print(DURATION.COUNTER)
            cost = DURATION.COUNTER[cmd.__name__]
        if GLOBALS.GetUtility() == "successRatio":
            return Utility("Success")
        
        if type(cost) == types.FunctionType:
            numpy.random.seed(5000)
            res = cost(*cmdArgs)
        else:
            res = cost

        if GLOBALS.GetUtility() == "efficiency":
            return Utility(1/res)
        elif GLOBALS.GetUtility() == "resilience":
            return Utility(1/20 + 1/res)
        else:
            print("ERROR: Invalid utility")
            exit()