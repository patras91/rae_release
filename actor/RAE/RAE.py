__author__ = 'patras'
#from RAE1_and_RAEplan import ipcArgs, envArgs, RAEplan_Choice, UPOM_Choice, GetBestTillNow
from RAE1Stack import RAE1
from dataStructures import PlanArgs
from timer import globalTimer, SetMode
from state import RemoveLocksFromState, RestoreState
import threading
import GLOBALS
import os
from learningData import WriteTrainingData
import signal
import sys
import multiprocessing as mp
from UPOM import UPOMChoice
from RAEPlan import RAEPlanChoice
from APEPlan import APEPlanChoice

#****************************************************************
#To control Progress of each stack step by step
class IpcArgs():
    def __init__(self):
        self.sem = [threading.Semaphore(1)]  #the semaphores to control progress of each stack and master
        self.nextStack = 0                 #the master thread is the next in line to be executed, master thread adds a new stack for every new incoming task
        self.threadList = [] #keeps track of all the stacks in RAE's Agenda

    def BeginCriticalRegion(self, stackid):
        #while(ipcArgs.nextStack != stackid):
        #    pass
        self.sem[stackid].acquire()

    def EndCriticalRegion(self):
        #ipcArgs.nextStack = 0
        self.sem[0].release()

class EnvArgs():
    def __init__(self):
        self.sem = threading.Semaphore(0)
        self.exit = False

#****************************************************************

class rae():
    def __init__(self, domain, problem, planner, plannerParams, showOutputs, v, state, rv):
        self.showOutputs = showOutputs
        self.verbosity = v

        self.taskQueue = mp.Queue() # where the tasks come in
        self.cmdExecQueue = mp.Queue() # where commands go out
        self.cmdStatusQueue = mp.Queue() # where the status of commands come in
        self.cmdStatusStack = {} # where the command statuses are saved after reading from cmdStatusQueue

        self.cmdStackTable = {} # keeps track of which command belongs to which stack/job

        self.TASKS = {} # dictionary of tasknames and the task parameters
        self.commands = {} # dictionary of commands, initialized once for every run via the domain file
        self.methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file

        self.heuristic = {}

        self.ipcArgs = IpcArgs() # for inter stack (thread) control transfer
        self.envArgs = EnvArgs() # for control transfer between environment and stacks; checks for events in the env

        self.state = state # only used via RAE1
        self.rv = rv

        self.InitializePlanner(planner, plannerParams)
        self.InitializeDomain(domain, problem)

    def InitializePlanner(self, p, params):
        print(params)
        if p == "APEPlan":
            self.planner = APEPlanChoice(params)
        elif p == "RAEPlan":
            self.planner = RAEPlanChoice(params)
        elif p == "UPOM":
            self.planner = UPOMChoice(params)
        elif p == "None" or p == None:
            self.planner = None 
        else:
            print("Invalid planner. Please select from [APEPlan, RAEPlan, UPOM, None]")
            exit()

    def InitializeDomain(self, domain, problem, startState=None):
        '''
        :param domain: code of the domain which you are running
        :param problem: id of the problem
        :return:none
        '''
        
        self.domain = domain
        if domain in ['fetch', 'nav', 'explore', 'rescue', 'deliver', 'testInstantiation', 'testSSU',  'testMethodswithCosts', "AIRS"]:
            module = problem + '_' + domain
            self.problemModule = __import__(module)
            self.problemModule.SetInitialStateVariables(self.state, self.rv)
        elif domain == 'AIRS_dev':
            RestoreState(startState)
        else:
            print("Invalid domain\n", domain)
            exit(11)

    def GetNextAlive(self, lastActiveStack, numstacks, threadList):
        '''
        :param lastActiveStack: the stack which was progressed before this
        :param numstacks: total number of stacks in the Agenda
        :param threadList: list of all the threads, each running a RAE stack
        :return: The stack which should be executed next
        '''
        nextAlive = -1
        i = 1
        j = lastActiveStack % numstacks + 1
        while i <= numstacks:
            if threadList[j-1].isAlive() == True:
                nextAlive = j
                break
            i = i + 1
            j = j % numstacks + 1

        return nextAlive

    def noNewTasks(self):
        if self.domain == 'AIRS_dev':
            return False
        for c in self.probleModule.tasks:
            if c > self.newTasksCounter:
                return False
        return True

    def GetNewTasks(self):
        '''
        :return: gets the new task that appears in the problem at the current time
        '''
        self.newTasksCounter += 1
        if self.domain != 'AIRS_dev':
            if self.newTasksCounter in self.problemModule.tasks:
                return self.problemModule.tasks[self.newTasksCounter]
            else:
                return []
        else:
            tasks = []
            while not self.taskQueue.empty():
                tasks.append(self.taskQueue.get())
            return tasks

    def BeginFreshIteration(self, lastActiveStack, numstacks, threadList):
        begin = True
        i = lastActiveStack % numstacks + 1
        while i != 1:
            if threadList[i - 1].isAlive() == True:
                begin = False
                break
            i = i % numstacks + 1
        return begin

    def CreateNewStack(self, taskInfo, raeArgs):
        stackid = raeArgs.stack
        rae1 = RAE1(raeArgs.task, raeArgs, self.domain, self.ipcArgs, self.cmdStatusStack, self.verbosity, self.state, self.methods)
        retcode, retryCount, eff, height, taskCount, commandCount, utilVal, utilitiesList = rae1.RAE1Main(raeArgs.task, raeArgs)
        taskInfo[stackid] = ([raeArgs.task] + raeArgs.taskArgs, retcode, retryCount, eff, height, taskCount, commandCount, utilVal, utilitiesList)

    def PrintResult(self, taskInfo):
        print('ID ','\t','Task',
                '\t\t\t', 'Result',
                '\t\t\t', 'Retry Count', 
                '\t\t\t', 'Efficiency', 
                '\t\t\t', 'height',
                '\t\t\t', '#tasks',
                '\t\t\t', '#commands',
                '\t\t\t'
                '\n')
        for stackid in taskInfo:
            args, res, retryCount, eff, height, taskCount, commandCount, utilVal, utilitiesList = taskInfo[stackid]
            
            print(stackid,'\t','Task {}{}'.format(args[0], args[1:]),
                '\t\t\t', res,
                '\t\t\t', retryCount, 
                '\t\t\t', eff, 
                '\t\t\t', height,
                '\t\t\t', taskCount,
                '\t\t\t', commandCount,
                '\t\t\t', utilVal,
                '\n')
            print(stackid, '\t', 'Task {}{}'.format(args[0], args[1:]),
                '\t')

            utilString = ""
            for u in utilitiesList:
                utilString += str(u)  
                utilString += ","

            print(utilString)

    def PrintResultSummaryVersion1(self, taskInfo):
        succ = 0
        fail = 0
        retries = 0
        effTotal = 0
        h = 0
        t = 0
        c = 0
        for stackid in taskInfo:
            args, res, retryCount, eff, height, taskCount, commandCount = taskInfo[stackid]
            if res == 'Success':
                succ += 1
            else:
                fail += 1
            retries += retryCount
            effTotal += eff.GetValue()
            c += commandCount
            t += taskCount
            if height > h:
                h = height
        print(succ, succ+fail, retries, globalTimer.GetSimulationCounter(), globalTimer.GetRealCommandExecutionCounter(), effTotal, h, t, c)
        #print(' '.join('-'.join([key, str(cmdNet[key])]) for key in cmdNet))

    def PrintResultSummaryVersion2(self, taskInfo):
        for stackid in taskInfo:
            args, res, retryCount, eff, height, taskCount, commandCount, utilVal, utilitiesList = taskInfo[stackid]
            if res == 'Success':
                succ = 1
                fail = 0
            else:
                succ = 0
                fail = 1
            print("v2", succ, succ+fail, retryCount, globalTimer.GetSimulationCounter(), 
                globalTimer.GetRealCommandExecutionCounter(), eff, height, taskCount, commandCount, utilVal)
            utilString = ""
            for u in utilitiesList:
                utilString += str(u)  
                utilString += " "

            print(utilString)

            #print(' '.join('-'.join([key, str(cmdNet[key])]) for key in cmdNet))


    def StartEnv(self):
        while(True):
            self.envArgs.sem.acquire()
            if self.envArgs.exit == True:
                self.ipcArgs.sem[0].release() # main controller
                return

            self.startEnvCounter += 1
            if self.domain != "AIRS":
                if self.startEnvCounter in self.problemModule.eventsEnv:
                    self.eventArgs = self.problemModule.eventsEnv[self.startEnvCounter]
                    event = eventArgs[0]
                    eventParams = eventArgs[1]
                    t = threading.Thread(target=event, args=eventParams)
                    t.setDaemon(True)  # Setting the environment thread to daemon because we don't want the environment running once the tasks are done
                    t.start()
            self.ipcArgs.sem[0].release()

    def add_tasks(self, tasks):
        current_counter = self.newTasksCounter
        if current_counter + 1 not in self.problemModule.tasks:
            problemModule.tasks[current_counter + 1] = tasks
        else:
            problemModule.tasks[current_counter + 1] += tasks

    def raeMult(self):
        lastActiveStack = 0 #keeps track of the last stack that was Progressed
        numstacks = 0 #keeps track of the total number of stacks
        self.newTasksCounter = 0
        self.startEnvCounter = 0
        taskInfo = {}

        envThread = threading.Thread(target=self.StartEnv)
        #startTime = time()
        envThread.start()


        while (True):
            #if ipcArgs.nextStack == 0 or ipcArgs.threadList[ipcArgs.nextStack-1].isAlive() == False:
            if True:
                self.ipcArgs.sem[0].acquire()
                if numstacks == 0 or self.BeginFreshIteration(lastActiveStack, numstacks, self.ipcArgs.threadList) == True: # Check for incoming tasks after progressing all stacks

                    taskParams = self.GetNewTasks()
                    if taskParams != []:

                        for newTask in taskParams:
                            numstacks = numstacks + 1
                            raeArgs = GLOBALS.RaeArgs()
                            raeArgs.stack = numstacks
                            raeArgs.task = newTask[0]
                            raeArgs.taskArgs = newTask[1:]

                            self.ipcArgs.sem.append(threading.Semaphore(0))
                            self.ipcArgs.threadList.append(threading.Thread(target=self.CreateNewStack, args = (taskInfo, raeArgs)))
                            self.ipcArgs.threadList[numstacks-1].start()

                    lastActiveStack = 0 # for the environment
                    self.envArgs.sem.release()
                    self.ipcArgs.sem[0].acquire()

                    if self.domain == "AIRS":
                        self.UpdateCommandStatus()
                    globalTimer.IncrementTime()

                if numstacks > 0:
                    res = self.GetNextAlive(lastActiveStack, numstacks, self.ipcArgs.threadList)

                    if res != -1:
                        self.ipcArgs.nextStack = res
                        lastActiveStack = res
                        self.ipcArgs.sem[res].release()
                    else:
                        if noNewTasks():
                            self.envArgs.exit = True
                            self.envArgs.sem.release()
                            break
                else:
                    self.ipcArgs.sem[0].release()

            WriteTrainingData()
        if self.showOutputs == 'on':
            print("----Done with RAE----\n")
            PrintResult(taskInfo)
        else:
            PrintResultSummaryVersion2(taskInfo)
            #globalTimer.Callibrate(startTime)

        return taskInfo # for unit tests

    def HandleTermination(self, signalId, frame):
        methodUtil, planningTime = GetBestTillNow()
        method, util = methodUtil
        HandleTermination.q.put((method, util, planningTime))
        sys.exit()
    HandleTermination.q = None 

    def CallPlanner(self, pArgs, queue):
        """ Calls the planner according to what the user decided."""
        if self.planner.name == "UPOM":

            HandleTermination.q = queue
            signal.signal(signal.SIGTERM, HandleTermination)
            
            if GLOBALS.GetDoIterativeDeepening() == True:
                d = 5
                while(d <= GLOBALS.GetMaxDepth()):
                    pArgs.SetDepth(d)
                    methodUtil, planningTime = UPOM_Choice(pArgs.GetTask(), pArgs)
                    method, util = methodUtil
                    d += 5
            else:
                d = GLOBALS.GetMaxDepth()
                pArgs.SetDepth(d)
                methodUtil, planningTime = UPOM_Choice(pArgs.GetTask(), pArgs)
                method, util = methodUtil

        elif self.planner.name == "RAEPlan":

            pArgs.SetDepth(GLOBALS.GetMaxDepth())
            methodUtil, planningTime = RAEplan_Choice(pArgs.GetTask(), pArgs)
            method, util = methodUtil

        else:
            print("Invalid planner")


        queue.put((method, util, planningTime))

    def PlannerMain(self, task, taskArgs, queue, candidateMethods, state, aTree, curUtil):

        SetMode('Counter') #Counter mode in simulation
        GLOBALS.SetPlanningMode(True)
        #RemoveLocksFromState()

        pArgs = PlanArgs()

        pArgs.SetStackId(1) # Simulating one stack now
        # TODO: Simulate multiple stacks in future
        
        pArgs.SetTask(task)
        pArgs.SetTaskArgs(taskArgs)
        pArgs.SetCandidates(candidateMethods)

        pArgs.SetState(state)
        pArgs.SetActingTree(aTree)
        pArgs.SetCurUtil(curUtil)

        self.CallPlanner(pArgs, queue)

        WriteTrainingData() # data to be used for learning


    def do_task(self):
        # the current active stack do_task

    # RAE updates which stack a new command belongs to 
    def AddToCommandStackTable(self, cmdid, stackid):
        self.cmdStackTable[cmdid] = stackid

    # RAE reads the cmdStatusQueue and updates the cmdStatusStack  
    def UpdateCommandStatus(self):
        while(self.cmdStatusQueue.empty() == False):
            (id, res, nextState) = self.cmdStatusQueue.get()
            stackid = self.cmdStackTable[id]
            self.cmdStatusStack[stackid] = (id, res, nextState)

    def declare_commands(self, cmd_list):
        """
        Call this after defining the commands, to tell APE and APE-plan what they are.
        cmd_list must be a list of functions, not strings.
        """
        self.commands.update({cmd.__name__:cmd for cmd in cmd_list})

    def declare_task(self, t, *args):
        self.TASKS[t] = args

    # declares the refinement methods for a task;
    # ensuring that some constraints are satisfied
    def declare_methods(self, task_name, *method_list):

        taskArgs = self.TASKS[task_name]
        q = len(taskArgs)
        
        self.methods[task_name] = []
        for m in method_list:

            variableArgs = False
            if len(taskArgs) == 1:
                if taskArgs[0] == "*":
                    variableArgs = True
            if variableArgs != True:
                # ensure that the method has atleast as many parameters as the task
                assert(m.__code__.co_argcount - 1 >= q)
                
                # ensure that the variable names of the 
                # first q parameters of m match with the parameters of task t
                print(m.__code__.co_varnames, taskArgs)
                assert(m.__code__.co_varnames[1:q+1] == taskArgs)

            self.methods[task_name].append(m)

    def declare_heuristic(self, task, name):
        self.heuristic[task] = name
        