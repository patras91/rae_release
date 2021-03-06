__author__ = 'patras'

from actors.RAE.RAE1Stack import RAE1
from shared.timer import globalTimer
import threading
from shared import GLOBALS
from learning.learningData import WriteTrainingData
import multiprocessing as mp
import importlib

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
    def __init__(self, domain, problem, useLearningStrategy, planner, plannerParams, v, state, rv, RestoreState, GetDomainState):
        self.verbosity = v

        self.taskQueue = mp.Queue() # where the tasks come in
        self.cmdExecQueue = mp.Queue() # where commands go out
        self.cmdStatusQueue = mp.Queue() # where the status of commands come in
        self.cmdStatusStack = {} # where the command statuses are saved after reading from cmdStatusQueue

        self.cmdStackTable = {} # keeps track of which command belongs to which stack/job

        self.TASKS = {} # dictionary of tasknames and the task parameters
        self.methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file

        self.heuristic = {}

        self.ipcArgs = IpcArgs() # for inter stack (thread) control transfer
        self.envArgs = EnvArgs() # for control transfer between environment and stacks; checks for events in the env

        self.state = state # only used via RAE1
        self.rv = rv
        self.RestoreState = RestoreState
        self.GetDomainState = GetDomainState

        self.InitializeDomain(domain, problem)

        self.rae1Instances = {} # dictionary mapping stack ids to the rae1 objects
        self.useLearningStrategy = useLearningStrategy
        self.planner = planner
        self.plannerParams = plannerParams

    def InitializeDomain(self, domain, problem, startState=None):
        '''
        :param domain: code of the domain which you are running
        :param problem: id of the problem
        :return:none
        '''
        
        self.domain = domain
        if domain in ['AIRS_dev', 'Mobipick']:
            pass
        else:
            module = 'domains.' + domain + '.problems.auto.' + problem + '_' + domain
            print("Importing ", module)
            self.problemModule = importlib.import_module(module)
            self.problemModule.SetInitialStateVariables(self.state, self.rv)

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
            if threadList[j-1].is_alive() == True:
                nextAlive = j
                break
            i = i + 1
            j = j % numstacks + 1

        return nextAlive

    def noNewTasks(self):
        if self.domain in ['AIRS_dev', 'Mobipick']:
            return False
        for c in self.problemModule.tasks:
            if c > self.newTasksCounter:
                return False
        return True

    def GetNewTasks(self):
        '''
        :return: gets the new task that appears in the problem at the current time
        '''
        self.newTasksCounter += 1
        if self.domain not in  ['AIRS_dev', 'Mobipick']:
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
            if threadList[i - 1].isAlive():
                begin = False
                break
            i = i % numstacks + 1
        return begin

    def CreateNewStack(self, taskInfo, raeArgs):
        stackid = raeArgs.stack
        rae1 = RAE1(
            raeArgs.task,
            raeArgs, 
            self.domain, 
            self.ipcArgs, 
            self.cmdStatusStack,
            self.cmdStackTable,
            self.cmdExecQueue,
            self.verbosity, 
            self.state, 
            self.methods,
            self.heuristic,
            self.useLearningStrategy,
            self.planner, 
            self.plannerParams, 
            self.RestoreState, 
            self.GetDomainState
        )
        self.rae1Instances[stackid] = rae1
        retcode, retryCount, eff, height, taskCount, commandCount, traces, utilVal, utilitiesList = rae1.RAE1Main(raeArgs.task, raeArgs)
        taskInfo[stackid] = ([raeArgs.task] + raeArgs.taskArgs, retcode, retryCount, eff, height, taskCount, commandCount, traces, utilVal, utilitiesList)

    def PrintResult(self, taskInfo):
        output = "\nRESULTS:"
        for stackid in taskInfo:
            args, res, retryCount, eff, height, taskCount, commandCount, traces, utilVal, utilitiesList = taskInfo[stackid]
            output += '\n Task : ' +  '\t{}{}'.format(args[0], args[1:]) + \
                '\n Result : \t' + str(res) + \
                '\n Retry Count: \t' + str(retryCount) + \
                '\n Utility: \t' + str(eff) + \
                "\n -----------------\n"
        return output

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
            args, res, retryCount, eff, height, taskCount, commandCount, traces, utilVal, utilitiesList = taskInfo[stackid]
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

#            with open("traces.txt", "a") as f:
#                f.write("\n\n")
#                f.write(traces)

            #print(' '.join('-'.join([key, str(cmdNet[key])]) for key in cmdNet))

    def StartEnv(self):
        while True:
            self.envArgs.sem.acquire()
            if self.envArgs.exit:
                self.ipcArgs.sem[0].release() # main controller
                return

            self.startEnvCounter += 1
            if self.domain not in ["AIRS_dev", "Mobipick", "AIRS"]:
                if self.startEnvCounter in self.problemModule.eventsEnv:
                    eventArgs = self.problemModule.eventsEnv[self.startEnvCounter]
                    event = eventArgs[0]
                    eventParams = eventArgs[1]
                    t = threading.Thread(target=event, args=eventParams)
                    t.setDaemon(True)  # Setting the environment thread to daemon because we don't want the environment running once the tasks are done
                    t.start()
            self.ipcArgs.sem[0].release()

    def add_tasks(self, tasks):
        current_counter = self.newTasksCounter
        if current_counter + 1 not in self.problemModule.tasks:
            self.problemModule.tasks[current_counter + 1] = tasks
        else:
            self.problemModule.tasks[current_counter + 1] += tasks

    def raeMult(self, outputQueue=None):
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
                if numstacks == 0 or self.BeginFreshIteration(lastActiveStack, numstacks, self.ipcArgs.threadList):
                    # Check for incoming tasks after progressing all stacks
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

                    if self.domain in ["AIRS", "AIRS_dev"]:
                        self.UpdateCommandStatus()
                    globalTimer.IncrementTime()

                if numstacks > 0:
                    res = self.GetNextAlive(lastActiveStack, numstacks, self.ipcArgs.threadList)

                    if res != -1:
                        self.ipcArgs.nextStack = res
                        lastActiveStack = res
                        self.ipcArgs.sem[res].release()
                    else:
                        if self.noNewTasks():
                            self.envArgs.exit = True
                            self.envArgs.sem.release()
                            break
                        else:
                            self.ipcArgs.sem[0].release()
                else:
                    self.ipcArgs.sem[0].release()

            WriteTrainingData()
        if self.verbosity > 0:
            print("----Done with RAE----\n")
        else:
            self.PrintResultSummaryVersion2(taskInfo)
            #globalTimer.Callibrate(startTime)

        if outputQueue:
            outputQueue.put(self.PrintResult(taskInfo))

        return taskInfo # for unit tests



    def do_task(self, task, *taskArgs):
        # the current active stack do_task
        currentStackId = self.ipcArgs.nextStack
        self.rae1Instances[currentStackId].do_task(task, *taskArgs)

    def do_command(self, cmd, *cmdArgs):
        # the current active stack do_task
        currentStackId = self.ipcArgs.nextStack
        self.rae1Instances[currentStackId].do_command(cmd, *cmdArgs)

    # RAE reads the cmdStatusQueue and updates the cmdStatusStack  
    def UpdateCommandStatus(self):
        while(self.cmdStatusQueue.empty() == False):
            (id, res, nextState) = self.cmdStatusQueue.get()
            stackid = self.cmdStackTable[id]
            self.cmdStatusStack[stackid] = (id, res, nextState)

    def declare_task(self, t, *args):
        self.TASKS[t] = args

    # declares the refinement methods for a task;
    # ensuring that some constraints are satisfied
    def declare_methods(self, task_name, *method_list):
        self.methods[task_name] = []
        for m in method_list:
            self.add_new_method(task_name, m)
            
    def add_new_method(self, task_name, m):
        taskArgs = self.TASKS[task_name]
        q = len(taskArgs)
        variableArgs = False
        if len(taskArgs) == 1:
            if taskArgs[0] == "*":
                variableArgs = True
        if variableArgs != True:
            # ensure that the method has atleast as many parameters as the task
            assert(m.__code__.co_argcount - 1 >= q)
            
            # ensure that the variable names of the 
            # first q parameters of m match with the parameters of task t
            assert(m.__code__.co_varnames[1:q+1] == taskArgs)


        self.methods[task_name].append(m)

        #print(self.methods['fix_component'])

    def declare_heuristic(self, task, name):
        self.heuristic[task] = name

    def declare_goal_method(self, method, goalState):
        # TODO
        # save the methods and corresponding states in a dict
        pass
        