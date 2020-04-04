__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse
from param_values import resultsFolder, Depth, UCT_max_depth, UCT_lim_depth, timeLimit, GetRAEfname, GetNewDict

def NotTimeLine(s):
    if len(s) < 7:
        return True
    elif s[2:7] == "loops" or s[2:6] == "loop":
        return False
    else:
        return True

def GetUtilities(res, domain, f_rae, param, fileName, problem): # param may be k or d

    line = f_rae.readline()
    
    utils = 0
    count = 0

    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':
            if parts[4] == problem:
                counts = f_rae.readline()
                while(NotTimeLine(counts)):
                    if counts == '':
                        break

                    parts2 = counts.split(' ')

                    if parts2[0] != "v2":
                        version = 1
                        utils += float(parts2[5])
                        count += 1
                    else:
                        version = 2
                        utils += float(parts2[6])
                        count += 1

                    if version == 2:
                        f_rae.readline() # list of commands and planning efficiencies

                    counts = f_rae.readline()
        line = f_rae.readline()

    return utils/count

chars = [str(i) for i in range(0,10)]

def UpdateCommCount(a, l, h):
    l = a if a < l else l
    h = a if a > h else h
    return l, h

def GetCountAndTime(res, domain, f, param, fileName): # param may be k or d

    line = f.readline()
    nLine = 1

    totalRuns = 0
    totalTime = 0

    nPass = 0
    nTimeOut = 0

    highestTime = 0
    problemsTimedOut = set({})

    maxCommCount = 0
    minCommCount = 0

    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':
            totalRuns += 1
            problemName = parts[4]
            #print("fname = ", fileName, " line = ", nLine)
            counts = f.readline()
            nLine += 1

            if counts[0] == "T":
                nPass += 1
            while(NotTimeLine(counts)):
                if counts == '':
                    break

                parts2 = counts.split(' ')
                version = 2 if parts2[0] == "v2" else 1

                if version == 2:
                    comms = f.readline().split() # list of commands and planning efficiencies
                    nLine += 1
                    numberOfCommands = 0
                    for item in comms:
                        if item[0] not in chars:
                            numberOfCommands += 1
                    minCommCount, maxCommCount = UpdateCommCount(numberOfCommands, minCommCount, maxCommCount)
                    

                counts = f.readline()
                nLine += 1
            # time line
            secTimeLine = counts
            #print(secTimeLine)
            parts = secTimeLine.split()

            t = float(parts[5]) / 1000 if parts[6] == "msec" else float(parts[5])
            totalTime += t

            if t == timeLimit[domain]:
                nTimeOut += 1
                problemsTimedOut.add(problemName)

            highestTime = t if t > highestTime and t < timeLimit[domain] else highestTime
                
        line = f.readline()
        nLine += 1

    return totalRuns, \
        totalTime/60, \
        nPass, \
        nTimeOut, \
        highestTime, \
        problemsTimedOut, \
        minCommCount, \
        maxCommCount 

def GetProblems(f_rae):
    line = f_rae.readline()
    p = set({})
    while(line != ''):
        parts = line.split(' ')
        if parts[0] == 'Time':
            p.add(parts[4][0:-1])
        line = f_rae.readline()
    return p

def Get_UCT_max_depth_discrepencies(res, domain):
    problems = GetProblems(open(GetRAEfname(domain)))
    #print(problems)
    #problems = {"problem1088", "problem1001"}
    res = set({})

    for p in problems:
        lastUtils = 0
        for uct in [50, 75]:
        #for uct in UCT_max_depth[domain]:
            if uct > 0:
                fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, util, uct)
                fptr = open(fname)
                utils = GetUtilities(res, domain, open(fname), uct, fname, p)
                if lastUtils > 1.5 * utils:
                    res.add((p, lastUtils, utils))
                lastUtils = utils
                fptr.close()
    print(res)
    print(len(res))

def GetProblemsAndCounts(f_rae):
    line = f_rae.readline()
    p = set({})
    count = 0
    while(line != ''):
        parts = line.split(' ')
        if parts[0] == 'Time':
            p.add(parts[4][0:-1])
            count += 1
        line = f_rae.readline()
    return p, count

def Print_Problems_and_Tasks(domain):
    f_rae = open(GetRAEfname(domain))
    line = f_rae.readline()
    p = {}
    p_count = 0
    t_count = 0
    while(line != ''):
        parts = line.split(' ')
        if parts[0] == 'Time':
            pname = parts[4][0:-1]
            p_count += 1
            if pname not in p:
                p[pname] = 0
        elif parts[0] == 'v2':
            p[pname] += 1
            t_count += 1
        line = f_rae.readline()
    
    print(p)
    print("Problems run Count = ", p_count)
    print("Tasks Count = ", t_count)

    z = round(p_count/len(p))
    print([p[pname]/z for pname in p])
    nTasks = sum([p[pname]/z for pname in p])
    print("Number of tasks is ", nTasks)

    tasks = {1:[], 2:[], 3:[]}
    for pname in p:
        tasks[int(p[pname]/z)].append(pname)
    print(tasks)

def Get_UCT_max_depth_run_counts(res, domain):
    problems, count = GetProblemsAndCounts(open(GetRAEfname(domain)))
    for uct in UCT_max_depth[domain]:
        if uct > 0:
            fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, util, uct)
            fptr = open(fname)
            count_uct, time, passCount, timeOutCount, highestTime, problems, minCommCount, maxCommCount = \
                GetCountAndTime(res, domain, open(fname), uct, fname)
            print("Domain ", domain, \
                "uctCount = " , uct, \
                "expected ", count, \
                "found ", count_uct, \
                " time = ", time, \
                " passCount = ", passCount, \
                " timeOutCount = ",timeOutCount, \
                " highest count = ", highestTime)
            print("min Comm = ", minCommCount, " max Comm = ", maxCommCount)
            print(problems)
            fptr.close()
    print(res)
    print(len(res))

def Get_UCT_lim_depth_run_counts(res, domain):
    problems, count = GetProblemsAndCounts(open(GetRAEfname(domain)))
    for uct in UCT_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth > 0:
                fname = '{}{}_v_journal{}/rae_plan_uct_{}_d_{}_h_h0.txt'.format(resultsFolder, domain, util, uct, depth)
                fptr = open(fname)
                count_uct, time, passCount, timeOutCount, highestTime, problems, minCommCount, maxCommCount = \
                    GetCountAndTime(res, domain, open(fname), uct, fname)
                print("Domain ", domain, \
                    "depth = " , depth, \
                    "expected ", count, \
                    "found ", count_uct, \
                    " time = ", time, \
                    " passCount = ", passCount, \
                    " timeOutCount = ",timeOutCount,\
                    " highest count = ", highestTime)
                print("min Comm = ", minCommCount, " max Comm = ", maxCommCount)
                print(problems)
                fptr.close()

def Populate_UCT_max_depth_planning_utilities(res, domain):
    for uct in UCT_max_depth[domain]:
        if uct == 0:
            f_rae_name = GetRAEfname(domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelper_UCT_max_depth_planning_utilities(res[uct], domain, f_rae, uct, f_rae_name)
            f_rae.close()
        else:
            fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, util, uct)
            fptr = open(fname)
            print(fname)
            PopulateHelper_UCT_max_depth_planning_utilities(res[uct], domain, open(fname), uct, fname)
            fptr.close()

def Populate_UCT_lim_depth(res, domain):  
    for uct in UCT_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth == 0:
                f_rae_name = GetRAEfname(domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper_UCT_lim_depth(res[uct], domain, f_rae, depth, f_rae_name)
                f_rae.close()
            else:
                fname = '{}{}_v_journal{}/rae_plan_uct_{}_d_{}.txt'.format(resultsFolder, domain, util, uct, depth)
                fptr = open(fname)
                print(fname)
                PopulateHelper_UCT_lim_depth(res[uct], domain, open(fname), depth, fname)
                fptr.close()

def GetData_UCT_max_depth():
    resDict = {}
    for domain in D:
        resDict[domain] = GetNewDict()
        #Get_UCT_max_depth_discrepencies(resDict[domain], domain)
        Get_UCT_max_depth_run_counts(resDict[domain], domain)

def GetData_UCT_lim_depth():
    resDict = {
        'SD': {},
        'EE': {},
        'CR': {},
        'SR': {},
        'OF': {},
    }

    for domain in D:
        resDict[domain] = {}
        for uct in UCT_lim_depth[domain]:
            resDict[domain][uct] = GetNewDict()
    for d in D:
        Get_UCT_lim_depth_run_counts(resDict[d], d)

D = None
heuristic = None
util = None

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SD', 'SR', 'OF', 'EE']",
                           type=str, required=True)
    args = argparser.parse_args()
    D = [args.domain]
    Print_Problems_and_Tasks(D[0])
    for depth in ['max']: #, 'lim']:
        for util in [ '_eff', '_sr']:
            s = "UCT"
            print("---------------- Depth = ", depth, "  Utility function = ", util, "---------------------")
            if depth == "max":
                GetData_UCT_max_depth()
            elif depth == "lim":
                GetData_UCT_lim_depth()
            else:
                print("Incorrect value depth: should be 'max' or 'lim'.")



