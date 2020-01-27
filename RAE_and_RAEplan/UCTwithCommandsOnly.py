__author__="__patras__"

import multiprocessing
from state import RestoreState, GetState
import rTree
import GLOBALS
from utility import Utility
from dataStructures import rL_PLAN
import random
from timer import DURATION
import types

goalChecks = {}
commands = {}
planLocals = rL_PLAN()

class PlanM():
    def __init__(self, p):
        self.plan = p
        print("PLAN")
        print(self.plan)

    def Call(self):
        for item in self.plan:
            print("Doing ", item.__name__)
            RAE1_and_RAEplan.do_command(item)

def declare_commands(cmd_list):
    commands.update({cmd.__name__:cmd for cmd in cmd_list})

def declare_goalCheck(task, goalCheckMethod):
    goalChecks[task] = goalCheckMethod

def RunUCTwithCommandsOnlyMain(task, taskArgs, initState, queue):

    root = rTree.CommandSearchTreeNode(initState.copy() , 'state', None)

    for i in range(GLOBALS.GetUCTRuns()):
        print("rollout ", i)
        RestoreState(initState)
        planLocals.SetSearchTreeNode(root)
        planLocals.SetUtilRollout(Utility("Success"))
        DoOneRollout(task, taskArgs)

    sNode = root
    plan = []
    bestQ = Utility('Failure')
    bestC = "Failure"
    while(sNode.children != []):

        for i in range(0, len(sNode.Q)):
            print("(")
            if sNode.n[i] > 0:
                print(sNode.Q[i].value)
                if sNode.Q[i] > bestQ: 
                    bestQ = sNode.Q[i]
                    print(sNode.children[i].GetLabel())
                    bestC = sNode.children[i]
            print(")")
        if bestC == "Failure":
            queue.put("Failure")
            return
        plan.append(bestC.GetLabel())
        bestW = 0
        for i in range(0, len(bestC.children)):
            if bestC.childWeights[i] > bestW:
                bestW = bestC.childWeights[i]
                sNode = bestC.children[i]

    queue.put(PlanM(plan))

def RunUCTwithCommandsOnly(task, taskArgs):

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(
            target=RunUCTwithCommandsOnlyMain,
            args=[task, taskArgs, GetState(), queue])

    p.start()
    p.join(int(0.7*GLOBALS.GetTimeLimit())) # planner gets max 70% of the total time

    if p.is_alive() == True:
        p.terminate()
        return 'Failure'
    else:
        plan = queue.get()
        return plan

def DoOneRollout(task, taskArgs):
    goalCheck = goalChecks[task]
    if goalCheck(*taskArgs) == True:
        return
    curNode = planLocals.GetSearchTreeNode()
    if curNode.children == []:
        for cmd in commands.values():
            newSearchTreeNode = rTree.CommandSearchTreeNode(cmd, 'command', [])
            curNode.AddChild(newSearchTreeNode)

    untried = []

    if curNode.N == 0:
        untried = curNode.children
    else:
        for child in curNode.children:
            if child.children == []:
                untried.append(child) # command that has not been simulated yet

    if untried != []:
        cNode = random.choice(untried)
        index = curNode.children.index(cNode)
    else:
        vmax = 0
        cNode = None
        index = None
        for i in range(0, len(curNode.children)):
            v = curNode.Q[i].GetValue() + \
                GLOBALS.GetC() * math.sqrt(math.log(curNode.N)/curNode.n[i])
            if v >= vmax:
                vmax = v
                cNode = curNode.children[i]
                index = i

    c = cNode.GetLabel()

    cmdRet = {'state':'running'}
    RAE1_and_RAEplan.beginCommand(c, cmdRet, [])
    retcode = cmdRet['state']

    nextState = GetState().copy()

    if retcode == 'Failure':
        nSN = rTree.CommandSearchTreeNode(nextState, 'state', None) # next state node
        nSN.SetUtility(Utility('Failure'))
        cNode.AddChild(nSN)
        planLocals.SetUtilRollout(Utility('Failure'))
        return 
    else:
        nSN = cNode.FindAmongChildren(nextState) 
        if nSN == None:
            nSN = rTree.CommandSearchTreeNode(nextState, 'state', None)
            cNode.AddChild(nSN)
        
        util1 = planLocals.GetUtilRollout()
        util2 = RAE1_and_RAEplan.GetUtility(c, []) # cmdArgs
        planLocals.SetUtilRollout(util1 + util2)
        nSN.SetUtility(RAE1_and_RAEplan.GetUtility(c, [])) # cmdArgs
        planLocals.SetSearchTreeNode(nSN)
        DoOneRollout(task, taskArgs)
        curNode.Q[index] = Utility((curNode.Q[index].GetValue() * \
                                curNode.n[index] + \
                                planLocals.GetUtilRollout().GetValue()) / \
                            (curNode.n[index] + 1))
        print(curNode.Q[index].value)
        curNode.n[index] += 1

import RAE1_and_RAEplan
