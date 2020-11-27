__author__ = 'patras'
from opPlanner import OpPlanner

class UPOMChoice(OpPlanner):
	def __init__(self, l):
		self.n_ro = l[0]
		self.maxSearchDepth = l[1]

	def UPOM_Choice(self, task, planArgs):
        """
        RAEplanChoice is the main routine of the planner used by RAE which plans using the available operational models
        """

        #planLocals is the set of variables local to this call to RAEplanChoice but used throughout
        planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is not important.
                                                     # This will be useful if we decide to simulate multiple stacks in future.
        planLocals.SetCandidates(planArgs.GetCandidates())
        planLocals.SetState(planArgs.state)

        taskArgs = planArgs.GetTaskArgs()
        planLocals.SetHeuristicArgs(task, taskArgs)
        planLocals.SetRolloutDepth(planArgs.GetDepth())

        globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
        
        searchTreeRoot = planArgs.GetSearchTree()
        planLocals.SetSearchTreeRoot(searchTreeRoot)
        planLocals.SetTaskToRefine(-1)
            
        InitializePlanningTree() 

        if self.verbosity > 1:
            print('Initial state is:')
            PrintState()

        i = 1
        while (i <= GLOBALS.Get_nRO()): # all rollouts not explored
            try:
                planLocals.SetDepth(0)
                planLocals.SetRefDepth(float("inf"))
                planLocals.SetUtilRollout(Utility('Success'))
                planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
                planLocals.SetFlip(False)
                RestoreState(searchTreeRoot.GetNext().GetPrevState())
                searchTreeRoot.updateIndex = 0
                self.do_task(task, *taskArgs) 
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())   
            except Failed_Rollout as e:
                self.v_failedCommand(e)
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())
            except DepthLimitReached as e:
                #searchTreeRoot.PrintUsingGraphviz()
                searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())
                pass
            else:
                pass
            i += 1

        if self.verbosity > 1:
            print('Final state is:')
            PrintState()

        taskToRefine = planLocals.GetTaskToRefine()
        if GLOBALS.GetDataGenerationMode() == "learnH":
            taskToRefine.UpdateAllUtilities()
            taskToRefine.GetTrainingItems(
                trainingDataRecords, 
                planArgs.GetCurUtil(), 
                planArgs.GetTask())

        #taskToRefine.PrintMethodsAndUtilities()
        return GetBestTillNow()


	def DoTask_UPOM(self, task, taskArgs):
        searchTreeNode = planLocals.GetSearchTreeNode()
        
        if searchTreeNode.children == []:
            # add new nodes with this task and its applicable method instances
            taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
            searchTreeNode.AddChild(taskNode)
            # Need to look through several candidates for this task
            cand, state, flag = GetCandidates(task, taskArgs)

            if flag == 1:
                planLocals.SetTaskToRefine(taskNode)
                planLocals.SetRefDepth(planLocals.GetDepth())
                planLocals.SetFlip(True)
            if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():
                newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs)

                util1 = planLocals.GetUtilRollout()
                util2 = Utility(GetHeuristicEstimate(task, taskArgs))
                planLocals.SetUtilRollout(util1 + util2)

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
            if taskNode == planLocals.GetTaskToRefine():
                planLocals.SetFlip(True)
                planLocals.SetRefDepth(planLocals.GetDepth())

            if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():
                newNode = taskNode.children[0]
                taskNode.updateIndex = 0
                util1 = planLocals.GetUtilRollout()
                util2 = Utility(GetHeuristicEstimate(task, taskArgs))
                planLocals.SetUtilRollout(util1 + util2)

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
        planLocals.SetSearchTreeNode(mNode)
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
            planLocals.SetUtilRollout(planLocals.GetUtilRollout() + GetUtilityforMethod(m.cost))
        
        if failed:
            raise Failed_Rollout()
        elif depthLimReached:
            raise DepthLimitReached()

 	def DoCommand_UPOM(self, cmd, cmdArgs):

        searchTreeNode = planLocals.GetSearchTreeNode()
        #planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
        if searchTreeNode.children == []:
            commandNode = rTree.SearchTreeNode(cmd, 'command', None)
            searchTreeNode.AddChild(commandNode)
        else:
            commandNode = searchTreeNode.children[0]
            assert(commandNode.GetType() == 'command')
            assert(commandNode.GetLabel() == cmd)

        if planLocals.GetFlip() == False:
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
            planLocals.SetUtilRollout(Utility('Failure'))
            commandNode.updateChild = nextStateNode
            raise Failed_Rollout()
        else:
            nextStateNode = commandNode.FindAmongChildren(nextState) 
            if nextStateNode == None:
                nextStateNode = rTree.SearchTreeNode(nextState, 'state', None)

                commandNode.AddChild(nextStateNode)
            
            util1 = planLocals.GetUtilRollout()
            util2 = GetUtility(cmd, cmdArgs)
            planLocals.SetUtilRollout(util1 + util2)
            commandNode.updateChild = nextStateNode
            nextStateNode.SetUtility(GetUtility(cmd, cmdArgs))
            planLocals.SetSearchTreeNode(nextStateNode)

    def GetBestTillNow(self):
        taskToRefine = planLocals.GetTaskToRefine()
        return (taskToRefine.GetBestMethodAndUtility_UPOM(), globalTimer.GetSimulationCounter())

