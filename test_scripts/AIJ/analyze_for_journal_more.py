__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse

figuresFolder = "figures/"
resultsFolder = "../../../raeResults/AIJ2020/"

B_max_depth = {
    "SD": [2,5,8],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [1, 2, 3],
    'SR': [2, 3, 4],
    'OF': [3, 6, 9]
}

B_lim_depth = {
    'SD': [2,5,8],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [1,2],
    'SR': [2, 3, 4],
    'OF': [3,6,9]
}

K_lim_depth = {
    'SD': 3,
    'EE': 3,
    'IP': 3,
    'CR': 3,
    'SR': 3,
}

K_max_depth = {
    "SD": [0, 1,3,5],
    'EE': [0, 1, 3, 5, 8, 10], #, 20, 50, 75, 100],
    'IP': [0, 3, 5, 7, 10],
    'CR': [0,1,3,5], #20, 30, 40, 50, 60, 70, 75, 80, 90, 100],
    'SR': [0, 1, 3, 5],
    'OF': [0, 1, 3, 5]
}

Depth = {
    'SR': [0, 5, 10, 15, 20],
    'CR': [0, 5, 10, 15, 20],
    'OF': [0, 10, 15], # 5
    'SD': [0, 5, 10, 15],
    'EE': [0, 5, 10, 15],
}

#UCT_max_depth = {
#    'CR': [0,5, 25, 50, 75, 100, 125],
#    'SR': [0,5, 25, 50, 75, 100, 125],
#    'OF': [0,5, 25, 50, 75, 100, 125, 150],
#    'SD': [0,5, 25, 50, 75, 100, 125],
#    'EE': [0,5, 25, 50, 75, 100, 125],
#}

UCT_max_depth = {
    'OF': [500, 1000, 1500, 2000],
}

UCT_lim_depth = {
    'CR': [50],
    'SR': [50],
    'OF': [5, 25, 50, 75, 100],
    'SD': [5, 25, 50],
    'EE': [5, 25, 50],
}

succCases = {
    'SD': [],
    'EE': [],
    'IP': [],
    'CR': [],
    'SR': [],
    'OF': [],
}

timeLimit = {
    "OF": 300,
    "CR": 300,
    "SR": 300,
    "EE": 300,
    "IP": 300,
    "SD": 300,
}


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
def GetCountAndTime(res, domain, f_rae, param, fileName): # param may be k or d

    line = f_rae.readline()
    
    totalRuns = 0
    totalTime = 0
    passCount = 0
    timeOutCount = 0
    highestTime = 0
    problems = set({})
    maxCommCount = 0
    minCommCount = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':
            totalRuns += 1
            problemName = parts[4]
            counts = f_rae.readline()
            if counts[0] == "T":
                passCount += 1
            while(NotTimeLine(counts)):
                if counts == '':
                    break

                parts2 = counts.split(' ')

                if parts2[0] != "v2":
                    version = 1
                else:
                    version = 2

                if version == 2:
                    commLine = f_rae.readline() # list of commands and planning efficiencies
                    comms = commLine.split()
                    numberOfCommands = 0
                    for item in comms:
                        if item[0] not in chars:
                            numberOfCommands += 1
                    if numberOfCommands < minCommCount:
                        minCommCount = numberOfCommands
                    elif numberOfCommands > maxCommCount:
                        maxCommCount = numberOfCommands

                counts = f_rae.readline()
            # time line
            secTimeLine = counts
            #print(secTimeLine)
            parts11 = secTimeLine.split()
            t11 = float(parts11[5])
            unit11 = parts11[6]
            if unit11 == "msec":
                t11 = t11 / 1000
            if t11 == timeLimit[domain]:
                timeOutCount += 1
            totalTime += t11
            if t11 > highestTime and t11 < timeLimit[domain]:
                highestTime = t11
            if t11 == timeLimit[domain]:
                problems.add(problemName)
        line = f_rae.readline()

    return totalRuns, totalTime/60, passCount, timeOutCount, highestTime, problems, minCommCount, maxCommCount


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
    f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    problems = GetProblems(open(f_rae_name))
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

def Get_UCT_max_depth_run_counts(res, domain):
    f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    problems, count = GetProblemsAndCounts(open(f_rae_name))
    for uct in UCT_max_depth[domain]:
        if uct > 0:
            fname = '{}{}_v_journal{}/rae_plan_uct_{}.txt'.format(resultsFolder, domain, util, uct)
            fptr = open(fname)
            count_uct, time, passCount, timeOutCount, highestTime, problems, minCommCount, maxCommCount = \
                GetCountAndTime(res, domain, open(fname), uct, fname)
            print("Domain ", domain, "uctCount = " , uct, "expected ", 
                count, "found ", count_uct, " time = ", time, 
                " passCount = ", passCount, " timeOutCount = ",timeOutCount,
                " highest count = ", highestTime)
            print("min Comm = ", minCommCount, " max Comm = ", maxCommCount)
            print(problems)
            fptr.close()
    print(res)
    print(len(res))

def Get_UCT_lim_depth_run_counts(res, domain):
    f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
    problems, count = GetProblemsAndCounts(open(f_rae_name))
    for uct in UCT_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth > 0:
                fname = '{}{}_v_journal{}/rae_plan_uct_{}_d_{}.txt'.format(resultsFolder, domain, util, uct, depth)
                fptr = open(fname)
                count_uct, time, passCount, timeOutCount, highestTime, problems, minCommCount, maxCommCount = \
                    GetCountAndTime(res, domain, open(fname), uct, fname)
                print("Domain ", domain, "depth = " , depth, "expected ", 
                    count, "found ", count_uct, " time = ", time, 
                    " passCount = ", passCount, " timeOutCount = ",timeOutCount,
                    " highest count = ", highestTime)
                print("min Comm = ", minCommCount, " max Comm = ", maxCommCount)
                print(problems)
                fptr.close()

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

def Populate_UCT_lim_depth(res, domain):  
    for uct in UCT_lim_depth[domain]:
        for depth in Depth[domain]:
            if depth == 0:
                f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
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
        resDict[domain] = {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            }
        #Get_UCT_max_depth_discrepencies(resDict[domain], domain)
        Get_UCT_max_depth_run_counts(resDict[domain], domain)

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
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {},
        'SR': {},
        'OF': {},
    }

    for domain in D:
        resDict[domain] = {}
        for uct in UCT_lim_depth[domain]:
            resDict[domain][uct] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': [],
                'timeOut': [],
            }
    for d in D:
        Get_UCT_lim_depth_run_counts(resDict[d], d)

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
        return 'Efficiency, $E$'
    elif util == 'successRatio':
        return 'Success Ratio'
    else:
        return 'Retry Ratio'

def PlotHelper_UCT_max(resDict, utilp):
    index1 = utilp
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_max_depth{}.png'.format(figuresFolder, domain, utilp, util)
        PlotViaMatlab(UCT_max_depth[domain], 
            resDict[domain][index1],
            COLORS[0],
            GetYlabel(utilp))
        
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        plt.xlabel('Number of rollouts')
        plt.xticks(UCT_max_depth[domain],
           [str(item) for item in UCT_max_depth[domain]])
        plt.ylabel(GetYlabel(utilp))

        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_lim(resDict, utilp):
    index1 = utilp
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_lim_depth{}.png'.format(figuresFolder, domain, utilp, util)
        
        i = 0
        for uct in UCT_lim_depth[domain]:
            PlotViaMatlab(Depth[domain],
                resDict[domain][uct][index1],
                COLORS[i],
                'rollouts={}'.format(uct))
            i += 1
        
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],
           GetString(Depth[domain]))
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

    for domain in D:
        plt.clf()
        fname = '{}{}_UCT_max_depth_planning_utilities{}.png'.format(figuresFolder, domain, util)
        
        i = 0
        for uct in UCT_max_depth[domain][1:]:
            sortedDict = {}
            for k in sorted(resDict[domain][uct]):
                sortedDict[k] = resDict[domain][uct][k]
            print(sortedDict)
            PlotViaMatlab(sortedDict.keys(),
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

def PlotViaMatlab(x, y, c, l):
    line1, = plt.plot(x, y, c, label=l, linewidth=4, MarkerSize=10, markerfacecolor='white')

D = None
heuristic = None
util = None

if __name__=="__main__":
    util = '_eff'
    D = ['OF']
    depth = "max"
    s = "UCT"
    if depth == "max":
        if s == "SLATE":
            GeneratePlots_SLATE_max_depth()
        else:
            GeneratePlots_UCT_max_depth()
    elif depth == "lim":
        if s == "SLATE":
            GeneratePlots_SLATE_lim_depth()
        else:
            GeneratePlots_UCT_lim_depth()
    else:
        print("Incorrect value depth: should be 'max' or 'lim'.")

def Plot(val, res, domain, plotMode, ii):
    plt.subplot(1, 4, ii)
    ylabel = ''

    index1 = 'successCount'
    ylabel = ''
    color1 = 'white'

    width = 0.25
    plt.bar(EditToFitBarPlot(val, 0 * width), res['active'][index1], width=width, edgecolor='black', hatch="/", label=label1, color=color1, linewidth=3)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), res['lazy'][index1], width=width, edgecolor='black', hatch="***", label=label3, tick_label=val, color='white', linewidth=3)
    #plt.bar(Edit(val, -0.1), res['concurrent'][mode], align='edge', width=-0.2, label='concurrent') # for aligning the right edge

    #plt.ylabel(ylabel)
    plt.xlabel('k1 in {}'.format(domain))
    #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #plt.savefig(fname, bbox_inches='tight')

def PopulateHelper1_SLATE_max_depth(domain, f_rae, k):

    line = f_rae.readline()
    
    time = 0
    
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            for i in range(0, 1):
                
                counts = f_rae.readline()

            secTimeLine = f_rae.readline()
            parts = secTimeLine.split()
            t = float(parts[5])
            unit = parts[6]
            if unit == "msec":
                t = t / 1000
            time += t

        line = f_rae.readline()

    print("running time = ", time)

def PopulateHelper1_SLATE_lim_depth(domain, f_rae, k, depth):

    line = f_rae.readline()
    
    time = 0
    
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            for i in range(0, 1):
                

                counts = f_rae.readline()


            secTimeLine = f_rae.readline()
            parts = secTimeLine.split()
            t = float(parts[5])
            unit = parts[6]
            if unit == "msec":
                t = t / 1000
            time += t

        line = f_rae.readline()

    print("running time = ", time)


