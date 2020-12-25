__author__ = 'patras'
from timer import SetMode
import GLOBALS
from dataStructures import PlanArgs
import signal
import rTree

class OpPlanner(): # Operational Planner; Planner that uses Operational Models
    def __init__(self):
        self.HandleTerminationQueue = None 

    def InitializePlanningTree(self):
        root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
        self.planLocals.SetCurrentNode(root)
        self.planLocals.SetPlanningTree(root)

    def CallPlanner(self, pArgs, queue):
        """ Calls the planner according to what the user decided."""
        if self.name == "UPOM":

            self.HandleTerminationQueue = queue
            signal.signal(signal.SIGTERM, self.HandleTermination)
            
            if GLOBALS.GetDoIterativeDeepening() == True:
                d = 5
                while(d <= self.maxSearchDepth):
                    pArgs.SetDepth(d)
                    methodUtil, planningTime = self.UPOMChoiceMain(pArgs.GetTask(), pArgs)
                    method, util = methodUtil
                    d += 5
            else:
                d = self.maxSearchDepth
                pArgs.SetDepth(d)
                methodUtil, planningTime = self.UPOMChoiceMain(pArgs.GetTask(), pArgs)
                method, util = methodUtil

        elif self.name == "RAEPlan":

            pArgs.SetDepth(GLOBALS.GetMaxDepth())
            methodUtil, planningTime = self.RAEPlanChoiceMain(pArgs.GetTask(), pArgs)
            method, util = methodUtil

        else:
            print("Invalid planner")


        queue.put((method, util, planningTime))

    def Main(self, task, taskArgs, queue, candidateMethods, state, aTree, curUtil):

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

    def HandleTermination(self, signalId, frame):
        methodUtil, planningTime = GetBestTillNow()
        method, util = methodUtil
        self.HandleTerminationQueue.put((method, util, planningTime))
        sys.exit()
    