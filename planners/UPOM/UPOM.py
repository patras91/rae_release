__author__ = 'patras'
from opPlanner import OpPlanner
from dataStructures import rL_PLAN

class UPOMChoice(OpPlanner):
    
    def __init__(self, l):
        self.n_ro = l[0]
        self.maxSearchDepth = l[1]
        self.planLocals = rL_PLAN()

    def UPOM_Choice(self, task, planArgs):

        #planLocals is the set of variables local to this call to RAEplanChoice but used throughout
        self.planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is not important.
                                                     # This will be useful if we decide to simulate multiple stacks in future.
        self.planLocals.SetCandidates(planArgs.GetCandidates())
        self.planLocals.SetState(planArgs.state)

        taskArgs = planArgs.GetTaskArgs()
        self.planLocals.SetHeuristicArgs(task, taskArgs)
        self.planLocals.SetRolloutDepth(planArgs.GetDepth())

        globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
        
        searchTreeRoot = planArgs.GetSearchTree()
        self.planLocals.SetSearchTreeRoot(searchTreeRoot)
        self.planLocals.SetTaskToRefine(-1)
            
        InitializePlanningTree() 

        if self.verbosity > 1:
            print('Initial state is:')
            PrintState()

        i = 1
        while (i <= GLOBALS.Get_nRO()): # all rollouts not explored
            try:
                self.planLocals.SetDepth(0)
                self.planLocals.SetRefDepth(float("inf"))
                self.planLocals.SetUtilRollout(Utility('Success'))
                self.planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
                self.planLocals.SetFlip(False)
                RestoreState(searchTreeRoot.GetNext().GetPrevState())
                searchTreeRoot.updateIndex = 0
                self.do_task(task, *taskArgs) 
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())   
            except Failed_Rollout as e:
                self.v_failedCommand(e)
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())
            except DepthLimitReached as e:
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(self.planLocals.GetUtilRollout().GetValue())
                pass
            else:
                pass
            i += 1

        if self.verbosity > 1:
            print('Final state is:')
            PrintState()

        taskToRefine = self.planLocals.GetTaskToRefine()
        if GLOBALS.GetDataGenerationMode() == "learnH":
            taskToRefine.UpdateAllUtilities()
            taskToRefine.GetTrainingItems(
                trainingDataRecords, 
                planArgs.GetCurUtil(), 
                planArgs.GetTask())

        #taskToRefine.PrintMethodsAndUtilities()
        return GetBestTillNow()


    def DoTask_UPOM(self, task, taskArgs):
        searchTreeNode = self.planLocals.GetSearchTreeNode()
        
        if searchTreeNode.children == []:
            # add new nodes with this task and its applicable method instances
            taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
            searchTreeNode.AddChild(taskNode)
            # Need to look through several candidates for this task
            cand, state, flag = GetCandidates(task, taskArgs)

            if flag == 1:
                self.planLocals.SetTaskToRefine(taskNode)
                self.planLocals.SetRefDepth(self.planLocals.GetDepth())
                self.planLocals.SetFlip(True)
            if self.planLocals.GetRefDepth() + self.planLocals.GetRolloutDepth() <= self.planLocals.GetDepth():
                newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs)

                util1 = self.planLocals.GetUtilRollout()
                util2 = Utility(GetHeuristicEstimate(task, taskArgs))
                self.planLocals.SetUtilRollout(util1 + util2)

                # Is this node needed?
                taskNode.AddChild(newNode)
                taskNode.updateIndex = 0
                raise DepthLimitReached()

            for m in cand:
                newSearchTreeNode = rTree.SearchTreeNode(m, 'method', taskArgs)
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
                    GLOBALS.GetC() * math.sqrt(math.log(taskNode.N)/taskNode.n[i])
                if v >= vmax:
                    vmax = v
                    mNode = taskNode.children[i]
                    index = i

        m = mNode.GetLabel()
        RestoreState(mNode.GetPrevState())
        self.planLocals.SetSearchTreeNode(mNode)
        failed = False
        depthLimReached = False
        try:
            DoMethod(m, task, taskArgs)
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

    def DoCommand_UPOM(self, cmd, cmdArgs):

        searchTreeNode = self.planLocals.GetSearchTreeNode()
        #self.planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
        if searchTreeNode.children == []:
            commandNode = rTree.SearchTreeNode(cmd, 'command', None)
            searchTreeNode.AddChild(commandNode)
        else:
            commandNode = searchTreeNode.children[0]
            assert(commandNode.GetType() == 'command')
            assert(commandNode.GetLabel() == cmd)

        if self.planLocals.GetFlip() == False:
            retcode = 'Success'
            nextState = commandNode.GetNext().GetLabel()
            RestoreState(nextState)
        else:
            retcode = CallCommand_OperationalModel(cmd, cmdArgs)
            nextState = state.copy()

        if retcode == 'Failure':
            nextStateNode = rTree.SearchTreeNode(nextState, 'state', None)
            nextStateNode.SetUtility(Utility('Failure'))
            commandNode.AddChild(nextStateNode)
            self.planLocals.SetUtilRollout(Utility('Failure'))
            commandNode.updateChild = nextStateNode
            raise Failed_Rollout()
        else:
            nextStateNode = commandNode.FindAmongChildren(nextState) 
            if nextStateNode == None:
                nextStateNode = rTree.SearchTreeNode(nextState, 'state', None)

                commandNode.AddChild(nextStateNode)
            
            util1 = self.planLocals.GetUtilRollout()
            util2 = GetUtility(cmd, cmdArgs)
            self.planLocals.SetUtilRollout(util1 + util2)
            commandNode.updateChild = nextStateNode
            nextStateNode.SetUtility(GetUtility(cmd, cmdArgs))
            self.planLocals.SetSearchTreeNode(nextStateNode)

    def GetBestTillNow(self):
        taskToRefine = self.planLocals.GetTaskToRefine()
        return (taskToRefine.GetBestMethodAndUtility_UPOM(), globalTimer.GetSimulationCounter())

