goalChecks = {}

def declare_goalCheck(task, goalCheckMethod):
    goalChecks[task] = goalCheckMethod

def RunUCTwithCommandsOnlyMain(task, taskArgs, state, queue):

    root = rTree.CommandSearchTreeNode(state.copy() , 'state', None)

    plan = []
    for i in range(GLOBALS.GetUCTRuns()):
        print("rollout ", i)
        RestoreState(state)
        planLocals.SetSearchTreeNode(root)
        planLocals.SetUtilRollout(Utility("Success"))
        DoOneRollout(task, taskArgs)

    queue.put(plan)


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
    if goalCheck() == True:
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
    beginCommand(c, cmdRet, [])
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
        util2 = GetUtility(c, []) # cmdArgs
        planLocals.SetUtilRollout(util1 + util2)
        nSN.SetUtility(GetUtility(c, [])) # cmdArgs
        planLocals.SetSearchTreeNode(nSN)
        DoOneRollout(task, taskArgs)
        curNode.Q[index] = Utility((curNode.Q[index].GetValue() * \
                                curNode.n[index] + \
                                planLocals.GetUtilRollout().GetValue()) / \
                            (curNode.n[index] + 1))
        curNode.n[index] += 1
