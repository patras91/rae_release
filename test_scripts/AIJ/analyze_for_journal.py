__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse
import math
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.2  # previous pdf hatch linewidth
#mpl.rcParams['hatch.linewidth'] = 1.0  # previous svg hatch linewidth
import numpy as np 
from pylab import rcParams

from param_values import *

# used to keep track of problems that succeeded using purely reactive RAE
succCases = { 'SD': set({}), 'EE': set({}), 'CR': set({}), 'SR': set({}), 'OF': set({}), 'SDN': set({})}

def NotTimeLine(s):
    if len(s) < 7:
        return True
    elif s[2:7] == "loops" or s[2:6] == "loop":
        return False
    else:
        return True

def GetMSEError(l, mean, fac):
    variance = 0
    if fac > 0:
        fac = 1.96
    for i in l:
        variance += (i - mean) * (i - mean)

    print("mean = ", mean, "variance = ", variance)
    return fac * math.sqrt(variance/(len(l)-1)/len(l))
    #return fac*variance/(len(l) - 1)/len(l)

def Include(pname, domain, num_tasks_per_problem):
    #print(pname, problems_with_n_tasks[domain][num_tasks_per_problem])
    v = num_tasks_per_problem == 0 or pname in problems_with_n_tasks[domain][num_tasks_per_problem]
    return v

def PopulateHelper(res, domain, f, param, fileName, num_tasks_per_problem=0): # param may be n_ro or k or d
    print(fileName)
    line = f.readline()

    nSucc, nTasks, nRetry, totalCountForRetries, nTimeOut, nLine = 0, 0, 0, 0, 0, 0
    plTime, acTime, ttTime, nu = 0, 0, 0, 0 # sums

    nu_L, sr_L, rr_L, tt_L = [], [], [], [] # lists of efficiency, success Ratio, retry ratio, total time 

    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':
            pName = parts[4][0:-1] if parts[4][-1] == '\n' else parts[4]

            fLine = f.readline()
            if fLine[0] == "T":
                print("passing ---------------")
                print(fileName, " line number = ", nLine)
                fLine = f.readline()
                nLine += 1
            nLine += 1

            while(NotTimeLine(fLine)):
                if fLine == '': break

                parts2 = fLine.split(' ')
                version = 2 if parts2[0] == "v2" else 1

                if Include(pName, domain, num_tasks_per_problem):
                    if fLine == "0 1 0 0 0 0 0 0 0\n":
                        nTimeOut += 1
                        plTime += ptMax

                    if parts2[0] != "v2":
                        s, t, r = int(parts2[0]), int(parts2[1]), int(parts2[2])
                        plTime += float(parts2[3])
                        acTime += float(parts2[4])
                        tt_L.append(float(parts2[4]) + float(parts2[3]))
                        taskEff = float(parts2[5])
                    else:
                        s, t, r = int(parts2[1]), int(parts2[2]), int(parts2[3])
                        plTime += float(parts2[4])
                        acTime += float(parts2[5])
                        tt_L.append(float(parts2[4]) + float(parts2[5]))
                        taskEff = float(parts2[6])

                    if taskEff == float("inf"):
                        print("Infinite efficiency! Normalizing.\n")
                        taskEff = 1/5
                    
                    nu += taskEff
                    nu_L.append(taskEff)
                    nSucc += s
                    sr_L.append(s)
                    nTasks += t
                    
                    if s == t: # for retry ratio
                        if ((pName in succCases[domain]) and param > 0): 
                            nRetry += r
                            rr_L.append(r)
                            totalCountForRetries += t
                        elif param == 0:
                            succCases[domain].add(pName)
                            nRetry += r
                            rr_L.append(r)
                            totalCountForRetries += t
                        else: pass
                    else: pass

                if version == 2:
                    f.readline() # list of commands and planning efficiencies
                    nLine += 1

                fLine = f.readline()
                nLine += 1
            
            if Include(pName, domain, num_tasks_per_problem):
                timeParts = fLine.split()
                t = float(timeParts[5])/1000 if timeParts[6] == "msec" else float(timeParts[5])
                ttTime += t
                tt_L.append(t)

        line = f.readline()
        nLine += 1

    res['successRatio'].append(nSucc/nTasks)
    res['sr_error'].append(GetMSEError(sr_L, nSucc/nTasks, 1))
    if totalCountForRetries != 0:
        res['retryRatio'].append(nRetry/totalCountForRetries)
        res['rr_error'].append(GetMSEError(rr_L, nRetry/totalCountForRetries, 10))
    else:
        res['retryRatio'].append(0)
        res['rr_error'].append(0)

    res['planTime'].append(plTime/nTasks)
    res['actTime'].append(acTime/nTasks)
    res['totalTime'].append(ttTime/nTasks)
    res['tt_error'].append(GetMSEError(tt_L, ttTime/nTasks, 0.000000))

    res['nu'].append(nu / nTasks)
    res['nu_error'].append(GetMSEError(nu_L, nu/nTasks, 1))

    res['timeOut'].append(nTimeOut)

def GetStandardDev(l):
    m = sum(l)/len(l)
    r = 0
    for i in l:
        r += (i-m)*(i-m)
    return math.sqrt(r/(len(l)-1))

def NormalizeValues(r):
    for v in ['nu', 'successRatio', 'retryRatio']: # 'nu_error', 'sr_error', 'rr_error']:
        print("before", r[v])
        val = r[v][0]
        if val != 0:
            r[v] = [item/val for item in r[v]]
            key_error = {
                'nu': 'nu_error',
                'successRatio': 'sr_error',
                'retryRatio': 'rr_error',
            }[v]
            r[key_error] = [item/val for item in r[key_error]]

        print("after", r[v])

def CommonStuffErrorRatio(res, domain, f_rae, param, fileName): # param may be k or d

    line = f_rae.readline()
    
    id = 0
    lineNumber = 0
    total = {}
    sumEff = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            id += 1

            counts = f_rae.readline()
            if counts[0] == "T":
                print("passing ---------------")
                print(fileName, " line number = ", lineNumber)
                counts = f_rae.readline()
                lineNumber += 1
            lineNumber += 1
            #print(fileName, " line number = ", lineNumber)
            while(NotTimeLine(counts)):
                if counts == '':
                    break
                if counts == "0 1 0 0 0 0 0 0 0\n":
                    pass

                parts2 = counts.split(' ')
                #print(parts2)
                if parts2[0] != "v2":
                    version = 1
                    taskEff = float(parts2[5])
                else:
                    version = 2
                    taskEff = float(parts2[6])

                if taskEff == float("inf"):
                    print("Infinite efficiency! Normalizing.\n")
                    taskEff = 1/10

                if version == 2:
                    planningUtils = f_rae.readline() # list of commands and planning efficiencies
                    lineNumber += 1
                    # update the planning utility error ratios
                    #if taskEff > 0:
                    if True:
                        subs = planningUtils.split(' ')
                        commCount = 0
                        itr = 0
                        for item in subs:
                            chars = [str(i) for i in range(0,10)]
                            if item[0] in chars or item == "inf":

                                if item == "inf":
                                    item = 0.1
                                errorRatio = abs(taskEff - float(item))

                                if itr == 2:
                                    if commCount in res:
                                        res[commCount].append(errorRatio)
                                        #print(errorRatio)
                                        total[commCount] += 1
                                        sumEff += taskEff
                                    else:
                                        res[commCount] = [errorRatio]
                                        total[commCount] = 1
                                    commCount += 1
                                    if commCount > 10:
                                        break
                                itr = (itr + 1)%3

                counts = f_rae.readline()
                lineNumber += 1
            
        line = f_rae.readline()
        lineNumber += 1

    for commCount in res:
        #res[commCount] = GetStandardDev(res[commCount])
        res[commCount] = sum(res[commCount])/total[commCount]

    print(res)

def PopulateHelper_UCT_max_depth_error_ratio(res, domain, f_rae, uct, fileName):
    CommonStuffErrorRatio(res, domain, f_rae, uct, fileName)

def Populate_SLATE_max_depth(res, domain):
    for b in B_max_depth[domain]:
        for k in K_max_depth[domain]:
            if k == 0:
                f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper(res[b], domain, f_rae, k, f_rae_name)
                f_rae.close()
            else:
                fname = '{}{}_v_journal{}/rae_plan_b_{}_k_{}.txt'.format(resultsFolder, domain, util, b, k)
                fptr = open(fname)
                print(fname)
                PopulateHelper(res[b], domain, open(fname), k, fname)
                fptr.close()

def Populate_UCT_max_depth(res, domain, utilF, num_tasks_per_problem):
    for n_ro in UCT_max_depth[domain]:
        if n_ro == 0:
            fname = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
        else:
            fname = '{}{}_v_journal{}/UPOM_{}.txt'.format(resultsFolder, domain, utilF, n_ro)
        fptr = open(fname, "r")
        print(fname)
        PopulateHelper(res, domain, open(fname), n_ro, fname, num_tasks_per_problem)
        fptr.close()
    NormalizeValues(res)

def Populate_learning(res, domain, model, num_tasks_per_problem):
    if model == "UCT":
        #if domain == "CR":
        #    f1 = "{}{}_v_journal/rae_plan_uct_5000.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal_eff/rae_plan_uct_250.txt".format(resultsFolder, domain)
        print("reading from ", f1)
        #if domain == "CR" or domain == "EE":
            #f1 = "{}{}_v_journal/RAE_with_planning.txt".format(resultsFolder, domain)
        #else:
        #    f1 = "{}{}_v_journal_eff/rae_plan_uct_100.txt".format(resultsFolder, domain)
    elif model == "heuristic_10_3":
        #if domain == "EE":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_40_6.txt".format(resultsFolder, domain)
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_with_learnH_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE_with_learnH.txt".format(resultsFolder, domain)
        #else:
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_10_3.txt".format(resultsFolder, domain)
    
    elif model == "SLATE":
        f1 = "{}{}_v_journal/rae_plan_b_2_k_2.txt".format(resultsFolder, domain)
    
    elif model == "reactive" or domain == "OF":
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    

    elif model == "actor":
        #if domain not in  ["SR"]:
        #    f1 = "{}{}_v_journal/RAE_with_trained_model_actor.txt".format(resultsFolder, domain)
        #else:
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_with_learnM_a_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE_with_learnM_a.txt".format(resultsFolder, domain)
            
    elif model == "planner":
        #if domain not in  ["SR"]:
        #    f1 = "{}{}_v_journal/RAE_with_trained_model_planner.txt".format(resultsFolder, domain)
        #else:
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_with_learnM_p_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE_with_learnM_p.txt".format(resultsFolder, domain)
        #elif model == "heuristic0_10_3" or domain == "SR" or domain == "EE":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_0_10_3.txt".format(resultsFolder, domain)
        #elif model == "heuristic":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic.txt".format(resultsFolder, domain)
        #elif model == "heuristic5":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_5.txt".format(resultsFolder, domain)
        #elif model == "heuristic0":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_0.txt".format(resultsFolder, domain)
    f1_p = open(f1, "r")
    PopulateHelper(res, domain, f1_p, 0, f1, num_tasks_per_problem)

    f1_p.close()

def Populate_learning_mi(res, domain, model, nTasks):
    if model == "UCT":
        f1 = "{}{}_v_journal_eff/rae_plan_uct_250.txt".format(resultsFolder, domain)
    elif model == "learnMI":
        f1 = "{}{}_v_journal/RAE_with_learnMI_p.txt".format(resultsFolder, domain)    
    elif model == "learnH":
        #if domain == "EE":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_40_6.txt".format(resultsFolder, domain)
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_with_learnH_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE_with_learnH.txt".format(resultsFolder, domain)
    elif model == "SLATE":
        f1 = "{}{}_v_journal/rae_plan_b_2_k_2.txt".format(resultsFolder, domain)  
    elif model == "reactive" or domain == "OF":
        f1 = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    elif model == "actor":
        f1 = "{}{}_v_journal/RAE_with_learnM_a.txt".format(resultsFolder, domain)
      
    elif model == "planner":
        f1 = "{}{}_v_journal/RAE_with_learnM_p.txt".format(resultsFolder, domain)

    f1_p = open(f1, "r")
    if domain != 'OF':
        nTasks = 0
    PopulateHelper(res, domain, f1_p, 0, f1, nTasks)
    f1_p.close()

def Populate_UCT_max_depth_error_ratio(res, domain):
    for uct in UCT_max_depth[domain]:
        if uct == 0:
            f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelper_UCT_max_depth_error_ratio(res[uct], domain, f_rae, uct, f_rae_name)
            f_rae.close()
        else:
            fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, util, uct)
            fptr = open(fname)
            print(fname)
            PopulateHelper_UCT_max_depth_error_ratio(res[uct], domain, open(fname), uct, fname)
            fptr.close()

def Populate_SLATE_lim_depth(res, domain):  
    k = K_lim_depth[domain]
    for b in B_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth == 0:
                f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper(res[b], domain, f_rae, depth, f_rae_name)
                f_rae.close()
            else:
                fname = '{}{}_v_journal{}/rae_plan_b_{}_k_{}_d_{}.txt'.format(resultsFolder, domain, util, b, k, depth)
                fptr = open(fname)
                print(fname)
                PopulateHelper(res[b], domain, open(fname), depth, fname)
                fptr.close()

def Populate_UCT_lim_depth(res, domain, heuristic, num_tasks_per_problem):  
    for depth in Depth[domain]:
        n_ro = Get_nro_in_lim_depth(heuristic, depth)
        if depth == 0:
            f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelper(res, domain, f_rae, depth, f_rae_name, num_tasks_per_problem)

            f_rae.close()
        else:
            if heuristic == "h0":
                h = "_h_h0"
            elif heuristic == "h1":
                h = ""
            elif heuristic == "learnH":
                h = "_h_learnH"

            fname = '{}{}_v_journal_eff/rae_plan_uct_{}_d_{}'.format(resultsFolder, domain, n_ro, depth) \
                    + h + '.txt'.format()
            
            fptr = open(fname)
            print(fname)
            PopulateHelper(res, domain, open(fname), depth, fname, num_tasks_per_problem)
            fptr.close()

    NormalizeValues(res)

def GeneratePlots_SLATE_max_depth():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {},
        'SR': {},
        'OF': {},
    }

    for domain in resDict:
        resDict[domain] = {}
        for b in B_max_depth[domain]:
            resDict[domain][b] = GetNewDict()
    for d in D:
        Populate_SLATE_max_depth(resDict[d], d)
        #CalculateRunningTime(d)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    print(resDict)
    for util in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_SLATE_max(resDict, util)

def GeneratePlots_UCT_max_depth(num_tasks_per_problem):
    resDict = {}
    for domain in D:
        if util == "_sr":
            resDict[domain] = {}
            resDict[domain]['_sr'] = GetNewDict()
            resDict[domain]['_eff'] = GetNewDict()
            Populate_UCT_max_depth(resDict[domain]['_sr'], domain, '_sr', num_tasks_per_problem)
            Populate_UCT_max_depth(resDict[domain]['_eff'], domain, '_eff', num_tasks_per_problem)
        else:
            resDict[domain] = GetNewDict()
            Populate_UCT_max_depth(resDict[domain], domain, '_eff', num_tasks_per_problem)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'regular',
        'size'   : 12}
    plt.rc('font', **font)
    
    print(resDict)
    for metric in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_UCT_max(resDict, metric)

def GeneratePlots_LearnMI(num_tasks):
    resDict = {}
    for domain in D:
        resDict[domain] = {}
        resDict[domain]['reactive'] = GetNewDict()
        resDict[domain]['SLATE'] = GetNewDict()
        resDict[domain]['learning_from_actor'] = GetNewDict()
        resDict[domain]['learning_from_planner'] = GetNewDict()
        resDict[domain]['learnMI'] = GetNewDict()
        resDict[domain]['learnH'] = GetNewDict()
        resDict[domain]['UCT'] = GetNewDict()

        Populate_learning_mi(resDict[domain]['UCT'], domain, 'UCT', num_tasks)
        Populate_learning_mi(resDict[domain]['SLATE'], domain, 'SLATE', num_tasks)
        
        Populate_learning_mi(resDict[domain]['reactive'], domain, 'reactive', num_tasks)
        Populate_learning_mi(resDict[domain]['learning_from_actor'], domain, 'actor', num_tasks)
        Populate_learning_mi(resDict[domain]['learning_from_planner'], domain, 'planner', num_tasks)
        Populate_learning_mi(resDict[domain]['learnMI'], domain, 'learnMI', num_tasks)
        Populate_learning_mi(resDict[domain]['learnH'], domain, 'learnH', num_tasks)
    
    print(resDict)
    
    for metric in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_LearnMI(resDict, metric, errIndex[metric])

def GeneratePlots_learning(num_tasks_per_problem):
    resDict = {}
    for domain in D:
        if domain == "CR":
            n_UCT = 1
        else:
            n_UCT = 0
        resDict[domain] = {}
        resDict[domain]['reactive'] = GetNewDict()
        resDict[domain]['SLATE'] = GetNewDict()
        resDict[domain]['learning_from_actor'] = GetNewDict()
        resDict[domain]['learning_from_planner'] = GetNewDict()
        resDict[domain]['heuristic_10_3'] = GetNewDict()
        resDict[domain]['UCT'] = GetNewDict()


        Populate_learning(resDict[domain]['UCT'], domain, 'UCT', num_tasks_per_problem)
        Populate_learning(resDict[domain]['SLATE'], domain, 'SLATE', num_tasks_per_problem)
        Populate_learning(resDict[domain]['reactive'], domain, 'reactive', num_tasks_per_problem)
        

        # resDict[domain]['heuristic'] = GetNewDict()    
        # resDict[domain]['heuristic5'] = GetNewDict()
        # resDict[domain]['heuristic0'] = GetNewDict()
        # resDict[domain]['heuristic0_10_3'] = GetNewDict()

        Populate_learning(resDict[domain]['learning_from_actor'], domain, 'actor', num_tasks_per_problem)
        Populate_learning(resDict[domain]['learning_from_planner'], domain, 'planner', num_tasks_per_problem)
        #Populate_learning(resDict[domain]['heuristic5'], domain, 'heuristic5')
        #Populate_learning(resDict[domain]['heuristic'], domain, 'heuristic')
        #Populate_learning(resDict[domain]['heuristic0'], domain, 'heuristic0')
        #Populate_learning(resDict[domain]['heuristic0_10_3'], domain, 'heuristic0_10_3')
        Populate_learning(resDict[domain]['heuristic_10_3'], domain, 'heuristic_10_3', num_tasks_per_problem)

    
    print(resDict)
    
    for metric in ['nu', 'successRatio', 'retryRatio'] : #, 'totalTime']:
        PlotHelper_learning(resDict, metric, errIndex[metric])

def GeneratePlots_UCT_max_depth_error_ratio():
    resDict = {}
    for domain in D:
        resDict[domain] = {}
        for uct in UCT_max_depth[domain]:
            resDict[domain][uct] = {}

    for domain in D:
        Populate_UCT_max_depth_error_ratio(resDict[domain], domain)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    
    print(resDict)
    PlotHelper_UCT_max_error_ratio(resDict)

def GeneratePlots_SLATE_lim_depth():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {},
        'SR': {},
    }

    for domain in resDict:
        resDict[domain] = {}
        for b in B_lim_depth[domain]:
            resDict[domain][b] = GetNewDict()

    for d in D:
        Populate_SLATE_lim_depth(resDict[d], d)
        #CalculateRunningTimeDepth(d)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})


    print(resDict)
    for util in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_SLATE_lim(resDict, util)

def GeneratePlots_UCT_lim_depth(num_tasks_per_problem):
    global util
    resDict = {}
    assert(util == "_eff")
    for domain in D:
        resDict[domain] = {'h0': {}, 'h1': {}, 'learnH': {}}
        for h in resDict[domain]:
            resDict[domain][h] = GetNewDict()
            Populate_UCT_lim_depth(resDict[domain][h], domain, h, num_tasks_per_problem)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'regular',
        'size'   : 16}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    print(resDict)
    for metric in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_UCT_lim(resDict, metric)

def GetString(depth):
    s = []
    for item in depth:
        s.append(str(item))

    return s

def CheckIn(l, e):
    for key in l:
        if e <= key*(1.01) and e >= key*0.99:
            return (True, key)
    return (False, None)

def normalize(l):
    #m = max(l)
    lret = []
    for i in range(1, len(l)):
        if (l[0] - l[i])*100/l[0]/4 > 0:
            lret.append((l[0] - l[i])*100/l[0])
        else:
            lret.append(0)
    return lret

def GetSum(*l):
    size = len(l[0])
    res = []
    for i in range(0, size):
        res.append(0)
        for item in l:
            res[i] += item[i]
    return res

def GetYlabel(util):
    if util == 'nu':
        return 'Efficiency'
    elif util == 'successRatio':
        return 'Success Ratio'
    elif util == "retryRatio":
        return 'Retry Ratio'
    elif util == "totalTime":
        return 'Total time'
    else:
        return "Y"

def Accumulate(res1, res2):
    if res1 == []:
        for item in res2[0:7]:
            res1.append(item/5)
        #res1 = [item for item in res2[0:6]]

    else:
        for i in range(7):
            res1[i] += res2[i]/5

def PlotHelper_UCT_max_Acc(resDict, index1):

    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    res = {'_sr': GetNewDict(), '_eff': GetNewDict()}

    assert(util == "_sr")

    for domain in D:
        Accumulate(res['_sr'][index1], resDict[domain]['_sr'][index1])
        Accumulate(res['_sr'][errIndex[index1]], resDict[domain]['_sr'][errIndex[index1]])
        Accumulate(res['_eff'][index1], resDict[domain]['_eff'][index1])
        Accumulate(res['_eff'][errIndex[index1]], resDict[domain]['_eff'][errIndex[index1]])
        
    plt.clf()
    fname = '{}{}_UCT_max_depth.png'.format(figuresFolder, index1)
    
    fig, ax = plt.subplots()
    PlotViaMatlabBar([0, 5, 10, 25, 50, 100, 250], 
        res['_sr'][index1],
        res['_sr'][errIndex[index1]],
        COLORBAR[0],
        "utility = success ratio", -1, ax)
    PlotViaMatlabBar([0, 5, 10, 25, 50, 100, 250], 
        res['_eff'][index1],
        res['_eff'][errIndex[index1]],
        COLORBAR[1],
        "utility = efficiency", 1, ax)

    plt.legend(bbox_to_anchor=(0.05, 1.01), loc=3, ncol=2, borderaxespad=0.)
        
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels([str(item) for item in [0, 5, 10, 25, 50, 100, 250]])
    ax.set_ylim(bottom=0.2)
    plt.xlabel('Number of rollouts')
    plt.ylabel(GetYlabel(index1))

    plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_max(resDict, utilp):
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 20}
    plt.rc('font', **font)
    #PlotHelper_UCT_max_Acc(resDict, utilp)
    #return

    index1 = utilp
    width = 0.8
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        #fname = '{}{}_{}_UCT_max_depth_one_task.png'.format(figuresFolder, domain, utilp)
        fname = '{}{}_{}_UCT_max_depth.png'.format(figuresFolder, domain, utilp)
        
        if util == "_sr":
            fig, ax = plt.subplots()
            if utilp == "successRatio":
                PlotViaMatlabBar(UCT_max_depth[domain], 
                    resDict[domain]['_sr'][index1],
                    resDict[domain]['_sr'][errIndex[index1]],
                    COLORBAR[0],
                    "utility = success ratio", 0, ax, width)
            else:
                PlotViaMatlabBar(UCT_max_depth[domain], 
                    resDict[domain]['_eff'][index1],
                    resDict[domain]['_eff'][errIndex[index1]],
                    COLORBAR[1],
                    "utility = efficiency", 0, ax, width)
        else:
            fig, ax = plt.subplots()
            PlotViaMatlabBar(UCT_max_depth[domain], 
                resDict[domain][index1],
                resDict[domain][errIndex[index1]],
                COLORBAR[0],
                GetYlabel(utilp), 0, ax, width)
        
        #plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        ax.set_xticks(np.arange(len(UCT_max_depth[domain])))
        ax.set_xticklabels([str(item) if item != 1000 else "1K" for item in UCT_max_depth[domain]])
        plt.xlabel('Number of rollouts')
        ax.set_title(GetFullName(domain))
        ax.set_ylim(bottom=GetLowerLim(domain))
        #plt.xticks(UCT_max_depth[domain],
        #   [str(item) for item in UCT_max_depth[domain]])
        plt.ylabel(GetYlabel(utilp))

        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_LearnMI(resDict, utilp, errorP):
    index1 = utilp

    fname = '{}{}_learning_mi.png'.format(figuresFolder, utilp)

    rcParams['figure.figsize'] = 6, 3
    plt.clf()
    ax = {}
    ax['SD'] = plt.subplot2grid((1,2), (0,0), colspan=1)
    ax['OF'] = plt.subplot2grid((1,2), (0,1), colspan=1)

    toPlot = {}
    
    for domain in D:
        normalizer = resDict[domain]['reactive'][index1][0]
        toPlot = {'val': {}, 'err': {}}
        toPlot['val']['RAE\n(no planning)'] = resDict[domain]['reactive'][index1][0]/normalizer
        toPlot['val']['LearnM-1'] = resDict[domain]['learning_from_actor'][index1][0]/normalizer
        toPlot['val']['LearnM-2'] = resDict[domain]['learning_from_planner'][index1][0]/normalizer
        toPlot['val']['LearnMI'] = resDict[domain]['learnMI'][index1][0]/normalizer
        toPlot['val']['LearnH'] = resDict[domain]['learnH'][index1][0]/normalizer
        #toPlot['val']['RAEplan'] = resDict[domain]['SLATE'][index1][0]/normalizer
        toPlot['val']['UPOM'] = resDict[domain]['UCT'][index1][0]/normalizer

        # the errors
        toPlot['err']['RAE (no planning)'] = resDict[domain]['reactive'][errorP][0]/normalizer
        toPlot['err']['LearnM-1'] = resDict[domain]['learning_from_actor'][errorP][0]/normalizer
        toPlot['err']['LearnM-2'] = resDict[domain]['learning_from_planner'][errorP][0]/normalizer
        toPlot['err']['LearnMI'] = resDict[domain]['learnMI'][errorP][0]/normalizer
        toPlot['err']['LearnH'] = resDict[domain]['learnH'][errorP][0]/normalizer
        #toPlot['err']['RAEplan'] = resDict[domain]['SLATE'][errorP][0]/normalizer
        toPlot['err']['UPOM'] = resDict[domain]['UCT'][errorP][0]/normalizer

        width = 0.85  # 0.003 the width of the bars
    
        labels = list(toPlot['val'].keys())
        x = np.arange(len(labels))

        print(domain)
        print(list(toPlot['val'].values()))

        rects = ax[domain].bar(x, list(toPlot['val'].values()), width, 
            color=['turquoise', 'grey', 'orange', 'yellowgreen', 'blue',  'orchid'],
            yerr=list(toPlot['err'].values()), capsize=3)
       
        patterns = ('\\', '\\\\', '/', '+', 'x', '\\\\\\\\')
        for bar, pattern in zip(rects, patterns):
            bar.set_hatch(pattern)

        text = {
            0: 'Purely reactive',
            1: 'LearnM-1',
            2: 'LearnM-2',
            3: 'LearnMI',
            4: 'LearnH',
            5: 'RAE + UPOM',
        }
        for i, v in enumerate(x):
            pass
            #ax[domain].text(i, list(toPlot['val'].values())[i] + 0.001, text[i], rotation=90)
        #ax[domain].set_ylim(bottom=lowerLim[domain][index1])
        ax[domain].set_ylim(bottom=0.9)
        #elif index1 == "successRatio":
        #    ax.set_ylim(bottom=0.1)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax[domain].set_ylabel(GetYlabel(utilp))
        ax[domain].yaxis.grid(True)
        ax[domain].set_xlabel(domain)
        ax[domain].get_xaxis().set_visible(False)
        ax[domain].set_title(GetFullName(domain))
        #ax[domain].set_xticks(x)
        #ax[domain].set_xticklabels(labels, rotation=45)
        ax[domain].legend()

    plt.tight_layout()
    #plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=1, ncol=0, borderaxespad=0.)
     
    plt.savefig(fname, bbox_inches='tight')
    print("saved")

def PlotHelper_learning(resDict, utilp, errorP):
    index1 = utilp
    #index1 = 'actTime'
    #K = [0, 1, 2, 3, 4, 8, 16]
    rcParams['figure.figsize'] = 9, 6
    fname = '{}{}_learning.png'.format(figuresFolder, utilp)

    plt.clf()
    #font = {
    #    'family' : 'times',
    #    'weight' : 'regular',
    #    'size'   : 8}
    #plt.rc('font', **font)
    
    ax = {}
    ax['SR'] = plt.subplot2grid(shape=(2,3), loc=(0,0), colspan=1)
    ax['SD'] = plt.subplot2grid((2,3), (0,1), colspan=1)
    ax['EE'] = plt.subplot2grid((2,3), (0,2), colspan=1)
    ax['CR'] = plt.subplot2grid((2,3), (1,0), colspan=1)
    ax['OF'] = plt.subplot2grid((2,3), (1,1), colspan=1)

    toPlot = {}

    for domain in D:
        normalizer = resDict[domain]['reactive'][index1][0]
        toPlot = {'val': {}, 'err': {}}
        toPlot['val']['RAE\n(no planning)'] = resDict[domain]['reactive'][index1][0]/normalizer
        toPlot['val']['LearnM-1'] = resDict[domain]['learning_from_actor'][index1][0]/normalizer
        toPlot['val']['LearnM-2'] = resDict[domain]['learning_from_planner'][index1][0]/normalizer
        toPlot['val']['LearnH'] = resDict[domain]['heuristic_10_3'][index1][0]/normalizer
        toPlot['val']['RAEplan'] = resDict[domain]['SLATE'][index1][0]/normalizer
        toPlot['val']['UPOM'] = resDict[domain]['UCT'][index1][0]/normalizer

        # the errors
        toPlot['err']['RAE (no planning)'] = resDict[domain]['reactive'][errorP][0]/normalizer
        toPlot['err']['LearnM-1'] = resDict[domain]['learning_from_actor'][errorP][0]/normalizer
        toPlot['err']['LearnM-2'] = resDict[domain]['learning_from_planner'][errorP][0]/normalizer
        toPlot['err']['LearnH'] = resDict[domain]['heuristic_10_3'][errorP][0]/normalizer
        toPlot['err']['RAEplan'] = resDict[domain]['SLATE'][errorP][0]/normalizer
        toPlot['err']['UPOM'] = resDict[domain]['UCT'][errorP][0]/normalizer

        width = 0.85  # 0.003 the width of the bars
    

        labels = list(toPlot['val'].keys())
        x = np.arange(len(labels))

        print(domain)
        print(ptMax)
        print(list(toPlot['val'].values()))

        rects = ax[domain].bar(x, list(toPlot['val'].values()), width, 
            color=['turquoise', 'grey', 'orange', 'yellowgreen', 'orangered', 'orchid'],
            yerr=list(toPlot['err'].values()), capsize=3)
       
        patterns = ('\\', '\\\\', '/', '+', 'x', '\\\\\\\\')
        for bar, pattern in zip(rects, patterns):
            bar.set_hatch(pattern)

        #ax[domain].set_ylim(bottom=lowerLim[domain][index1])
        ax[domain].set_ylim(bottom=0.8)
        #elif index1 == "successRatio":
        #    ax.set_ylim(bottom=0.1)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax[domain].set_ylabel(GetYlabel(utilp))
        ax[domain].yaxis.grid(True)
        ax[domain].set_xlabel(domain)
        ax[domain].get_xaxis().set_visible(False)
        ax[domain].set_title(GetFullName(domain))
        #ax[domain].set_xticks(x)
        #ax[domain].set_xticklabels(labels, rotation=45)
        #ax[domain].legend()
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=1, borderaxespad=0.)
            

    plt.savefig(fname, bbox_inches='tight')
    print("saved")

def PlotHelper_UCT_lim(resDict, utilp):
    index1 = utilp
    width=0.25
    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_lim_depth.png'.format(figuresFolder, domain, utilp)
        
        i = 2
        fig, ax = plt.subplots()
        PlotViaMatlabBar(Depth[domain],
            resDict[domain]['h0'][index1],
            resDict[domain]['h0'][errIndex[index1]],
            COLORBAR[i],
            'heuristic = h0', -2, ax, width)
        i += 1
        PlotViaMatlabBar(Depth[domain],
            resDict[domain]['h1'][index1],
            resDict[domain]['h1'][errIndex[index1]],
            COLORBAR[i],
            'heuristic = hD', 0, ax, width)
        i += 1
        PlotViaMatlabBar(Depth[domain],
            resDict[domain]['learnH'][index1],
            resDict[domain]['learnH'][errIndex[index1]],
            COLORBAR[i],
            'heuristic = hLearnH', +2, ax, width)
        i += 1
    
        #plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=1, borderaxespad=0.)
            
        plt.xlabel('Depth')
        ax.set_xticks(np.arange(len(Depth[domain])))
        ax.set_xticklabels([str(item) for item in Depth[domain]])
        ax.set_title(GetFullName(domain))
        ax.set_ylim(bottom=0.8)
        plt.ylabel(GetYlabel(utilp)) 
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_SLATE_max(resDict, utilp):
    index1 = utilp
    width = 0.25

    for domain in D:
        i = 0
        plt.clf()
        for b in B_max_depth[domain]:
            PlotViaMatlab(K_max_depth[domain], 
                resDict[domain][b][index1],
                COLORS[i],
                'b={}'.format(b)
            )
            i += 1
        
        fname = '{}{}_{}_SLATE_max_depth{}.png'.format(figuresFolder, domain, index1, util)
        plt.xlabel('k')
        plt.xticks(K_max_depth[domain],
           GetString(K_max_depth[domain]))
        plt.ylabel(GetYlabel(utilp))
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_SLATE_lim(resDict, utilp):
    index1 = utilp
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_SLATE_lim_depth{}.png'.format(figuresFolder, domain, utilp, util)
        i = 0
        for b in B_lim_depth[domain]:
            PlotViaMatlab(Depth[domain],
                resDict[domain][b][index1],
                COLORS[i],
                'b={}'.format(b)
            )
            i += 1
     
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
            
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel(GetYlabel(utilp)) 
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_max_error_ratio(resDict):
    width = 0.25

    for domain in ['EE']:
        plt.clf()
        fname = '{}{}_UCT_max_depth_error_ratio.png'.format(figuresFolder, util)
        
        i = 0
        val = None
        for uct in [5, 10, 25, 50, 100, 250]:# UCT_max_depth[domain][1:]:
            sortedDict = {}
            for k in sorted(resDict[domain][uct]):
                sortedDict[k] = resDict[domain][uct][k]
                count = 1
                for x in ['CR', 'SR', 'SD', 'OF']:
                    if k in resDict[x][uct]:
                        sortedDict[k] += resDict[x][uct][k]
                        count += 1
                sortedDict[k] /= count
            print(sortedDict)
            if val == None:
                val = sortedDict[0]
            for k in sortedDict:
                sortedDict[k] = sortedDict[k]/val
            PlotViaMatlabLine(sortedDict.keys(),
                sortedDict.values(),
                COLORS[i],
                'rollouts={}'.format(uct))
            i += 1
        
        plt.legend(bbox_to_anchor=(1.02, 0.02), loc=3, ncol=1, borderaxespad=0.)
            
        plt.xlabel('Refinement Deepness')
        plt.xticks(list(sortedDict.keys()),
           GetString(list(sortedDict.keys())))
        plt.ylabel("Difference in \n Expected Efficiency") 
        plt.savefig(fname, bbox_inches='tight')

def PlotViaMatlabLine(x, y, c, l):
    line1, = plt.plot(x, y, c, 
        label=l, 
        linewidth=4, 
        MarkerSize=10, 
        markerfacecolor='white')
        
def PlotViaMatlabBar(x, y, y_error, c, l, f, ax, width=0.4):
    print(x)
    print(y)
    print(y_error)
    x = np.arange(len(x))
    rects = ax.bar(x + f*width/2, y, width,
            color=c, 
            #color=['black', 'turquoise', 'grey', 'orange', 'yellowgreen', 'orangered', 'orchid', 'green'],
            yerr=y_error, 
            label=l,
            capsize=3
            )
       
D = None
util = None
l = None

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SD', 'IP', 'SR', 'OF', 'EE']",
                           type=str, required=True)
    argparser.add_argument("--depth", help="depth = 'max' or 'lim'",
                           type=str, required=True)
    argparser.add_argument("--s", help="SamplingStrategy ",
                           type=str, required=False, default="UCT")
    argparser.add_argument("--er", help="plot error ratio", default='n',
                            type=str, required=False)
    argparser.add_argument("--utility", help="efficiency or successRatio?",
                            type=str, required=True)
    argparser.add_argument("--l", help="Compare with learning? ('y' or 'mi' or 'n')?",
                            type=str, default='n', required=True)
    args = argparser.parse_args()

    learning = args.l
    if args.utility == "efficiency":
        util = "_eff"
    else:
        util = "_sr"

    #D = ["SD", "SR", "EE", "CR", "OF"]
    #D = ["CR", "OF"]
    #D = ["SD", "OF"]
    D = ["SDN"]

    if args.l == "y":
        GeneratePlots_learning(0)
    elif args.l == "mi":
        GeneratePlots_LearnMI(0)
    elif args.depth == "max":
        if args.s == "SLATE":
            GeneratePlots_SLATE_max_depth()
        else:
            if args.er == "n":
                GeneratePlots_UCT_max_depth(0)
            else:
                GeneratePlots_UCT_max_depth_error_ratio()
    elif args.depth == "lim":
        if args.s == "SLATE":
            GeneratePlots_SLATE_lim_depth()
        else:
            if args.er == "n":
                GeneratePlots_UCT_lim_depth(0)
            else:
                GeneratePlots_UCT_lim_depth_error_ratio()
    else:
        print("Incorrect value depth: should be 'max' or 'lim'.")
