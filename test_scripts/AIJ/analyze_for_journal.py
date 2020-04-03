__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse
import math
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.2  # previous pdf hatch linewidth
#mpl.rcParams['hatch.linewidth'] = 1.0  # previous svg hatch linewidth

import numpy as np 

from param_values import *

succCases = {
    'SD': [],
    'EE': [],
    'IP': [],
    'CR': [],
    'SR': [],
    'OF': [],
}

# The set of problems with 1 tasks, 2 tasks, or 3 tasks in each domain
problems_with_n_tasks = {
    'SD': {1: ['problem1119', 'problem1059', 'problem1029', 'problem1103', 'problem1121', 'problem1063', 'problem1057', 'problem1069', 'problem1055', 'problem1083', 'problem1049', 'problem1039', 'problem1125', 'problem1087', 'problem1115', 'problem1033', 'problem1019', 'problem1089', 'problem1053', 'problem1085', 'problem1051', 'problem1107', 'problem1045', 'problem1007', 'problem1003', 'problem1013', 'problem1127', 'problem1027', 'problem1043'], 2: ['problem1014', 'problem1070', 'problem1068', 'problem1106', 'problem1028', 'problem1046', 'problem1100', 'problem1086', 'problem1116', 'problem1124', 'problem1084', 'problem1066', 'problem1010', 'problem1078', 'problem1120', 'problem1110', 'problem1032', 'problem1104', 'problem1036', 'problem1016', 'problem1094'], 3: []},
    'EE': {1: ['problem187', 'problem91', 'problem159', 'problem131', 'problem7', 'problem35', 'problem3', 'problem31', 'problem103', 'problem75', 'problem123', 'problem143', 'problem163', 'problem43', 'problem183'], 2: ['problem5', 'problem108', 'problem72', 'problem85', 'problem173', 'problem44', 'problem29', 'problem20', 'problem129', 'problem188', 'problem161', 'problem17', 'problem89', 'problem136', 'problem104', 'problem57', 'problem52', 'problem156', 'problem168', 'problem164', 'problem68', 'problem73'], 3: ['problem170', 'problem134', 'problem190', 'problem86', 'problem58', 'problem158', 'problem78', 'problem42', 'problem14', 'problem50', 'problem2', 'problem174', 'problem178']},
    'CR': {
        1: ['problem1004', 'problem1002', 'problem1096', 'problem1073', 'problem1012', 'problem1005', 'problem1087', 'problem1069', 'problem1089', 'problem1001', 'problem1008', 'problem1013', 'problem1092', 'problem1079', 'problem1085', 'problem1011', 'problem1076', 'problem1036', 'problem1099', 'problem1038', 'problem1028', 'problem1088', 'problem1007', 'problem1017', 'problem1040', 'problem1074', 'problem1078', 'problem1009', 'problem1045', 'problem1032', 'problem1046', 'problem1027', 'problem1041', 'problem1019'], 
        2: ['problem1106', 'problem1114', 'problem1053', 'problem1062', 'problem1111', 'problem1110', 'problem1120', 'problem1100', 'problem1118', 'problem1056', 'problem1108', 'problem1061', 'problem1065', 'problem1112', 'problem1067', 'problem1066'], 
        3: [],
        },
    'SR': {1: ['problem43', 'problem32', 'problem102', 'problem96', 'problem73', 'problem105', 'problem27', 'problem85', 'problem35', 'problem36', 'problem38', 'problem24', 'problem89', 'problem75', 'problem76', 'problem106', 'problem108', 'problem78', 'problem88', 'problem39', 'problem95', 'problem72', 'problem46', 'problem107', 'problem92', 'problem21', 'problem110', 'problem71', 'problem30', 'problem113', 'problem60', 'problem64', 'problem42', 'problem84', 'problem23', 'problem97', 'problem111', 'problem90', 'problem65', 'problem54', 'problem56', 'problem112', 'problem98', 'problem109', 'problem55', 'problem81', 'problem100', 'problem50', 'problem104', 'problem74'], 2: [], 3: []},
    'OF': {
        1: ['problem55', 'problem109', 'problem72', 'problem53', 'problem45', 'problem73', 'problem89', 'problem51', 'problem74', 'problem11', 'problem39', 'problem68', 'problem56', 'problem95', 'problem77', 'problem66', 'problem97', 'problem42', 'problem64', 'problem61', 'problem13'], 
        2: ['problem12', 'problem25', 'problem48', 'problem57', 'problem103', 'problem20', 'problem37', 'problem21', 'problem36', 'problem29', 'problem76', 'problem105', 'problem15', 'problem67', 'problem90', 'problem27', 'problem18', 'problem34', 'problem23', 'problem91', 'problem28', 'problem22', 'problem59', 'problem47', 'problem30', 'problem78', 'problem49', 'problem75', 'problem94'], 
        3: []
    },
}

COLORS = ['ro:', 'bs--', 'm^-.', 'go--', 'c^:', 'rs--', 'ms--', 'gs--']

COLORBAR = ['orange', 'grey', 'yellowgreen', 'turquoise',  'orangered', 'orchid']

def GetFreshDict():
    return {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }

def GetFullName(domain):
    if domain == "CR":
        return "Fetch Objects Domain"
    elif domain == "SD":
        return "Navigate Doorways Domain"
    elif domain == "SR":
        return "Search and Rescue Domain"
    elif domain == "OF":
        return "Order Delivery Domain"
    elif domain == "EE":
        return "Explore Environment Domain"

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
    return fac*math.sqrt(variance/(len(l)-1)/len(l))
    #return fac*variance/(len(l) - 1)/len(l)

def CommonStuff(res, domain, f_rae, param, fileName): # param may be k or d
    print(fileName)
    line = f_rae.readline()
    global ptMax
    succCount = 0
    totalTasks = 0
    
    retryCount = 0
    totalCountForRetries = 0

    planTime = 0
    actTime = 0
    time11 = 0

    clock = 0
    nu = 0

    nu_L = []
    sr_L = []
    rr_L = []
    tt_L = []

    timeOutCount = 0
    
    id = 0
    lineNumber = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            succ = 0
            total = 0

            id += 1

            counts = f_rae.readline()
            if counts[0] == "T":
                print("passing---------------")
                print(fileName, " line number = ", lineNumber)
                counts = f_rae.readline()
                lineNumber += 1
            lineNumber += 1

            while(NotTimeLine(counts)):
                if counts == '':
                    break
                if counts == "0 1 0 0 0 0 0 0 0\n":
                    timeOutCount += 1
                    planTime += ptMax
                    if domain == "OF":
                        ignoreThis = True
                    else:
                        ignoreThis = False
                else:
                    ignoreThis = False

                parts2 = counts.split(' ')

                if parts2[0] != "v2":
                    version = 1
                    s = int(parts2[0])
                    t = int(parts2[1])
                    r = int(parts2[2])
                    if ignoreThis == False:
                        planTime += float(parts2[3])
                        #if ptMax < float(parts2[3]):
                        #    ptMax = float(parts2[3])
                        actTime += float(parts2[4])
                        tt_L.append(float(parts2[4]) + float(parts2[3]))
                    taskEff = float(parts2[5])
                else:
                    version = 2
                    s = int(parts2[1])
                    t = int(parts2[2])
                    r = int(parts2[3])
                    if ignoreThis == False:
                        planTime += float(parts2[4])
                        #if ptMax < float(parts2[4]):
                        #    ptMax = float(parts2[4])
                        actTime += float(parts2[5])
                        tt_L.append(float(parts2[4]) + float(parts2[5]))
                    taskEff = float(parts2[6])

                if taskEff == float("inf"):
                    print("Infinite efficiency! Normalizing.\n")
                    taskEff = 1/10
                if ignoreThis == False:
                    nu += taskEff
                    nu_L.append(taskEff)
                    succCount += s
                    sr_L.append(s)
                    totalTasks += t

                # for retry ratio
                if s == t:
                    if ((id in succCases[domain]) and param > 0): #or (domain in ['CR', 'EE', 'SD', 'IP']):
                        if ignoreThis == False:
                            retryCount += r
                            rr_L.append(r)
                            totalCountForRetries += t
                    elif param == 0 and ignoreThis == False:
                        succCases[domain].append(id)
                        retryCount += r
                        rr_L.append(r)
                        totalCountForRetries += t
                    else:
                        pass
                else:
                    pass

                if version == 2:
                    f_rae.readline() # list of commands and planning efficiencies
                    lineNumber += 1

                counts = f_rae.readline()
                lineNumber += 1
            
            secTimeLine = counts
            parts11 = secTimeLine.split()
            if ignoreThis == False:
                t11 = float(parts11[5])
                unit11 = parts11[6]
                if unit11 == "msec":
                    t11 = t11 / 1000
                time11 += t11
                tt_L.append(t11)

        line = f_rae.readline()
        lineNumber += 1

    scalar = {
        "CR": {
            "nu": 1,
            "sr": 1,
        },
        "SR": {
            "nu": 1,
            "sr": 1,
        },
        "SD": {
            "nu": 1,
            "sr": 1,
        },
        "EE": {
            "nu": 1,
            "sr": 1,
        },
        "OF": {
            "nu": 1,
            "sr": 1,
        }
    }

    res['successRatio'].append(succCount/totalTasks)
    res['sr_error'].append(GetMSEError(sr_L, succCount/totalTasks, scalar[domain]['sr']))
    if totalCountForRetries != 0:
        res['retryRatio'].append(retryCount/totalCountForRetries)
        res['rr_error'].append(GetMSEError(rr_L, retryCount/totalCountForRetries, 10))
    else:
        res['retryRatio'].append(0)
        res['rr_error'].append(0)
    res['planTime'].append(planTime/totalTasks)

    res['actTime'].append(actTime/totalTasks)
    
    res['totalTime'].append(time11/totalTasks)
    res['tt_error'].append(GetMSEError(tt_L, time11/totalTasks, 0.000000))

    res['nu'].append(nu / totalTasks)
    res['nu_error'].append(GetMSEError(nu_L, nu/totalTasks, scalar[domain]['nu']))
    res['timeOut'].append(timeOutCount)

def CommonStuffPlanningUtilities(res, domain, f_rae, param, fileName): # param may be k or d

    line = f_rae.readline()
    
    id = 0
    lineNumber = 0
    total = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            id += 1

            counts = f_rae.readline()
            lineNumber += 1
            print(fileName, " line number = ", lineNumber)
            while(NotTimeLine(counts)):
                if counts == '':
                    break
                if counts == "0 1 0 0 0 0 0 0 0\n":
                    pass

                parts2 = counts.split(' ')

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
                    total += 1
                    # update the planning utility error ratios
                    subs = planningUtils.split(' ')
                    commCount = 0
                    itr = 0
                    for item in subs:
                        chars = [str(i) for i in range(0,10)]
                        if item[0] in chars or item == "inf":

                            errorRatio = abs(taskEff - float(item))/(1 + taskEff)
                            if itr == 2:
                                if commCount in res:
                                    res[commCount] += errorRatio
                                else:
                                    res[commCount] = errorRatio
                            itr += 1
                            if itr == 3:
                                itr = 0
                        else:
                            commCount += 1
                            if commCount > 10:
                                break

                counts = f_rae.readline()
                lineNumber += 1
            
        line = f_rae.readline()
        lineNumber += 1

    for commCount in res:
        res[commCount] /= total

def PopulateHelper_SLATE_max_depth(res, domain, f_rae, k, fileName):
    CommonStuff(res, domain, f_rae, k, fileName)

def PopulateHelper_UCT_max_depth(res, domain, f_rae, uct, fileName):
    CommonStuff(res, domain, f_rae, uct, fileName)

def PopulateHelper_UCT_max_depth_planning_utilities(res, domain, f_rae, uct, fileName):
    CommonStuffPlanningUtilities(res, domain, f_rae, uct, fileName)

def PopulateHelper_SLATE_lim_depth(res, domain, f_rae, depth, fileName):
    CommonStuff(res, domain, f_rae, depth, fileName)

def PopulateHelper_UCT_lim_depth(res, domain, f_rae, depth, fileName):
    CommonStuff(res, domain, f_rae, depth, fileName)

def Populate_SLATE_max_depth(res, domain):
    for b in B_max_depth[domain]:
        for k in K_max_depth[domain]:
            if k == 0:
                f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper_SLATE_max_depth(res[b], domain, f_rae, k, f_rae_name)
                f_rae.close()
            else:
                fname = '{}{}_v_journal{}/rae_plan_b_{}_k_{}.txt'.format(resultsFolder, domain, util, b, k)
                fptr = open(fname)
                print(fname)
                PopulateHelper_SLATE_max_depth(res[b], domain, open(fname), k, fname)
                fptr.close()

def Populate_UCT_max_depth(res, domain, u):
    for uct in UCT_max_depth[domain]:
        if uct == 0:
            f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelper_UCT_max_depth(res, domain, f_rae, uct, f_rae_name)
            f_rae.close()
        else:
            fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, u, uct)
            fptr = open(fname)
            print(fname)
            PopulateHelper_UCT_max_depth(res, domain, open(fname), uct, fname)
            fptr.close()

def Populate_learning(res, domain, model):
    if model == "UCT":
        if domain == "CR":
            f1 = "{}{}_v_journal/rae_plan_uct_5000.txt".format(resultsFolder, domain)
        else:
            f1 = "{}{}_v_journal/rae_plan_uct_1000.txt".format(resultsFolder, domain)
        #if domain == "CR" or domain == "EE":
            #f1 = "{}{}_v_journal/RAE_with_planning.txt".format(resultsFolder, domain)
        #else:
        #    f1 = "{}{}_v_journal_eff/rae_plan_uct_100.txt".format(resultsFolder, domain)
    elif model == "SLATE":
        f1 = "{}{}_v_journal/rae_plan_b_2_k_2.txt".format(resultsFolder, domain)
    elif model == "reactive" or domain == "OF":
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    elif model == "heuristic_10_3":
        #if domain == "EE":
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_40_6.txt".format(resultsFolder, domain)
        #if domain == "CR" or domain == "SR":
        #    f1 = "{}{}_v_journal/RAE_with_learnH_training.txt".format(resultsFolder, domain)
        #else:
        f1 = "{}{}_v_journal/RAE_with_learnH.txt".format(resultsFolder, domain)
        #else:
        #    f1 = "{}{}_v_journal/RAE_with_trained_heuristic_10_3.txt".format(resultsFolder, domain)
    
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
    PopulateHelper_UCT_max_depth(res, domain, f1_p, 0, f1)
    f1_p.close()

def Populate_UCT_max_depth_planning_utilities(res, domain):
    for uct in UCT_max_depth[domain]:
        if uct == 0:
            f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
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

def Populate_SLATE_lim_depth(res, domain):  
    k = K_lim_depth[domain]
    for b in B_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth == 0:
                f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper_SLATE_lim_depth(res[b], domain, f_rae, depth, f_rae_name)
                f_rae.close()
            else:
                fname = '{}{}_v_journal{}/rae_plan_b_{}_k_{}_d_{}.txt'.format(resultsFolder, domain, util, b, k, depth)
                fptr = open(fname)
                print(fname)
                PopulateHelper_SLATE_lim_depth(res[b], domain, open(fname), depth, fname)
                fptr.close()

def Populate_UCT_lim_depth(res, domain, heuristic):  
    for uct in UCT_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth == 0:
                f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper_UCT_lim_depth(res[uct], domain, f_rae, depth, f_rae_name)
                f_rae.close()
            else:
                if heuristic == "h0":
                    h = "_h_h0"
                elif heuristic == "h1":
                    h = ""

                fname = '{}{}_v_journal_eff/rae_plan_uct_{}_d_{}'.format(resultsFolder, domain, uct, depth) \
                        + h + '.txt'.format()
                
                fptr = open(fname)
                print(fname)
                PopulateHelper_UCT_lim_depth(res[uct], domain, open(fname), depth, fname)
                fptr.close()

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
            resDict[domain][b] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
                'nu_error': [],
                'sr_error': [],
                'rr_error': [],
            }
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

def GeneratePlots_UCT_max_depth():
    resDict = {}
    for domain in D:
        if util == "_sr":
            resDict[domain] = {}
            resDict[domain]['_sr'] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
                'nu_error': [],
                'sr_error': [],
                'rr_error': [],
                'tt_error': [],
                }
            resDict[domain]['_eff'] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
                'nu_error': [],
                'sr_error': [],
                'rr_error': [],
                'tt_error': [],
                }
            Populate_UCT_max_depth(resDict[domain]['_sr'], domain, '_sr')
            Populate_UCT_max_depth(resDict[domain]['_eff'], domain, '_eff')
        else:
            resDict[domain] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
                'nu_error': [],
                'sr_error': [],
                'rr_error': [],
                'tt_error': [],
                }
            Populate_UCT_max_depth(resDict[domain], domain, '_eff')

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'regular',
        'size'   : 12}
    plt.rc('font', **font)
    

    print(resDict)
    for metric in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_UCT_max(resDict, metric)

def GeneratePlots_learning():
    resDict = {}
    for domain in D:
        resDict[domain] = {}
        resDict[domain]['reactive'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }
        resDict[domain]['SLATE'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }
        resDict[domain]['learning_from_actor'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }
        resDict[domain]['learning_from_planner'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }
        resDict[domain]['heuristic_10_3'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }
        resDict[domain]['UCT'] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }


        Populate_learning(resDict[domain]['UCT'], domain, 'UCT')
        Populate_learning(resDict[domain]['SLATE'], domain, 'SLATE')
        Populate_learning(resDict[domain]['reactive'], domain, 'reactive')
        

        # resDict[domain]['heuristic'] = {
        #     'successRatio': [], 
        #     'retryRatio': [],
        #     'planTime': [],
        #     'actTime': [],
        #     'totalTime': [],
        #     'nu': [],
        #     'timeOut': [],
        #     'nu_error': [],
        #     'sr_error': [],
        #     'rr_error': [],
        #     }
        # resDict[domain]['heuristic5'] = {
        #     'successRatio': [], 
        #     'retryRatio': [],
        #     'planTime': [],
        #     'actTime': [],
        #     'totalTime': [],
        #     'nu': [],
        #     'timeOut': [],
        #     'nu_error': [],
        #     'sr_error': [],
        #     'rr_error': [],
        #     }
        # resDict[domain]['heuristic0'] = {
        #     'successRatio': [], 
        #     'retryRatio': [],
        #     'planTime': [],
        #     'actTime': [],
        #     'totalTime': [],
        #     'nu': [],
        #     'timeOut': [],
        #     'nu_error': [],
        #     'sr_error': [],
        #     'rr_error': [],
        #     }
        # resDict[domain]['heuristic0_10_3'] = {
        #     'successRatio': [], 
        #     'retryRatio': [],
        #     'planTime': [],
        #     'actTime': [],
        #     'totalTime': [],
        #     'nu': [],
        #     'timeOut': [],
        #     'nu_error': [],
        #     'sr_error': [],
        #     'rr_error': [],
        #     }

        Populate_learning(resDict[domain]['learning_from_actor'], domain, 'actor')
        Populate_learning(resDict[domain]['learning_from_planner'], domain, 'planner')
        #Populate_learning(resDict[domain]['heuristic5'], domain, 'heuristic5')
        #Populate_learning(resDict[domain]['heuristic'], domain, 'heuristic')
        #Populate_learning(resDict[domain]['heuristic0'], domain, 'heuristic0')
        #Populate_learning(resDict[domain]['heuristic0_10_3'], domain, 'heuristic0_10_3')
        Populate_learning(resDict[domain]['heuristic_10_3'], domain, 'heuristic_10_3')

    
    print(resDict)
    
    for metric in ['totalTime']: #['nu', 'successRatio', 'retryRatio', 'totalTime']:
        PlotHelper_learning(resDict, metric, errIndex[metric])

def GeneratePlots_UCT_max_depth_planning_utilities():
    resDict = {}
    for domain in D:
        resDict[domain] = {}
        for uct in UCT_max_depth[domain]:
            resDict[domain][uct] = {}

    for domain in D:
        Populate_UCT_max_depth_planning_utilities(resDict[domain], domain)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    
    print(resDict)
    PlotHelper_UCT_max_planning_utilities(resDict)

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
            resDict[domain][b] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
                'nu_error': [],
                'sr_error': [],
                'rr_error': [],
                'tt_error': [],
            }

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

def GeneratePlots_UCT_lim_depth():
    global util
    resDict = {}
    assert(util == "_eff")
    for domain in D:
        resDict[domain] = {'h0': {}, 'h1': {}}
        for uct in UCT_lim_depth[domain]:
            resDict[domain]['h0'][uct] = GetFreshDict()
            resDict[domain]['h1'][uct] = GetFreshDict()
        Populate_UCT_lim_depth(resDict[domain]['h0'], domain, 'h0')
        Populate_UCT_lim_depth(resDict[domain]['h1'], domain, 'h1')

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
        for item in res2[0:6]:
            res1.append(item)
        #res1 = [item for item in res2[0:6]]

    else:
        for i in range(6):
            res1[i] += res2[i]

def PlotHelper_UCT_max_retryRatio(resDict):
    index1 = 'retryRatio'

    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    res = {'_sr': GetFreshDict(), '_eff': GetFreshDict()}

    assert(util == "_sr")

    for domain in D:
        Accumulate(res['_sr'][index1], resDict[domain]['_sr'][index1])
        Accumulate(res['_sr'][errIndex[index1]], resDict[domain]['_sr'][errIndex[index1]])
        Accumulate(res['_eff'][index1], resDict[domain]['_eff'][index1])
        Accumulate(res['_eff'][errIndex[index1]], resDict[domain]['_eff'][errIndex[index1]])
        
    plt.clf()
    fname = '{}{}_UCT_max_depth.png'.format(figuresFolder, 'retryRatio')
    
    fig, ax = plt.subplots()
    PlotViaMatlabBar([0, 50, 100, 250, 500, 1000], 
        res['_sr'][index1],
        res['_sr'][errIndex[index1]],
        COLORBAR[0],
        "utility = success ratio", -1, ax)
    PlotViaMatlabBar([0, 50, 100, 250, 500, 1000], 
        res['_eff'][index1],
        res['_eff'][errIndex[index1]],
        COLORBAR[1],
        "utility = efficiency", 1, ax)

    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
        
    ax.set_xticks(np.arange(6))
    ax.set_xticklabels([str(item) for item in [0, 50, 100, 250, 500, 1000]])
    plt.xlabel('Number of rollouts')
    plt.ylabel(GetYlabel('retryRatio'))

    plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_max(resDict, utilp):
    if utilp == "retryRatio":
        PlotHelper_UCT_max_retryRatio(resDict)
        return

    index1 = utilp
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_max_depth.png'.format(figuresFolder, domain, utilp)
        
        if util == "_sr":
            fig, ax = plt.subplots()
            PlotViaMatlabBar(UCT_max_depth[domain], 
                resDict[domain]['_sr'][index1],
                resDict[domain]['_sr'][errIndex[index1]],
                COLORBAR[0],
                "utility = success ratio", -1, ax)
            PlotViaMatlabBar(UCT_max_depth[domain], 
                resDict[domain]['_eff'][index1],
                resDict[domain]['_eff'][errIndex[index1]],
                COLORBAR[1],
                "utility = efficiency", 1, ax)
        else:
            fig, ax = plt.subplots()
            PlotViaMatlabBar(UCT_max_depth[domain], 
                resDict[domain][index1],
                resDict[domain][errIndex[index1]],
                COLORBAR[0],
                GetYlabel(utilp), 0, ax)
        
        plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        ax.set_xticks(np.arange(len(UCT_max_depth[domain])))
        ax.set_xticklabels([str(item) for item in UCT_max_depth[domain]])
        plt.xlabel('Number of rollouts')
        #plt.xticks(UCT_max_depth[domain],
        #   [str(item) for item in UCT_max_depth[domain]])
        plt.ylabel(GetYlabel(utilp))

        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_learning(resDict, utilp, errorP):
    index1 = utilp
    index1 = 'actTime'
    #K = [0, 1, 2, 3, 4, 8, 16]

    fname = '{}{}_learning.png'.format(figuresFolder, utilp)

    plt.clf()
    #font = {
    #    'family' : 'times',
    #    'weight' : 'regular',
    #    'size'   : 8}
    #plt.rc('font', **font)
    
    ax = {}
    ax['CR'] = plt.subplot2grid(shape=(2,4), loc=(0,0), colspan=2)
    ax['SD'] = plt.subplot2grid((2,4), (0,2), colspan=2)
    ax['EE'] = plt.subplot2grid((2,4), (1,0), colspan=2)
    ax['SR'] = plt.subplot2grid((2,4), (1,2), colspan=2)
    #ax['OF'] = plt.subplot2grid((2,4), (2,0), colspan=2)

    lowerLim = {
        "CR":
        {
            "nu": 0.065,
            "retryRatio": 0,
            "successRatio":0.68,
            'totalTime': 0,
        },
        "SR":
        {
            "nu":0,
            "retryRatio": 0,
            "successRatio":0.1,
            'totalTime': 0,
        },
        "EE":
        {
            "nu": 0,
            "retryRatio": 0,
            "successRatio":0.20,
            'totalTime': 0,
        },
        "SD":
        {
            "nu":0.018,
            "retryRatio": 0,
            "successRatio":0.7,
            'totalTime': 0,
        },
        "OF":
        {
            "nu": 0.01,
            "retryRatio": 0,
            "successRatio":0.6,
            'totalTime': 0,
        }
    }
    toPlot = {}

    for domain in D:
        toPlot = {'val': {}, 'err': {}}
        toPlot['val']['RAE\n(no planning)'] = resDict[domain]['reactive'][index1][0]
        toPlot['val']['RAEplan'] = resDict[domain]['SLATE'][index1][0]
        toPlot['val']['LearnM-1'] = resDict[domain]['learning_from_actor'][index1][0]
        toPlot['val']['LearnM-2'] = resDict[domain]['learning_from_planner'][index1][0]
        toPlot['val']['LearnH'] = resDict[domain]['heuristic_10_3'][index1][0]
        toPlot['val']['UPOM'] = resDict[domain]['UCT'][index1][0]

        # the errors
        #toPlot['err']['RAE (no planning)'] = resDict[domain]['reactive'][errorP][0]
        #toPlot['err']['RAEplan'] = resDict[domain]['SLATE'][errorP][0]
        #toPlot['err']['LearnM-1'] = resDict[domain]['learning_from_actor'][errorP][0]
        #toPlot['err']['LearnM-2'] = resDict[domain]['learning_from_planner'][errorP][0]
        #toPlot['err']['LearnH'] = resDict[domain]['heuristic_10_3'][errorP][0]
        #toPlot['err']['UPOM'] = resDict[domain]['UCT'][errorP][0]

        width = 0.85  # 0.003 the width of the bars
    

        labels = list(toPlot['val'].keys())
        x = np.arange(len(labels))

        print(domain)
        print(ptMax)
        print(list(toPlot['val'].values()))
        continue
        rects = ax[domain].bar(x, list(toPlot['val'].values()), width, 
            color=['turquoise', 'grey', 'orange', 'yellowgreen', 'orangered', 'orchid'],
            yerr=list(toPlot['err'].values()), capsize=3)
       
        patterns = ('\\', '\\\\', '/', '+', 'x', '\\\\\\\\')
        for bar, pattern in zip(rects, patterns):
            bar.set_hatch(pattern)

        ax[domain].set_ylim(bottom=lowerLim[domain][index1])
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
    #plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=1, borderaxespad=0.)
            

    #plt.savefig(fname, bbox_inches='tight')
    print("saved")

def PlotHelper_UCT_lim(resDict, utilp):
    index1 = utilp
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_lim_depth.png'.format(figuresFolder, domain, utilp)
        
        i = 0
        fig, ax = plt.subplots()
        for uct in UCT_lim_depth[domain]:
            PlotViaMatlabBar(Depth[domain],
                resDict[domain]['h0'][uct][index1],
                resDict[domain]['h0'][uct][errIndex[index1]],
                COLORBAR[i],
                'heuristic = h0', -1, ax)
            i += 1
            PlotViaMatlabBar(Depth[domain],
                resDict[domain]['h1'][uct][index1],
                resDict[domain]['h1'][uct][errIndex[index1]],
                COLORBAR[i],
                'heuristic = h1', +1, ax)
            i += 1
    
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=1, borderaxespad=0.)
            
        plt.xlabel('Depth')
        ax.set_xticks(np.arange(len(Depth[domain])))
        ax.set_xticklabels([str(item) for item in Depth[domain]])
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

def PlotHelper_UCT_max_planning_utilities(resDict):
    width = 0.25

    for domain in ['CR']:
        plt.clf()
        fname = '{}{}_UCT_max_depth_planning_utilities.png'.format(figuresFolder, util)
        
        i = 0
        for uct in UCT_max_depth[domain][1:]:
            sortedDict = {}
            for k in sorted(resDict[domain][uct]):
                sortedDict[k] = resDict[domain][uct][k]
                count = 1
                for x in ['EE', 'SR', 'SD', 'OF']:
                    if k in resDict[x][uct]:
                        sortedDict[k] += resDict[x][uct][k]
                        count += 1
                sortedDict[k] /= count
            print(sortedDict)
            PlotViaMatlabLine(sortedDict.keys(),
                sortedDict.values(),
                COLORS[i],
                'rollouts={}'.format(uct))
            i += 1
        
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        plt.xlabel('Number of commands executed')
        plt.xticks(list(sortedDict.keys()),
           GetString(list(sortedDict.keys())))
        plt.ylabel("Error ratio (normalized)") 
        plt.savefig(fname, bbox_inches='tight')

def PlotViaMatlabLine(x, y, c, l):
    line1, = plt.plot(x, y, c, 
        label=l, 
        linewidth=4, 
        MarkerSize=10, 
        markerfacecolor='white')
        
def PlotViaMatlabBar(x, y, y_error, c, l, f, ax):
    width = 0.4
    
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
heuristic = None
util = None
l = None

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SD', 'IP', 'SR', 'OF', 'EE']",
                           type=str, required=True)
    argparser.add_argument("--depth", help="depth = 'max' or 'lim'",
                           type=str, required=True)
    argparser.add_argument("--heuristic", help="Heuristic function name",
                           type=str, required=False, default='h2')
    argparser.add_argument("--s", help="SamplingStrategy ",
                           type=str, required=False, default="UCT")
    argparser.add_argument("--planning", help="PlanningUtilities", default='n',
                            type=str, required=False)
    argparser.add_argument("--utility", help="efficiency or successRatio?",
                            type=str, required=True)
    argparser.add_argument("--l", help="Compare with learning? ('y' or 'n')?",
                            type=str, default='n', required=True)
    args = argparser.parse_args()

    heuristic = args.heuristic
    learning = args.l
    if args.utility == "efficiency":
        util = "_eff"
    else:
        util = "_sr"
    D = ["SD", "CR", "EE", "SR", "OF"]
    #D = ["OF"]

    if args.l == "y":
        GeneratePlots_learning()
    elif args.depth == "max":
        if args.s == "SLATE":
            GeneratePlots_SLATE_max_depth()
        else:
            if args.planning == "n":
                GeneratePlots_UCT_max_depth()
            else:
                GeneratePlots_UCT_max_depth_planning_utilities()
    elif args.depth == "lim":
        if args.s == "SLATE":
            GeneratePlots_SLATE_lim_depth()
        else:
            if args.planning == "n":
                GeneratePlots_UCT_lim_depth()
            else:
                GeneratePlots_UCT_lim_depth_planning_utilities()
    else:
        print("Incorrect value depth: should be 'max' or 'lim'.")
