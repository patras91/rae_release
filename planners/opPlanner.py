__author__ = 'patras'
from timer import SetMode
import GLOBALS
from dataStructures import PlanArgs
import signal
import rTree
from exceptions import *

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

    def GetCandidates(self, task, tArgs):
        """ Called from DoTaskRAEPlan and DoTaskUPOM"""
        if self.planLocals.GetCandidates() != None:
            # when candidates is a subset of the applicable methods, it is available from planLocals
            candidates = self.planLocals.GetCandidates()[:]
            self.planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
            prevState = self.planLocals.GetState()
            flag = 1
        else:
            print(" in the other ")
            candidateMethods = self.methods[task][:] # set of applicable methods
            candidates = self.GetMethodInstances(candidateMethods, tArgs)
            prevState = state
            flag = 0
            
        # b = max(1, GLOBALS.Getb() - int(planLocals.GetDepth() / 4))
        if self.name == "UPOM":
            cand = candidates
        elif self.name == "RAEPlan":
            b = GLOBALS.Getb()
            cand = candidates[0:min(b, len(candidates))]
        return cand, prevState, flag

    def CallMethod_OperationalModel(self, stackid, m, taskArgs):
        retcode = 'Failure'
        try:
            m.Call()  # This is the main job of this function, CallMethod
            retcode = 'Success'
        except Failed_command as e:
        	pass
        except Failed_task as e:
            pass
        return retcode

    def DoMethod(self, m, task, taskArgs):
        savedNode = self.planLocals.GetCurrentNode()
        
        newNode = rTree.PlanningTree(m, taskArgs, 'method')
        savedNode.AddChild(newNode)
        self.planLocals.SetCurrentNode(newNode)

        retcode = self.CallMethod_OperationalModel(self.planLocals.GetStackId(), m, taskArgs)


        if retcode == 'Failure':
            print("Error: retcode should not be Failure inside DoMethod.\n")
            raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))
        elif retcode == 'Success':
            if m.cost > 0:
                util = self.GetUtilityforMethod(m.cost)
            else:
                util = Utility('Success')
            for child in savedNode.children:
                util = util + child.GetUtility()
            savedNode.SetUtility(util)
            self.planLocals.SetCurrentNode(savedNode)

            return self.planLocals.GetPlanningTree()
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

    