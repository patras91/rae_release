__author__ = 'patras'
from opPlanner import OpPlanner
from dataStructures import rL_PLAN

class RAEPlanChoice(OpPlanner):
    def __init__(self, l):
        self.b = l[0]
        self.k = l[1]
        self.maxSearchDepth = l[2]
        self.planLocals = rL_PLAN()

    def DoTask_RAEPlan(self, task, taskArgs):
        # Need to look through several candidates for this task
        cand, state, flag = GetCandidates(task, taskArgs)

        searchTreeNode = self.planLocals.GetSearchTreeNode()
        taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
        searchTreeNode.AddChild(taskNode)
        if flag == 1:
            self.planLocals.SetTaskToRefine(taskNode)
            self.planLocals.SetRefDepth(self.planLocals.GetDepth())

            
        if self.planLocals.GetRefDepth() + self.planLocals.GetRolloutDepth() <= self.planLocals.GetDepth():

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

        searchTreeNode = self.planLocals.GetSearchTreeNode()
        prevState = state.copy()
        newCommandNode = rTree.SearchTreeNode(cmd, 'command', cmdArgs)
        searchTreeNode.AddChild(newCommandNode)

        #k = max(1, GLOBALS.Getk() - int(self.planLocals.GetDepth() / 2))
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

        #self.planLocals is the set of variables local to this call to RAEplanChoice but used throughout
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
            
        InitializePlanningTree() 

        if self.verbosity > 1:
            print_stack_size(self.planLocals.GetStackId())
            print('Initial state is:')
            PrintState()

        self.planLocals.SetRefDepth(float("inf"))
        while (searchTreeRoot.GetSearchDone() == False): # all rollouts not explored
            try:
                self.planLocals.SetDepth(0)
                
                self.planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
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
            print_stack_size(self.planLocals.GetStackId())
            print('Final state is:')
            PrintState()

        taskToRefine = self.planLocals.GetTaskToRefine()
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
            self.planLocals.SetSearchTreeNode(nextNode)
            tree = DoMethod(m, task, taskArgs)
            return tree

    def FollowSearchTree_command(self, cmd, cmdArgs, searchNode):
        #self.planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
        assert(cmd == searchNode.GetLabel())
        stateNode = searchNode.GetNext()
        RestoreState(stateNode.GetLabel())
        self.planLocals.SetSearchTreeNode(stateNode)

        if stateNode.GetUtility() != Utility('Failure'):
            util = GetUtility(cmd, cmdArgs)
            stateNode.SetUtility(util)
            newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
            self.planLocals.GetCurrentNode().AddChild(newNode)
            self.planLocals.GetCurrentNode().AddUtility(util)
            return 'Success'
        else:
            raise Failed_Rollout('{}{}'.format(cmd.__name__, cmdArgs))

    def do_task(self, task, *taskArgs):
        self.planLocals.IncreaseDepthBy1()
        nextNode = self.planLocals.GetSearchTreeNode().GetNext()
        if nextNode != None:
            assert(nextNode.GetType() == "task" or nextNode.GetType() == "heuristic")
            return self.FollowSearchTree_task(task, taskArgs, nextNode)
        else:
            return self.DoTask_RAEPlan(task, taskArgs)

    def do_command(self, cmd, *cmdArgs):
        nextNode = self.planLocals.GetSearchTreeNode().GetNext()
        if nextNode == None:
            return self.DoCommand_RAEPlan(cmd, cmdArgs)
        else:
            assert(nextNode.GetType() == "command")
            return self.FollowSearchTree_command(cmd, cmdArgs, nextNode)

    