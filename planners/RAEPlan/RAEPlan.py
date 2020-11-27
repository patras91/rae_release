__author__ = 'patras'
from opPlanner import OpPlanner

class RAEPlanChoice(OpPlanner):
	def __init__(self, l):
		self.b = l[0]
		self.k = l[1]
		self.maxSearchDepth = l[2]

	def DoTask_RAEPlan(self, task, taskArgs):
        # Need to look through several candidates for this task
        cand, state, flag = GetCandidates(task, taskArgs)

        searchTreeNode = planLocals.GetSearchTreeNode()
        taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
        searchTreeNode.AddChild(taskNode)
        if flag == 1:
            planLocals.SetTaskToRefine(taskNode)
            planLocals.SetRefDepth(planLocals.GetDepth())

            
        if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():

            newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs)
            newNode.SetPrevState(state)
            newNode.SetUtility(Utility(GetHeuristicEstimate()))
            taskNode.AddChild(newNode)
            raise Expanded_Search_Tree_Node()

        for m in cand:
            newSearchTreeNode = rTree.SearchTreeNode(m, 'method', taskArgs)
            newSearchTreeNode.SetPrevState(state)
            taskNode.AddChild(newSearchTreeNode)
        raise Expanded_Search_Tree_Node()

    def DoCommand_RAEPlan(self, cmd, cmdArgs):
        #outcomeStates = []

        searchTreeNode = planLocals.GetSearchTreeNode()
        prevState = state.copy()
        newCommandNode = rTree.SearchTreeNode(cmd, 'command', cmdArgs)
        searchTreeNode.AddChild(newCommandNode)

        #k = max(1, GLOBALS.Getk() - int(planLocals.GetDepth() / 2))
        k = GLOBALS.Getk()
        for i in range(0, k):
            RestoreState(prevState)
            retcode = CallCommand_OperationalModel(cmd, cmdArgs)
            nextState = state.copy()

            if retcode == 'Failure':
                newNode = rTree.SearchTreeNode(nextState, 'state', None)
                newNode.SetUtility(Utility('Failure'))
                newNode.SetPrevState(prevState)
                newCommandNode.AddChild(newNode)
                #outcomeStates.append(nextState)
            else:
                #index = IndexOf(nextState, outcomeStates)
                index = -1
                if index != -1:
                    # this state has already been planned for, so just use the previous result
                    #effList.append(effs[index])
                    #childNode = searchNodes[index]
                    newCommandNode.IncreaseWeight(nextState)
                else:
                    newNode = rTree.SearchTreeNode(nextState, 'state', None)
                    newNode.SetPrevState(prevState)
                    newCommandNode.AddChild(newNode)
                    #outcomeStates.append(nextState)
                    
        raise Expanded_Search_Tree_Node

    def RAEplan_Choice(self, task, planArgs):
        """
        RAEplan_Choice is the main routine of the planner used by RAE which plans using the available operational models
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
            
        InitializePlanningTree() 

        if self.verbosity > 1:
            print_stack_size(planLocals.GetStackId())
            print('Initial state is:')
            PrintState()

        planLocals.SetRefDepth(float("inf"))
        while (searchTreeRoot.GetSearchDone() == False): # all rollouts not explored
            try:
                planLocals.SetDepth(0)
                
                planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
                self.do_task(task, *taskArgs) 
                searchTreeRoot.UpdateChildPointers()  
            except Failed_Rollout as e:
                self.v_failedCommand(e)
                searchTreeRoot.UpdateChildPointers()
            except DepthLimitReached as e:
                searchTreeRoot.UpdateChildPointers()  
            except Expanded_Search_Tree_Node as e:
                pass
            else:
                pass

        if self.verbosity > 1:
            print_stack_size(planLocals.GetStackId())
            print('Final state is:')
            PrintState()

        taskToRefine = planLocals.GetTaskToRefine()
        if GLOBALS.GetDataGenerationMode() == "learnH":
            taskToRefine.GetTrainingItems_SLATE(
                trainingDataRecords, 
                planArgs.GetCurUtil(), 
                planArgs.GetTask())

        return (taskToRefine.GetBestMethodAndUtility(), globalTimer.GetSimulationCounter())
        
    def FollowSearchTree_task(self, task, taskArgs, node):
        nextNode = node.GetNext()
        m = nextNode.GetLabel()
        if m == 'heuristic':
            raise DepthLimitReached()
        else:
            RestoreState(nextNode.GetPrevState())
            planLocals.SetSearchTreeNode(nextNode)
            tree = DoMethod(m, task, taskArgs)
            return tree

    def FollowSearchTree_command(cmd, cmdArgs, searchNode):
        #planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
        assert(cmd == searchNode.GetLabel())
        stateNode = searchNode.GetNext()
        RestoreState(stateNode.GetLabel())
        planLocals.SetSearchTreeNode(stateNode)

        if stateNode.GetUtility() != Utility('Failure'):
            util = GetUtility(cmd, cmdArgs)
            stateNode.SetUtility(util)
            newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
            planLocals.GetCurrentNode().AddChild(newNode)
            planLocals.GetCurrentNode().AddUtility(util)
            return 'Success'
        else:
            raise Failed_Rollout('{}{}'.format(cmd.__name__, cmdArgs))

    