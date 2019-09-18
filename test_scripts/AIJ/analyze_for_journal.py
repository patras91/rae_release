__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse

figuresFolder = "figures/"
resultsFolder = "results/"

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
    'SR': [0, 5, 10, 15],
    'CR': [0, 5, 10, 15],
    'OF': [0, 5, 10, 15],
    'SD': [0, 5, 10, 15],
    'EE': [0, 5, 10, 15],
}

UCT_max_depth = {
    'CR': [0,5, 25, 50, 75],
    'SR': [0,5,25,50,75],
    'OF': [0, 5, 25, 50, 75],
    'SD': [0, 5, 25, 50, 75],
    'EE': [0, 5, 25, 50, 75],
}

UCT_lim_depth = {
    'CR': [5, 25, 50],
    'SR': [5, 25, 50],
    'OF': [5, 25, 50],
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

COLORS = ['ro:', 'bs--', 'm^-.', 'go--', 'c^:']

def NotTimeLine(s):
    if len(s) < 7:
        return True
    elif s[2:7] == "loops":
        return False
    else:
        return True

def CommonStuff(res, domain, f_rae, param, fileName): # param may be k or d

    line = f_rae.readline()
    
    succCount = 0
    totalTasks = 0
    
    retryCount = 0
    totalCountForRetries = 0

    planTime = 0
    actTime = 0
    time11 = 0

    clock = 0
    nu = 0

    timeOutCount = 0
    
    id = 0
    lineNumber = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            succ = 0
            total = 0

            for i in range(0, 1):
                id += 1

                counts = f_rae.readline()
                lineNumber += 1
                print(fileName, " line number = ", lineNumber)
                while(NotTimeLine(counts)):
                    if counts == '':
                        break
                    if counts == "0 1 0 0 0 0 0 0 0\n":
                        timeOutCount += 1

                    parts2 = counts.split(' ')

                    if parts2[0] != "v2":
                        version = 1
                        s = int(parts2[0])
                        t = int(parts2[1])
                        r = int(parts2[2])
                        planTime += float(parts2[3])
                        actTime += float(parts2[4])
                        taskEff = float(parts2[5])
                    else:
                        version = 2
                        s = int(parts2[1])
                        t = int(parts2[2])
                        r = int(parts2[3])
                        planTime += float(parts2[4])
                        actTime += float(parts2[5])
                        taskEff = float(parts2[6])

                    if taskEff == float("inf"):
                        print("Infinite efficiency! Normalizing.\n")
                        taskEff = 1/10
                    nu += taskEff
                    succCount += s
                    totalTasks += t

                    # for retry ratio
                    if s == t:
                        if ((id in succCases[domain]) and param > 0): #or (domain in ['CR', 'EE', 'SD', 'IP']):
                            retryCount += r
                            totalCountForRetries += t
                        elif param == 0:
                            succCases[domain].append(id)
                            retryCount += r
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
            t11 = float(parts11[5])
            unit11 = parts11[6]
            if unit11 == "msec":
                t11 = t11 / 1000
            time11 += t11
        line = f_rae.readline()
        lineNumber += 1

    res['successRatio'].append(succCount/totalTasks)
    if totalCountForRetries != 0:
        res['retryRatio'].append(retryCount/totalCountForRetries)
    else:
        res['retryRatio'].append(0)
    res['planTime'].append(planTime)
    res['actTime'].append(actTime)
    res['totalTime'].append(1 * planTime + 1 * actTime)
    res['nu'].append(nu / totalTasks)
    res['timeOut'].append(timeOutCount)

def CommonStuffPlanningUtilities(res, domain, f_rae, param, fileName): # param may be k or d

    line = f_rae.readline()
    
    id = 0
    lineNumber = 0
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            succ = 0
            total = 0

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
                    # update the planning utility error ratios
                    subs = planningUtils.split(' ')
                    commCount = 0
                    itr = 0
                    for item in subs:
                        chars = [str(i) for i in range(0,10)]
                        if item[0] in chars:
                            errorRatio = abs(taskEff - float(item))
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
                fname = '{}{}_v_journal/rae_plan_b_{}_k_{}.txt'.format(resultsFolder, domain, b, k)
                fptr = open(fname)
                print(fname)
                PopulateHelper_SLATE_max_depth(res[b], domain, open(fname), k, fname)
                fptr.close()

def Populate_UCT_max_depth(res, domain):
    for uct in UCT_max_depth[domain]:
        if uct == 0:
            f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelper_UCT_max_depth(res, domain, f_rae, uct, f_rae_name)
            f_rae.close()
        else:
            fname = '{}{}_v_journal/rae_plan_uct_{}.txt'.format(resultsFolder, domain, uct)
            fptr = open(fname)
            print(fname)
            PopulateHelper_UCT_max_depth(res, domain, open(fname), uct, fname)
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
            fname = '{}{}_v_journal/rae_plan_uct_{}.txt'.format(resultsFolder, domain, uct)
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
                fname = '{}{}_v_journal/rae_plan_b_{}_k_{}_d_{}.txt'.format(resultsFolder, domain, b, k, depth)
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
                fname = '{}{}_v_journal/rae_plan_uct_{}_d_{}.txt'.format(resultsFolder, domain, uct, depth)
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
        Populate_UCT_max_depth(resDict[domain], domain)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    

    print(resDict)
    for util in ['nu', 'successRatio', 'retryRatio']:
        PlotHelper_UCT_max(resDict, util)

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
        Populate_UCT_lim_depth(resDict[d], d)
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
        PlotHelper_UCT_lim(resDict, util)

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

def PlotHelper_UCT_max(resDict, util):
    index1 = util
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_max_depth.png'.format(figuresFolder, domain, util)
        PlotViaMatlab(UCT_max_depth[domain], 
            resDict[domain][index1],
            COLORS[0],
            GetYlabel(util))
        
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
            
        plt.xlabel('Number of rollouts')
        plt.xticks(UCT_max_depth[domain],
           [str(item) for item in UCT_max_depth[domain]])
        plt.ylabel(GetYlabel(util))

        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_lim(resDict, util):
    index1 = util
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_UCT_lim_depth.png'.format(figuresFolder, domain, util)
        
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
        plt.ylabel(GetYlabel(util)) 
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_SLATE_max(resDict, util):
    index1 = util
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
        
        fname = '{}{}_{}_SLATE_max_depth.png'.format(figuresFolder, domain, index1)
        plt.xlabel('k')
        plt.xticks(K_max_depth[domain],
           GetString(K_max_depth[domain]))
        plt.ylabel(GetYlabel(util))
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_SLATE_lim(resDict, util):
    index1 = util
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_{}_SLATE_lim_depth.png'.format(figuresFolder, domain, util)
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
        plt.ylabel(GetYlabel(util)) 
        plt.savefig(fname, bbox_inches='tight')

def PlotHelper_UCT_max_planning_utilities(resDict):
    width = 0.25

    for domain in D:
        plt.clf()
        fname = '{}{}_UCT_max_depth_planning_utilities.png'.format(figuresFolder, domain)
        
        i = 0
        for uct in UCT_max_depth[domain]:
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
        plt.ylabel("Expected Utility for Planning") 
        plt.savefig(fname, bbox_inches='tight')

def PlotViaMatlab(x, y, c, l):
    line1, = plt.plot(x, y, c, label=l, linewidth=4, MarkerSize=10, markerfacecolor='white')

D = None
heuristic = None

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SD', 'IP', 'SR', 'OF', 'EE']",
                           type=str, required=True)
    argparser.add_argument("--depth", help="depth = 'max' or 'lim'",
                           type=str, required=True)
    argparser.add_argument("--heuristic", help="Heuristic function name",
                           type=str, required=False, default='h2')
    argparser.add_argument("--s", help="SamplingStrategy ",
                           type=str, required=True)
    argparser.add_argument("--planning", help="PlanningUtilities", default='n',
                            type=str, required=False)
    args = argparser.parse_args()

    heuristic = args.heuristic
    D = [args.domain]
    if args.depth == "max":
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

def CalculateRunningTime_SLATE_max_depth(domain):
    for b in B_max_depth[domain]:
        for k in K_max_depth[domain]:
            print("b = ", b, ", k = ", k)
            if k == 0:
                f_rae_name = "{}/RAE.txt".format(domain)
                f_rae = open(f_rae_name, "r")
                #print(f_rae_name)
                PopulateHelper1_SLATE_max_depth(domain, f_rae, k)
                f_rae.close()
            else:
                fname = '{}/plan_b_{}_k_{}.txt'.format(domain, b, k)
                fptr = open(fname)
                #print(fname)
                PopulateHelper1_SLATE_max_depth(domain, open(fname), k)
                fptr.close()

def CalculateRunningTime_SLATE_lim_depth(domain):
    for b in B_lim_depth[domain]:
        for depth in Depth[domain]:
            print("b = ", b, ", depth = ", depth)
            if k == 0:
                f_rae_name = "{}_v8/RAE.txt".format(domain)
                f_rae = open(f_rae_name, "r")
                #print(f_rae_name)
                PopulateHelper1_SLATE_lim_depth(domain, f_rae, k, depth)
                f_rae.close()
            else:
                fname = '{}_v8/plan_b_{}_k_{}_d_{}.txt'.format(domain, b, k, depth)
                fptr = open(fname)
                #print(fname)
                PopulateHelper1_SLATE_lim_depth(domain, open(fname), k, depth)
                fptr.close()

def PlotRunningTime_SLATE_lim_depth1(resDict):
    index1 = 'totalTime'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(Depth[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(Depth[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(Depth[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(Depth[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=4, MarkerSize=10, markerfacecolor='white')        
        
        fname = 'RunningTime_SLATE_lim_depth_{}.png'.format(domain)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Running Time (in counter ticks)')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotRunningTime_SLATE_lim_depth(resDict):
    index1 = 'planTime'
    index2 = 'actTime'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(Depth[domain], resDict[domain][1][index1], 'ro:', label='b=1 Planning', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line11, = plt.plot(Depth[domain], resDict[domain][1][index2], 'ro:', label='b=1 Acting', linewidth=8, MarkerSize=10, markerfacecolor='white')
        
        #line2, = plt.plot(Depth[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line21, = plt.plot(Depth[domain], resDict[domain][2][index2], 'bs--', label='b=2', linewidth=6, MarkerSize=10, markerfacecolor='white')
        
        #line3, = plt.plot(Depth[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line31, = plt.plot(Depth[domain], resDict[domain][3][index2], 'm^-.', label='b=3', linewidth=6, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(Depth[domain], resDict[domain][4][index1], 'go--', label='b=4 Planning', linewidth=4, MarkerSize=10, markerfacecolor='white')        
            line41, = plt.plot(Depth[domain], resDict[domain][4][index2], 'go--', label='b=4 Acting', linewidth=8, MarkerSize=10, markerfacecolor='white')        
        
        fname = 'RunningTime_SLATE_lim_depth_{}.png'.format(domain)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Time (in counter ticks)')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')
