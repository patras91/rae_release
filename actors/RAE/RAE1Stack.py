__author__="patras"
from shared.dataStructures import rL_APE
from shared import rTree
from shared.utility import Utility, UTIL
from shared import GLOBALS
import random
import numpy
import threading
from shared.timer import globalTimer, DURATION
import types
from planners.UPOM.UPOM import UPOMChoice
from planners.RAEPlan.RAEPlan import RAEPlanChoice
from planners.APEPlan.APEPlan import APEPlanChoice
import multiprocessing
from shared.exceptions import *
#import torch.nn as nn
#import torch
#from learning.convertDataFormat import Encode_LearnM, Decode_LearnM

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

def UsesSharedQueues(domain):
    return domain in ["Mobipick", "AIRS_dev"]

class RAE1():
    def __init__(self, task, raeArgs, domain, ipcArgs, cmdStatusStack, cmdStackTable, cmdExecQueue, v, state, methods, heuristic, useLearningStrategy, planner, plannerParams, RestoreState, GetDomainState):
        self.raeLocals = rL_APE() # variables that are local to every stack
        """ Initialize the local variables of a task/event stack used during acting """
        self.raeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.\
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
        self.cmdStackTable = cmdStackTable
        self.cmdExecQueue = cmdExecQueue
        self.ipcArgs = ipcArgs

        if UsesSharedQueues(domain):
            cmdStatusStack[raeArgs.stack] = None

        self.GetNewIdNum = 0
        self.verbosity = v
        self.state = state
        self.RestoreState = RestoreState
        self.GetDomainState = GetDomainState
        self.methods = methods
        self.heuristic = heuristic

        self.useLearningStrategy = useLearningStrategy
        self.InitializePlanner(planner, plannerParams)

    def InitializePlanner(self, p, params):
        if p == "APEPlan":
            self.planner = APEPlanChoice(params)
        elif p == "RAEPlan":
            self.planner = RAEPlanChoice(params)
        elif p == "UPOM":
            self.planner = UPOMChoice(params, self.methods, self.heuristic, self.GetMethodInstances, self.domain, self.RestoreState, self.GetDomainState)
        elif p == "None" or p == None:
            self.planner = None 
        else:
            print("Invalid planner. Please select from [APEPlan, RAEPlan, UPOM, None]")
            exit()

    def GetMethodInstances(self, methods, tArgs):
        instanceList = [] # List of all applicable method instances for t

        for m in methods:

            q = m.__code__.co_argcount
            mArgs = m.__code__.co_varnames
            
            if len(tArgs) < q - 1:
                # some parameters are uninstantiated
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
        #random.shuffle(instanceList)
        return instanceList 

    def GetMethodsForGoal(self, args):
        # TODO
        pass

    def RAE1Main(self, task, raeArgs):
        """
        RAE1 is the actor with a single execution stack. The first argument is the name (which
        should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
        raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
        """

        if self.verbosity > 0:
            print('\n---- RAE: Create stack {}, task {}{}\n'.format(self.raeLocals.GetStackId(), task, raeArgs.taskArgs))

        self.ipcArgs.BeginCriticalRegion(self.raeLocals.GetStackId())

        if self.verbosity > 1:
            #print_stack_size(self.raeLocals.GetStackId())
            print('Initial state is:')
            print(self.state)

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

        if self.verbosity > 1:
            print('Final state is:')
            print(self.state)

        if self.verbosity > 0:
            print("\n---- RAE: Done with stack %d\n" %self.raeLocals.GetStackId())

        self.ipcArgs.EndCriticalRegion()

        if retcode == 'Failure':
            self.raeLocals.SetUtility(Utility('Failure'))
            self.raeLocals.SetEfficiency(0)

        if GLOBALS.GetUtility() == UTIL.EFFICIENCY:
            if not self.domain == "deliver":
                assert(numpy.isclose(self.raeLocals.GetEfficiency(), self.raeLocals.GetUtility().GetValue()))

        #self.raeLocals.GetActingTree().PrintUsingGraphviz()
        h, t, c = self.raeLocals.GetActingTree().GetMetaData()
        traces = self.raeLocals.GetActingTree().Print()
        return (retcode,
            self.raeLocals.GetRetryCount(), 
            self.raeLocals.GetEfficiency(), 
            h, t, c, traces,
            self.raeLocals.GetUtility(),
            self.raeLocals.GetPlanningUtilitiesList())

    def GetCandidateByPlanning(self, candidates, task, taskArgs):
        """
        RAE calls this functions when it wants suggestions from a planner
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
        #actingTree = self.raeLocals.GetActingTree()

        #actingTree.PrintUsingGraphviz()
        p = multiprocessing.Process(
            target=self.planner.Main,
            args=[self.raeLocals.GetMainTask(),
            self.raeLocals.GetMainTaskArgs(),
            queue,
            candidates,
            self.state.copy(),
            self.raeLocals.GetActingTree(),
            self.raeLocals.GetUtility()
            ])

        p.start()
        p.join(int(0.7*GLOBALS.GetTimeLimit())) # planner gets max 70% of total time 

        if p.is_alive() == True:
            p.terminate()
            methodIndex, expUtil, planningTime = queue.get()
        else:
            methodIndex, expUtil, planningTime = queue.get()
            curUtil = self.raeLocals.GetUtility()

            # save some metadata
            self.raeLocals.AddToPlanningUtilityList(curUtil)
            self.raeLocals.AddToPlanningUtilityList(expUtil)
            self.raeLocals.AddToPlanningUtilityList(expUtil + curUtil)
            globalTimer.UpdateSimCounter(planningTime)


        #retcode = plannedTree.GetRetcode()
        if self.verbosity > 0:
            #print("Done with planning. Result = {} \n".format(methodInstance), colorama.Style.RESET_ALL)
            print("Done with planning. Result = {} \n".format(methodIndex))

        if methodIndex == 'Failure':
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
            methodInstance = candidates[methodIndex]
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
            candidates.pop(methodIndex)
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
        "explore": 182, #22,
        "nav": 126, #24,
        "rescue": 330, #23,
        "deliver": 0,
        "fetch": 97, #22, #91
        }
        outClasses = {
            "explore": 17,
            "nav": 9,
            "rescue": 16,
            "deliver": 0,
            "fetch": 10,
        }

        if domain != "deliver":
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

        if self.useLearningStrategy == "learnMI" and m_chosen in params[domain]:
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
        if len(candidates) == 1 or task == "__diagnose" or (not self.planner and not self.useLearningStrategy):
            #random.shuffle(candidates)
            return(candidates[0], candidates[1:])
        elif self.planner == None and self.useLearningStrategy == "learnM":
            fname = GLOBALS.GetModelPath() + "model_to_choose_{}_actor".format(self.domain)
            return self.GetCandidateFromLearnedModel(fname, task, candidates, taskArgs)
        elif self.planner == None and self.useLearningStrategy in ["learnM2", "learnMI"]:
            fname = GLOBALS.GetModelPath() + "model_to_choose_{}_planner".format(self.domain)
            return self.GetCandidateFromLearnedModel(fname, task, candidates, taskArgs)
        else:
            return self.GetCandidateByPlanning(candidates, task, taskArgs)

    def DoTask_Acting(self, task, args):
        """
        Function to do the task in real world
        """
        self.v_begin(task, args)

        retcode = 'Failure'
        if task == 'achieve':
            candidateMethods = self.GetMethodsForGoal(args)
        else:
            candidateMethods = self.methods[task][:]

        candidates = self.GetMethodInstances(candidateMethods, args)
        if candidates == []:
            raise Failed_task('{}{}'.format(task, args))

        parent, node = self.raeLocals.GetCurrentNodes()

        while (retcode != 'Success'):
            node.Clear() # Clear it on every iteration for a fresh start
            node.SetPrevState(self.state.copy())
            if GLOBALS.GetUtility() == UTIL.SUCCESS_RATIO: # there may be a better way to do this
                self.raeLocals.SetUtility(Utility("Success"))

            (m,candidates) = self.choose_candidate(candidates, task, args)
            
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
            retcode = self.CallMethod_OperationalModel(self.raeLocals.GetStackId(), m, args)
            
            if m.cost > 0:
                self.raeLocals.SetEfficiency(self.AddEfficiency(self.raeLocals.GetEfficiency(), 1/m.cost))
                self.raeLocals.SetUtility(self.GetUtilityforMethod(m.cost) + self.raeLocals.GetUtility())
        
            if candidates == []:
                break

            if retcode == 'Failure':
                self.raeLocals.SetRetryCount(self.raeLocals.GetRetryCount() + 1)

        self.raeLocals.SetCurrentNode(parent)

        if retcode == 'Failure':
            raise Failed_task('{}{}'.format(task, args))
        elif retcode == 'Success':
            if GLOBALS.GetDataGenerationMode() == "learnM1" or GLOBALS.GetDataGenerationMode() == "learnM2":
                trainingDataRecords.Add(
                    self.state, 
                    m, 
                    self.raeLocals.GetEfficiency(),
                    task,
                    args,
                    self.raeLocals.GetMainTask(),
                    self.raeLocals.GetMainTaskArgs(),
                )
            return retcode
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, task, args))

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
                print(self.state)

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

    def do_diagnosis(self):
        self.DoTask_Acting('__diagnose', [])

    def do_task(self, task, *taskArgs):
        if GLOBALS.GetPlanningMode():
            self.planner.do_task(task, *taskArgs)
        else:
            if self.domain in ["AIRS", "AIRS_dev"]:
                self.do_diagnosis()
            return self.DoTask_Acting(task, taskArgs)

    # def DoMethod(self, m, task, taskArgs):
    #     savedNode = planLocals.GetCurrentNode()
    #
    #     newNode = rTree.PlanningTree(m, taskArgs, 'method')
    #     savedNode.AddChild(newNode)
    #     planLocals.SetCurrentNode(newNode)
    #
    #     retcode = self.CallMethod_OperationalModel(planLocals.GetStackId(), m, taskArgs)
    #
    #
    #     if retcode == 'Failure':
    #         print("Error: retcode should not be Failure inside DoMethod.\n")
    #         raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))
    #     elif retcode == 'Success':
    #         if m.cost > 0:
    #             util = GetUtilityforMethod(m.cost)
    #         else:
    #             util = Utility('Success')
    #         for child in savedNode.children:
    #             util = util + child.GetUtility()
    #         savedNode.SetUtility(util)
    #         planLocals.SetCurrentNode(savedNode)
    #
    #         return planLocals.GetPlanningTree()
    #     else:
    #         raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

    def beginCommand(self, cmd, cmdRet, cmdArgs):
        #cmdPtr = self.GetCommand(cmd)
        cmdRet['state'] = cmd(*cmdArgs)

    def do_command(self, cmd, *cmdArgs):
        """
        Perform command cmd(cmdArgs).
        """
        if GLOBALS.GetPlanningMode() == True:
            self.planner.do_command(cmd, *cmdArgs)                
        else:
            return self.DoCommand_Acting(cmd, cmdArgs)

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
        if not UsesSharedQueues(domain):
            cmdThread = threading.Thread(target=self.beginCommand, args = [cmd, cmdRet, cmdArgs])
            cmdThread.start()
        else:
            newCmdId = self.GetNewId()
            # Update which stack a new command belongs to
            self.cmdStackTable[newCmdId] = self.raeLocals.GetStackId()
            print("RAE1Stack: ", cmd)
            self.cmdExecQueue.put([newCmdId, cmd.__name__, cmdArgs])

        if cmd.__name__ in self.raeLocals.GetCommandCount():
            self.raeLocals.GetCommandCount()[cmd.__name__] += 1
        else:
            self.raeLocals.GetCommandCount()[cmd.__name__] = 1

        self.ipcArgs.EndCriticalRegion()
        self.ipcArgs.BeginCriticalRegion(self.raeLocals.GetStackId())

        if not UsesSharedQueues(domain):
            while (cmdRet['state'] == 'running'):
                if self.verbosity > 0:
                    print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

                self.ipcArgs.EndCriticalRegion()
                self.ipcArgs.BeginCriticalRegion(self.raeLocals.GetStackId())
        else:
            while not self.cmdStatusStack[self.raeLocals.GetStackId()]:
                if self.verbosity > 0:
                    print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

                self.ipcArgs.EndCriticalRegion()
                self.ipcArgs.BeginCriticalRegion(self.raeLocals.GetStackId())

        if self.verbosity > 0:
            print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

        if not UsesSharedQueues(domain):
            retcode = cmdRet['state']
        else:
            [id, retcode, nextState] = self.cmdStatusStack[self.raeLocals.GetStackId()]
            assert(retcode == 'Success' or retcode == 'Failure')
            self.RestoreState(nextState)

        par, cmdNode = self.raeLocals.GetCurrentNodes()

        cmdNode.SetLabelAndType(cmd, 'command', cmdArgs)

        cmdNode.SetNextState(self.state.copy())

        if self.verbosity > 1:
            print('Command {}{} returned {}'.format(cmd.__name__, cmdArgs, retcode))
            print('Current state is')
            PrintState()

        if cmd.__name__ == "fail" or retcode == 'Failure':
            util1 = self.GetFailureUtility(cmd, cmdArgs)
            self.raeLocals.AddToPlanningUtilityList('fail')
            eff1 = self.GetFailureEfficiency(cmd, cmdArgs)
        else:
            util1 = self.GetUtility(cmd, cmdArgs)
            eff1 = self.GetEfficiency(cmd, cmdArgs)
            wait = False

            if self.domain == "deliver": # to avoid overflow in output files
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
        self.raeLocals.SetEfficiency(self.AddEfficiency(eff1, self.raeLocals.GetEfficiency()))

        if retcode == 'Failure':
            raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
        elif retcode == 'Success':
            return retcode
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

    # def CallCommand_OperationalModel(self, cmd, cmdArgs):
    #     self.v_begin_c(cmd, cmdArgs)
    #     cmdRet = {'state':'running'}
    #     #cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    #     #cmdThread.start()
    #
    #     self.beginCommand(cmd, cmdRet, cmdArgs)
    #     #if GLOBALS.GetPlanningMode() == False:
    #     #    self.ipcArgs.EndCriticalRegion()
    #     #    self.ipcArgs.BeginCriticalRegion(planLocals.GetStackId())
    #
    #     #while (cmdRet['state'] == 'running'):
    #     #    if self.verbosity > 0:
    #     #        print_stack_size(planLocals.GetStackId(), path)
    #     #        print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
    #     #    if GLOBALS.GetPlanningMode() == False:
    #     #        self.ipcArgs.EndCriticalRegion()
    #     #        self.ipcArgs.BeginCriticalRegion(planLocals.GetStackId())
    #
    #     if self.verbosity > 0:
    #         print('Command {}{} is done'.format( cmd.__name__, cmdArgs))
    #
    #     retcode = cmdRet['state']
    #     if self.verbosity > 1:
    #         print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
    #         print('Current state is')
    #         PrintState()
    #
    #     return retcode

    def IndexOf(self, s, l):
        """ Helper function of PlanCommand_RAEPlan """
        i = 0
        for item in l:
            if item.EqualTo(s):
                return i
            i += 1 
        return -1

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
        if GLOBALS.GetUtility() == UTIL.EFFICIENCY:
            return Utility(1/20)
        elif GLOBALS.GetUtility() == UTIL.COST_EFFECTIVENESS:
            return Utility(1/20 + 1/20)
        else:
            return Utility("Failure")


    def GetUtilityforMethod(self, cost):
        if GLOBALS.GetUtility() == UTIL.SUCCESS_RATIO:
            return Utility("Success")
        elif GLOBALS.GetUtility() == UTIL.EFFICIENCY:
            return Utility(1/cost)
        elif GLOBALS.GetUtility() == UTIL.COST_EFFECTIVENESS:
            return Utility(1/20 + 1/cost)
        
    def GetFailureEfficiency(self, cmd, cmdArgs):
        return 1/20

    def GetEfficiency(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "nav" and cmd.__name__ == "helpRobot": # kluge because I forgot to add this cost in the auto-gen problems
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
    
    def GetUtility(self, cmd, cmdArgs):
        assert(cmd.__name__ != "fail")
        if self.domain == "nav" and cmd.__name__ == "helpRobot":
            # kluge because I forgot to add this cost in the auto-gen problems
            cost = 7
        else:
            cost = DURATION.COUNTER[cmd.__name__]
        if GLOBALS.GetUtility() == UTIL.SUCCESS_RATIO:
            return Utility("Success")
        
        if type(cost) == types.FunctionType:
            numpy.random.seed(5000)
            res = cost(*cmdArgs)
        else:
            res = cost

        if GLOBALS.GetUtility() == UTIL.EFFICIENCY:
            return Utility(1/res)
        elif GLOBALS.GetUtility() == UTIL.COST_EFFECTIVENESS:
            return Utility(1/20 + 1/res)
        else:
            print("ERROR: Invalid utility")
            exit()
            
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

