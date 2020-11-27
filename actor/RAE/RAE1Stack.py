__author__="patras"
from dataStructures import rL_APE
import rTree
from utility import Utility
import GLOBALS
import random
import numpy

class MethodInstance():
    def __init__(self, m):
        self.method = m
        self.params = None
        self.cost = 0

    def SetParams(self, p):
        self.params = p

    def GetParams(self):
        return self.params

    def Call(self):
        self.method(*self.params)

    def GetName(self):
        return self.method.__name__

    def SetCost(self, c):
        self.cost = c

    def __repr__(self):
        return self.method.__name__ + str(self.params) 

    def __eq__(self, other):
        if other == 'heuristic' or other == 'Failure' or other == None or other == 'root' or other == 'task':
            return False
        else:
            return self.method == other.method and self.params == other.params

class Failed_command(Exception):
    pass

class Failed_Rollout(Exception):
    pass

class Failed_task(Exception):
    pass

class Incorrect_return_code(Exception):
    pass

class Expanded_Search_Tree_Node(Exception):
    pass

class DepthLimitReached(Exception):
    pass


class RAE1():
    def __init__(self, task, raeArgs, domain, ipcArgs, cmdStatusStack, v, state, methods):
        self.raeLocals = rL_APE() # variables that are local to every stack
        """ Initialize the local variables of a stack used during acting """
        self.raeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
        self.raeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
        self.raeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                             # This is a dictionary to accomodate for commands with different costs.
        self.raeLocals.SetMainTask(task)
        self.raeLocals.SetMainTaskArgs(raeArgs.taskArgs)

        self.aT = rTree.ActingTree()
        self.aT.SetPrevState(state.copy())
        self.raeLocals.SetActingTree(self.aT)
        self.raeLocals.SetUtility(Utility('Success'))
        self.raeLocals.SetEfficiency(float("inf"))

        self.raeLocals.SetUseBackupUCT(False)

        self.domain = domain
        self.cmdStatusStack = cmdStatusStack
        self.ipcArgs = ipcArgs

        if domain == "SDN_dev":
            cmdStatusStack[raeArgs.stack] = None

        self.GetNewIdNum = 0
        self.verbosity = v
        self.state = state
        self.methods = methods

    def GetMethodInstances(self, methods, tArgs):
    
        instanceList = [] # List of all applicable method instances for t

        for m in methods:

            q = m.__code__.co_argcount
            mArgs = m.__code__.co_varnames
            
            if len(tArgs) < q - 1:
                # some parameters are uninstantiated
                print(m.__name__)
                paramList = self.EvaluateParameters(m.parameters, mArgs, tArgs)
                
                for params in paramList:
                    instance = MethodInstance(m)
                    instance.SetParams(tArgs + params)
                    if hasattr(m, "cost"):
                        instance.SetCost(m.cost)
                    instanceList.append(instance)
            else:
                instance = MethodInstance(m)
                instance.SetParams(tArgs)
                if hasattr(m, "cost"):
                    instance.SetCost(m.cost)
                instanceList.append(instance)

        random.seed(100)
        random.shuffle(instanceList)
        return instanceList 

    def RAE1Main(self, task, raeArgs):
        """
        RAE1 is the actor with a single execution stack. The first argument is the name (which
        should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
        raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
        """

        if self.verbosity > 0:
            print('\n---- RAE: Create stack {}, task {}{}\n'.format(raeLocals.GetStackId(), task, raeArgs.taskArgs))

        self.ipcArgs.BeginCriticalRegion(self.raeLocals.GetStackId())

        if self.verbosity > 1:
            print_stack_size(self.raeLocals.GetStackId())
            print('Initial state is:')
            PrintState()

        try:
            taskArgs = raeArgs.taskArgs 
            retcode = self.do_task(task, *taskArgs)  # do acting

        except Failed_command as e:
            if self.verbosity > 0:
                print('Failed command {}'.format(e))
            retcode = 'Failure'

        except Failed_task as e:
            if self.verbosity > 0:
                print('Failed task {}'.format(e))
            retcode = 'Failure'
        else:
            pass
        if self.verbosity > 1:
            print('Final state is:')
            PrintState()

        if self.verbosity > 0:
            print("\n---- RAE: Done with stack %d\n" %self.raeLocals.GetStackId())

        EndCriticalRegion()

        if retcode == 'Failure':
            self.raeLocals.SetUtility(Utility('Failure'))
            self.raeLocals.SetEfficiency(0)

        if GLOBALS.GetUtility() == "efficiency":
            if self.domain != "OF":
                assert(numpy.isclose(self.raeLocals.GetEfficiency(), self.raeLocals.GetUtility().GetValue()))

        #self.raeLocals.GetActingTree().PrintUsingGraphviz()
        h, t, c = self.raeLocals.GetActingTree().GetMetaData()
        return (retcode, 
            self.raeLocals.GetRetryCount(), 
            self.raeLocals.GetEfficiency(), 
            h, t, c, 
            self.raeLocals.GetUtility(),
            self.raeLocals.GetPlanningUtilitiesList())

    def GetCandidateByPlanning(self, candidates, task, taskArgs):
        """
        RAE calls this functions when it wants suggestions from RAEplan
        """
        if self.verbosity > 0:
            #print(colorama.Fore.RED, "Starting simulation for stack")
            print("Starting simulation for stack")

        if self.raeLocals.GetUseBackupUCT() == True:
            planM = ssu.StateSpaceUCTMain(task, taskArgs)
            if planM != 'Failure':
                return (planM, candidates)
            else:
                raise Failed_task('{}{}'.format(task, taskArgs))

        queue = multiprocessing.Queue()
        actingTree = self.raeLocals.GetActingTree()

        #actingTree.PrintUsingGraphviz()
        p = multiprocessing.Process(
            target=RAE.PlannerMain, 
            args=[self.raeLocals.GetMainTask(), 
            self.raeLocals.GetMainTaskArgs(), 
            queue, 
            candidates,
            self.state.copy(),
            self.raeLocals.GetActingTree(),
            self.raeLocals.GetUtility()])

        p.start()
        p.join(int(0.7*GLOBALS.GetTimeLimit())) # planner gets max 70% of total time 

        if p.is_alive() == True:
            p.terminate()
            methodInstance, expUtil, simTime = queue.get()
        else:
            methodInstance, expUtil, simTime = queue.get()
            curUtil = self.raeLocals.GetUtility()

            # save some metadata
            self.raeLocals.AddToPlanningUtilityList(curUtil)
            self.raeLocals.AddToPlanningUtilityList(expUtil)
            self.raeLocals.AddToPlanningUtilityList(expUtil + curUtil)
            globalTimer.UpdateSimCounter(simTime)

        #retcode = plannedTree.GetRetcode()

        if self.verbosity > 0:
            #print("Done with planning. Result = {} \n".format(methodInstance), colorama.Style.RESET_ALL)
            print("Done with planning. Result = {} \n".format(methodInstance))

        if methodInstance == 'Failure':
            if GLOBALS.GetBackupUCT() == True:
                self.raeLocals.SetUseBackupUCT(True)
                planM = ssu.StateSpaceUCTMain(task, taskArgs)
                if planM != 'Failure':
                    return (planM, candidates)
                else:
                    return (candidates[0], candidates[1:])
            else:
                return (candidates[0], candidates[1:])
        else:
            if GLOBALS.GetDataGenerationMode() == "learnM2":
                trainingDataRecords.Add(
                        self.state, 
                        methodInstance, 
                        self.raeLocals.GetEfficiency(),
                        task,
                        taskArgs,
                        self.raeLocals.GetMainTask(),
                        self.raeLocals.GetMainTaskArgs()
                    )
            candidates.pop(candidates.index(methodInstance))
            return (methodInstance, candidates)

    def GetCandidateFromLearnedModel(self, fname, task, candidates, taskArgs):
        domain = self.domain
        device = "cpu"

        # features = {
        #     "EE": 22,
        #     "SD": 24,
        #     "SR": 23,
        #     "OF": 0,
        #     "CR": 22,
        # }

        features = {
        "EE": 182, #22,
        "SD": 126, #24,
        "SR": 330, #23,
        "OF": 0,
        "CR": 97, #22, #91
        }
        outClasses = {
            "EE": 17,
            "SD": 9,
            "SR": 16,
            "OF": 0,
            "CR": 10,
        }

        if domain != "OF":
            #model = nn.Sequential(nn.Linear(features[self.domain], 1)).to(device) 
            model = nn.Sequential(nn.Linear(features[domain], 512), 
                nn.ReLU(inplace=True), 
                nn.Linear(512, outClasses[domain]))
            model.load_state_dict(torch.load(fname))
            model.eval()

            x = Encode_LearnM(domain, self.state.GetFeatureString(), task, self.raeLocals.GetMainTask())
            np_x = numpy.array(x)
            x_tensor = torch.from_numpy(np_x).float()
            y = model(x_tensor)
            m_chosen = Decode_LearnM(domain, y)
        else:
            m_chosen = candidates[0].GetName()

        if GLOBALS.GetUseTrainedModel() == "learnMI" and m_chosen in params[domain]:
            pList = []
            for p in params[domain][m_chosen]:
                
                fname_mi = GLOBALS.GetModelPath() + "learnMI_{}_planner_{}_{}".format(domain, m_chosen, p)
                model = nn.Sequential(nn.Linear(params[domain][m_chosen][p]['nInputs'], 128), 
                    nn.ReLU(inplace=True), 
                    nn.Linear(128, params[domain][m_chosen][p]['nOutputs']))
                model.load_state_dict(torch.load(fname_mi))
                model.eval()
                
                x = Encode_LearnMI(domain, self.state.GetFeatureString(), m_chosen, task+" "+ " ".join([str(j) for j in taskArgs]))
                np_x = numpy.array(x)
                x_tensor = torch.from_numpy(np_x).float()
                y = model(x_tensor)
                pList.append(Decode_LearnMI(self.domain, m_chosen, p, y))

            for i in range(len(candidates)):
                if m_chosen == candidates[i].GetName():
                    candP = candidates[i].GetParams()
                    flag = True
                    for p in params[domain][m_chosen]:
                        if candP[params[domain][m_chosen][p]['pos']] != pList[params[domain][m_chosen][p]['pos']]:
                            flag = False
                    if flag:
                        res = candidates[i]
                        candidates.pop(i)
                        return res, candidates
        
        for i in range(len(candidates)):
            if m_chosen == candidates[i].GetName():
                res = candidates[i]
                candidates.pop(i)
                return res, candidates

        return (candidates[0], candidates[1:])

    def choose_candidate(self, candidates, task, taskArgs):
        if len(candidates) == 1 or (GLOBALS.GetPlanner() == None and GLOBALS.GetUseTrainedModel() == None):
            #random.shuffle(candidates)
            return(candidates[0], candidates[1:])
        elif GLOBALS.GetPlanner() == None and GLOBALS.GetUseTrainedModel() == "learnM1":
            fname = GLOBALS.GetModelPath() + "model_to_choose_{}_actor".format(self.domain)
            return GetCandidateFromLearnedModel(fname, task, candidates, taskArgs)
        elif GLOBALS.GetPlanner() == None and GLOBALS.GetUseTrainedModel() == "learnM2" or GLOBALS.GetUseTrainedModel() == "learnMI":
            fname = GLOBALS.GetModelPath() + "model_to_choose_{}_planner".format(self.domain)
            return GetCandidateFromLearnedModel(fname, task, candidates, taskArgs)
        else:
            return GetCandidateByPlanning(candidates, task, taskArgs)

    def DoTask_Acting(self, task, taskArgs):
        """
        Function to do the task in real world
        """
        self.v_begin(task, taskArgs)

        retcode = 'Failure'
        candidateMethods = self.methods[task][:]
        candidates = self.GetMethodInstances(candidateMethods, taskArgs)
        if candidates == []:
            raise Failed_task('{}{}'.format(task, taskArgs))

        parent, node = self.raeLocals.GetCurrentNodes()

        while (retcode != 'Success'):
            node.Clear() # Clear it on every iteration for a fresh start
            node.SetPrevState(self.state.copy())
            if GLOBALS.GetUtility() == "successRatio": # there may be a better way to do this
                self.raeLocals.SetUtility(Utility("Success"))

            (m,candidates) = self.choose_candidate(candidates, task, taskArgs)
            
            # if candidates == "usingBackupUCT":
            #     plan = m
            #     retcode = "Success"
            #     for (cmd, cmdArgs) in plan:
            #         try:
            #             DoCommandInRealWorld(cmd, cmdArgs)
            #         except Failed_command as e:
            #             retcode = "Failure"
            #             break
            # else:
            
            node.SetLabelAndType(m, 'method')
            self.raeLocals.SetCurrentNode(node)
            retcode = self.CallMethod_OperationalModel(self.raeLocals.GetStackId(), m, taskArgs)
            
            if m.cost > 0:
                self.raeLocals.SetEfficiency(AddEfficiency(self.raeLocals.GetEfficiency(), 1/m.cost))
                self.raeLocals.SetUtility(GetUtilityforMethod(m.cost) + self.raeLocals.GetUtility())
        
            if candidates == []:
                break

            if retcode == 'Failure':
                self.raeLocals.SetRetryCount(self.raeLocals.GetRetryCount() + 1)

        self.raeLocals.SetCurrentNode(parent)

        if retcode == 'Failure':
            raise Failed_task('{}{}'.format(task, taskArgs))
        elif retcode == 'Success':
            if GLOBALS.GetDataGenerationMode() == "learnM1" or GLOBALS.GetDataGenerationMode() == "learnM2":
                trainingDataRecords.Add(
                    self.state, 
                    m, 
                    self.raeLocals.GetEfficiency(),
                    task,
                    taskArgs,
                    self.raeLocals.GetMainTask(),
                    self.raeLocals.GetMainTaskArgs(),
                )
            return retcode
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))

    def CallMethod_OperationalModel(self, stackid, m, taskArgs):
        if self.verbosity > 0:
            print('Try method {}{}'.format(m.GetName(),taskArgs))

        retcode = 'Failure'
        try:
            if GLOBALS.GetPlanningMode() == False:
                self.ipcArgs.EndCriticalRegion()
                self.ipcArgs.BeginCriticalRegion(stackid)
                node = self.raeLocals.GetCurrentNode()
                node.SetPrevState(self.state.copy())

            if self.verbosity > 0:
                print("Executing method {}{}".format(m.GetName(), taskArgs))
            if self.verbosity > 1:
                print('Current state is:'.format(stackid))
                PrintState()

            m.Call()  # This is the main job of this function, CallMethod
            retcode = 'Success'
        except Failed_command as e:
            if self.verbosity > 0:
                print('Failed command {}'.format(e))
        except Failed_task as e:
            if self.verbosity > 0:
                print('Failed task {}'.format(e))

        if self.verbosity > 1:
            print('{} for method {}{}'.format(retcode, m.GetName(), taskArgs))

        return retcode

    def do_task(self, task, *taskArgs):
        if GLOBALS.GetPlanningMode() == True:
            self.planLocals.IncreaseDepthBy1()
            if GLOBALS.GetPlanner() == "UPOM":
                self.DoTask_UPOM(task, taskArgs)
            else:
                nextNode = self.planLocals.GetSearchTreeNode().GetNext()
                if nextNode != None:
                    assert(nextNode.GetType() == "task" or nextNode.GetType() == "heuristic")
                    return self.FollowSearchTree_task(task, taskArgs, nextNode)
                else:
                    return self.DoTask_RAEPlan(task, taskArgs)
        else:
            return self.DoTask_Acting(task, taskArgs)

    def InitializePlanningTree(self):
        root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
        self.planLocals.SetCurrentNode(root)
        self.planLocals.SetPlanningTree(root)

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
        
    def GetBestTillNow(self):
        taskToRefine = planLocals.GetTaskToRefine()
        return (taskToRefine.GetBestMethodAndUtility_UPOM(), globalTimer.GetSimulationCounter())

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

    def GetCandidates(self, task, tArgs):
        """ Called from DoTask_RAEPlan """
        if planLocals.GetCandidates() != None:
            # when candidates is a subset of the applicable methods, it is available from planLocals
            candidates = planLocals.GetCandidates()[:]
            planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
            prevState = planLocals.state
            flag = 1
        else:
            candidateMethods = methods[task][:] # set of applicable methods
            candidates = GetMethodInstances(candidateMethods, tArgs)
            prevState = state
            flag = 0
            
        # b = max(1, GLOBALS.Getb() - int(planLocals.GetDepth() / 4))
        if GLOBALS.GetPlanner() == "UPOM":
            cand = candidates
        else:
            b = GLOBALS.Getb()
            cand = candidates[0:min(b, len(candidates))]
        return cand, prevState, flag

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

    def GetHeuristicEstimate(self, task=None, tArgs=None):
        if GLOBALS.GetUseTrainedModel() == "learnH":
            assert(GLOBALS.GetUtility() == "efficiency" or GLOBALS.GetUtility() == "resilience")
            domain = self.domain
            features = {
                "EE": 204, 
                "SD": 144,
                "SR": 401,
                "OF": 627,
                "CR": 100,
            }

            outClasses = {
                "EE": 200,
                "SD": 75,
                "SR": 10,
                "OF": 10,
                "CR": 100,
            }
            if domain == "SR" or domain == "SD" or domain == "EE" or domain == "CR":
                model = nn.Sequential(nn.Linear(features[domain], 1024), 
                nn.ReLU(inplace=True),
                nn.Linear(1024, outClasses[domain]))
            elif domain == "OF":
                model = nn.Sequential(nn.Linear(features[domain], 512), 
                nn.ReLU(inplace=True),
                nn.Linear(512, outClasses[domain]))


            fname = GLOBALS.GetModelPath() + "model_for_eff_{}_planner_task_all".format(self.domain)
            model.load_state_dict(torch.load(fname))
            model.eval()

            cand, prevState, flag = GetCandidates(task, tArgs)
            effMax = 0
            for m in cand:
                if domain != "OF":
                    taskAndArgs = task+" "+str(tArgs)
                else:
                    taskAndArgs = task + " " +  " ".join(str(item) for item in tArgs)
                x = Encode_LearnH(
                    domain, 
                    prevState.GetFeatureString(),
                    m.GetName(),
                    taskAndArgs)

                np_x = numpy.array(x)
                x_tensor = torch.from_numpy(np_x).float()
                y = model(x_tensor)
                eff = Decode_LearnH(self.domain, y)
                if eff > effMax:
                    effMax = eff
            if GLOBALS.GetUtility() == "efficiency":
                return effMax
            else:
                if effMax == 0:
                    return 0
                else:
                    return 1/20 + effMax # resilience

        elif GLOBALS.GetUtility() == "successRatio":
            mtask, args = planLocals.GetHeuristicArgs()
            res = heuristic[mtask](args)
            return 1 if res > 0 else 0
        else:
            mtask, args = planLocals.GetHeuristicArgs()
            res = heuristic[mtask](args)
        return res
        
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

    def DoMethod(self, m, task, taskArgs):
        savedNode = planLocals.GetCurrentNode()
        
        newNode = rTree.PlanningTree(m, taskArgs, 'method')
        savedNode.AddChild(newNode)
        planLocals.SetCurrentNode(newNode)

        retcode = self.CallMethod_OperationalModel(planLocals.GetStackId(), m, taskArgs)


        if retcode == 'Failure':
            print("Error: retcode should not be Failure inside DoMethod.\n")
            raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))
        elif retcode == 'Success':
            if m.cost > 0:
                util = GetUtilityforMethod(m.cost)
            else:
                util = Utility('Success')
            for child in savedNode.children:
                util = util + child.GetUtility()
            savedNode.SetUtility(util)
            planLocals.SetCurrentNode(savedNode)

            return planLocals.GetPlanningTree()
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

    def beginCommand(self, cmd, cmdRet, cmdArgs):
        cmdPtr = GetCommand(cmd)
        cmdRet['state'] = cmdPtr(*cmdArgs)

    def do_command(self, cmd, *cmdArgs):
        """
        Perform command cmd(cmdArgs).
        """
        if GLOBALS.GetPlanningMode() == True:
            planLocals.IncreaseDepthBy1()
            if GLOBALS.GetPlanner() == "UPOM":
                DoCommand_UPOM(cmd, cmdArgs)
            else:
                nextNode = planLocals.GetSearchTreeNode().GetNext()
                if nextNode == None:
                    return DoCommand_RAEPlan(cmd, cmdArgs)
                else:
                    assert(nextNode.GetType() == "command")
                    return FollowSearchTree_command(cmd, cmdArgs, nextNode)
        else:
            return DoCommand_Acting(cmd, cmdArgs)

    def GetNewId(self):
        self.GetNewIdNum += 1
        return self.GetNewIdNum

    def AddEfficiency(self, e1, e2):

        if e1 == float("inf"):
            res = e2
        elif e2 == float("inf"):
            res = e1
        elif e1 == 0 and e2 == 0:
            res = 0
        else:
            res = e1 * e2 / (e1 + e2)
        return res

    def DoCommand_Acting(self, cmd, cmdArgs):

        if self.verbosity > 0:
            print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

        cmdRet = {'state':'running'}

        domain = self.domain
        if domain != 'SDN_dev':
            cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
            cmdThread.start()
        else:
            newCmdId = GetNewId()
            AddToCommandStackTable(newCmdId, self.raeLocals.GetStackId())
            cmdExecQueue.put([newCmdId, cmd, cmdArgs])

        if cmd.__name__ in self.raeLocals.GetCommandCount():
            self.raeLocals.GetCommandCount()[cmd.__name__] += 1
        else:
            self.raeLocals.GetCommandCount()[cmd.__name__] = 1

        EndCriticalRegion()
        BeginCriticalRegion(self.raeLocals.GetStackId())

        if domain != 'SDN_dev':
            while (cmdRet['state'] == 'running'):
                if self.verbosity > 0:
                    print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

                EndCriticalRegion()
                BeginCriticalRegion(self.raeLocals.GetStackId())
        else:
            while(self.cmdStatusStack[self.raeLocals.GetStackId()] == None):
                EndCriticalRegion()
                BeginCriticalRegion(self.raeLocals.GetStackId())

        if self.verbosity > 0:
            print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

        if domain != 'SDN_dev':
            retcode = cmdRet['state']
        else:
            [id, retcode, nextState] = self.cmdStatusStack[self.raeLocals.GetStackId()]
            assert(retcode == 'Success' or retcode == 'Failure')
            RestoreState(nextState)

        par, cmdNode = self.raeLocals.GetCurrentNodes()

        cmdNode.SetLabelAndType(cmd, 'command', cmdArgs)

        cmdNode.SetNextState(state.copy())

        if self.verbosity > 1:
            print('Command {}{} returned {}'.format(cmd.__name__, cmdArgs, retcode))
            print('Current state is')
            PrintState()

        if cmd.__name__ == "fail" or retcode == 'Failure':
            util1 = GetFailureUtility(cmd, cmdArgs)
            self.raeLocals.AddToPlanningUtilityList('fail')
            eff1 = GetFailureEfficiency(cmd, cmdArgs)
        else:
            util1 = GetUtility(cmd, cmdArgs)
            eff1 = GetEfficiency(cmd, cmdArgs)
            wait = False

            if self.domain == "OF": # to avoid overflow in output files
                if cmd.__name__ == "wait":
                    wait = True
                    if len(self.raeLocals.GetPlanningUtilitiesList()) > 1:
                        lastItem = str(self.raeLocals.GetPlanningUtilitiesList()[-1])
                        if lastItem[0:4] == "wait":
                            n = int(lastItem[4:]) + 1
                            self.raeLocals.GetPlanningUtilitiesList()[-1] = "wait" + str(n)
                        else:
                            self.raeLocals.AddToPlanningUtilityList("wait0")
                    else:
                        self.raeLocals.AddToPlanningUtilityList("wait0")
            if wait == False:
                self.raeLocals.AddToPlanningUtilityList(cmd.__name__)

        util2 = self.raeLocals.GetUtility()
        self.raeLocals.SetUtility(util1 + util2)
        self.raeLocals.SetEfficiency(AddEfficiency(eff1, self.raeLocals.GetEfficiency()))

        if retcode == 'Failure':
            raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
        elif retcode == 'Success':
            return retcode
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

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

    def CallCommand_OperationalModel(cmd, cmdArgs):
        self.v_begin_c(cmd, cmdArgs)
        cmdRet = {'state':'running'}
        #cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
        #cmdThread.start()

        beginCommand(cmd, cmdRet, cmdArgs)
        #if GLOBALS.GetPlanningMode() == False:
        #    EndCriticalRegion()
        #    BeginCriticalRegion(planLocals.GetStackId())

        #while (cmdRet['state'] == 'running'):
        #    if self.verbosity > 0:
        #        print_stack_size(planLocals.GetStackId(), path)
        #        print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
        #    if GLOBALS.GetPlanningMode() == False:
        #        EndCriticalRegion()
        #        BeginCriticalRegion(planLocals.GetStackId())

        if self.verbosity > 0:
            print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

        retcode = cmdRet['state']
        if self.verbosity > 1:
            print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
            print('Current state is')
            PrintState()

        return retcode

    def IndexOf(self, s, l):
        """ Helper function of PlanCommand_RAEPlan """
        i = 0
        for item in l:
            if item.EqualTo(s):
                return i
            i += 1 
        return -1

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

    def GetCost(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "SD" and cmd.__name__ == "helpRobot":
            cost = 7
        else:
            cost = DURATION.COUNTER[cmd.__name__]
        if type(cost) == types.FunctionType:
            numpy.random.seed(5000)
            res = cost(*cmdArgs)
        else:
            return cost

    def GetFailureUtility(self, cmd, cmdArgs):
        if GLOBALS.GetUtility() == "efficiency":
            return Utility(1/20)
        elif GLOBALS.GetUtility() == "resilience":
            return Utility(1/20 + 1/20)
        else:
            return Utility("Failure")

    def GetUtility(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "SD" and cmd.__name__ == "helpRobot": 
            # kluge because I forgot to add this cost in the auto-gen problems
            cost = 7
        else:
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

    def GetUtilityforMethod(self, cost):
        if GLOBALS.GetUtility() == "successRatio":
            return Utility("Success")
        elif GLOBALS.GetUtility() == "efficiency":
            return Utility(1/cost)
        elif GLOBALS.GetUtility() == "resilience":
            return Utility(1/20 + 1/cost)
        
    def GetFailureEfficiency(self, cmd, cmdArgs):
        return 1/20

    def GetEfficiency(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "SD" and cmd.__name__ == "helpRobot": # kluge because I forgot to add this cost in the auto-gen problems
            cost = 7
        else:
            cost = DURATION.COUNTER[cmd.__name__]
        if type(cost) == types.FunctionType:
            numpy.random.seed(5000)
            res = cost(*cmdArgs)
            return 1/res
        else:
            return 1/cost

    def EvaluateParameters(self, expr, mArgs, tArgs):
        for i in range(0, len(tArgs)):
            globals()[mArgs[i]] = tArgs[i]
        return eval(expr, globals())
        ## Verbosity functions 

    def v_begin(self, task, taskArgs):
        if self.verbosity > 0:
            print('Begin task {}{}'.format(task, taskArgs))

    def v_begin_c(self, cmd, cmdArgs):
        if self.verbosity > 0:
            print('Begin command {}{}'.format(cmd.__name__, cmdArgs))


    def v_failedCommand(self, e):
        if self.verbosity > 0:
            print('Failed command {}'.format(e))

    def v_failedTask(self, e):
        if self.verbosity > 0:
            print('Failed task {}'.format(e))

