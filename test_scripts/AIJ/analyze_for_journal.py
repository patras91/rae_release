__author__ = 'patras'
import matplotlib.pyplot as plt
import csv
import argparse

figuresFolder = "figures/"
resultsFolder = "results/"

B = {
    'SD': [1, 2, 3, 4],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [1, 2, 3],
    'SR': [1, 2, 3, 4],
}

B_depth = {
    'SD': [4],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [3],
    'SR': [1, 2, 3, 4],
}

K_depth = {
    'SD': 4,
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': 3,
    'SR': [1, 2, 3, 4],
}

K = {
    'SD': [0, 1, 3, 5, 8, 10],
    'EE': [0, 1, 3, 5, 8, 10], #, 20, 50, 75, 100],
    'IP': [0, 3, 5, 7, 10],
    'CR': [0, 1, 3, 5, 8, 10], #20, 30, 40, 50, 60, 70, 75, 80, 90, 100],
    'SR': [0, 1, 3, 5, 8, 10]
}

Depth = {
    'SR': [0, 3, 6, 9, 12, 15],
    'CR': [0, 1, 3, 5, 7, 9],
    #'SR': [0, 5, 10, 15]
}

succCases = {
    'SD': [],
    'EE': [],
    'IP': [],
    'CR': [],
    'SR': [],
}

def PopulateHelper(res, domain, f_rae, k):

    line = f_rae.readline()
    
    succCount = 0
    totalTasks = 0
    
    retryCount = 0
    totalCountForRetries = 0

    planTime = 0
    actTime = 0
    
    clock = 0
    nu = 0
    
    id = 0
    
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            succ = 0
            total = 0

            for i in range(0, 1):
                id += 1

                counts = f_rae.readline()
                if counts == '':
                    break
                parts2 = counts.split(' ')

                s = int(parts2[0])
                t = int(parts2[1])
                r = int(parts2[2])
                planTime += int(parts2[3])
                actTime += int(parts2[4])
                nu += float(parts2[5])

                succCount += s
                totalTasks += t

                # for retry ratio
                if s == t:
                    if ((id in succCases[domain]) and k > 0): #or (domain in ['CR', 'EE', 'SD', 'IP']):
                        retryCount += r
                        totalCountForRetries += t
                    elif k == 0:
                        succCases[domain].append(id)
                        retryCount += r
                        totalCountForRetries += t
                    else:
                        pass
                else:
                    pass

            secTimeLine = f_rae.readline()

        line = f_rae.readline()

    print(res)

    print(len(res['successRatio']), "k = ", k)
    k_index = K[domain].index(k)
    if K[domain].index(k) == len(res['successRatio']):
        res['successRatio'].append(succCount/totalTasks)
        if totalCountForRetries != 0:
            res['retryRatio'].append(retryCount/totalCountForRetries)
        else:
            res['retryRatio'].append(0)
        res['planTime'].append(planTime)
        res['actTime'].append(actTime)
        res['nu'].append(nu / totalTasks)
    else:
        res['successRatio'][k_index] += succCount/totalTasks
        if totalCountForRetries != 0:
            res['retryRatio'][k_index] += retryCount/totalCountForRetries
        else:
            res['retryRatio'][k_index] += 0
        res['planTime'][k_index] += planTime
        res['actTime'][k_index] += actTime
        res['nu'][k_index] += nu / totalTasks

def PopulateHelper1(domain, f_rae, k):

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

def Populate(res, domain):
    for b in B[domain]:
        for k in K[domain]:
            if k == 0:
                for v in range(3, 4):
                    f_rae_name = "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)
                    f_rae = open(f_rae_name, "r")
                    print(f_rae_name)
                    PopulateHelper(res[b], domain, f_rae, k)
                    f_rae.close()
            else:
                for v in range(3, 4):
                    fname = '{}{}_v_journal/rae_plan_b_{}_k_{}.txt'.format(resultsFolder, domain, b, k)
                    fptr = open(fname)
                    print(fname)
                    PopulateHelper(res[b], domain, open(fname), k)
                    fptr.close()

def CalculateRunningTime(domain):
    for b in B[domain]:
        for k in K[domain]:
            print("b = ", b, ", k = ", k)
            if k == 0:
                f_rae_name = "{}/RAE.txt".format(domain)
                f_rae = open(f_rae_name, "r")
                #print(f_rae_name)
                PopulateHelper1(domain, f_rae, k)
                f_rae.close()
            else:
                fname = '{}/plan_b_{}_k_{}.txt'.format(domain, b, k)
                fptr = open(fname)
                #print(fname)
                PopulateHelper1(domain, open(fname), k)
                fptr.close()

def GeneratePlotsForbAndk():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {},
        'SR': {},
    }

    for domain in resDict:
        resDict[domain] = {}
        for b in B[domain]:
            resDict[domain][b] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'nu': []
            }
    #Populate(resDict['CR'], 'CR')
    #Populate(resDict['SD'], 'SD')
    #Populate(resDict['IP'], 'IP')
    for d in D:
        Populate(resDict[d], d)
        #CalculateRunningTime(d)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    PlotNuAAAI(resDict)

    PlotRetryRatio(resDict)

    PlotSuccessRatio(resDict)

def PlotNuAAAI(resDict):
    index1 = 'nu'
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = '{}Nu_{}.png'.format(figuresFolder, domain)
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=4, MarkerSize=10, markerfacecolor='white')        
        #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
                
        # Create a legend for the first line.
        #first_legend = plt.legend(handles=[line1], loc=10)

        # Add the legend manually to the current Axes.
        #ax = plt.gca().add_artist(first_legend)

        # Create another legend for the second line.
        #leg2 = plt.legend(handles=[line2], loc=9)

        #bx = plt.gca().add_artist(leg2)

        #plt.legend(handles=[line3], loc=8)
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
            
        plt.xlabel('k')
        plt.xticks([0, 1, 3, 5, 8, 10],
           ['0', '1', '3', '5', '8', '10'])
        plt.ylabel('Efficiency, $E$') 
        plt.savefig(fname, bbox_inches='tight')

def GetString(depth):
    s = []
    for item in depth:
        s.append(str(item))

    return s

def PlotNuAAAIDepth(resDict):
    index1 = 'nu'
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = '{}AIJ_Nu_Depth_{}_h_{}.png'.format(figuresFolder, domain, heuristic)
        line1, = plt.plot(Depth[domain], resDict[domain][B_depth[domain][0]][index1], 'ro:', label='b={}'.format(B_depth[domain][0]), linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line2, = plt.plot(Depth[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line3, = plt.plot(Depth[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        #if domain == 'SD' or domain == 'SR':
        #    line4, = plt.plot(Depth[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=4, MarkerSize=10, markerfacecolor='white')        
        
        #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
                
        # Create a legend for the first line.
        #first_legend = plt.legend(handles=[line1], loc=10)

        # Add the legend manually to the current Axes.
        #ax = plt.gca().add_artist(first_legend)

        # Create another legend for the second line.
        #leg2 = plt.legend(handles=[line2], loc=9)

        #bx = plt.gca().add_artist(leg2)

        #plt.legend(handles=[line3], loc=8)
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
            
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Efficiency, $E$') 
        plt.savefig(fname, bbox_inches='tight')

def PopulateHelperDepth(res, domain, f_rae, k, depth):

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
    
    id = 0
    
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            succ = 0
            total = 0

            for i in range(0, 1):
                id += 1

                counts = f_rae.readline()
                if counts == '':
                    break
                parts2 = counts.split(' ')

                s = int(parts2[0])
                t = int(parts2[1])
                r = int(parts2[2])
                planTime += int(parts2[3])
                if s == t:
                    actTime += int(parts2[4])
                else:
                    actTime += int(parts2[4])
                nu += float(parts2[5])

                succCount += s
                totalTasks += t

                # for retry ratio
                if s == t:
                    if ((id in succCases[domain]) and depth > 0): #or (domain in ['CR', 'EE', 'SD', 'IP']):
                        retryCount += r
                        totalCountForRetries += t
                    elif depth == 0:
                        succCases[domain].append(id)
                        retryCount += r
                        totalCountForRetries += t
                    else:
                        pass
                else:
                    pass

            secTimeLine = f_rae.readline()
            parts11 = secTimeLine.split()
            t11 = float(parts11[5])
            unit11 = parts11[6]
            if unit11 == "msec":
                t11 = t11 / 1000
            time11 += t11
        line = f_rae.readline()

    print(res)

    print(len(res['successRatio']), "depth = ", depth)
    k_index = Depth[domain].index(depth)
    if Depth[domain].index(depth) == len(res['successRatio']):
        res['successRatio'].append(succCount/totalTasks)
        if totalCountForRetries != 0:
            res['retryRatio'].append(retryCount/totalCountForRetries)
        else:
            res['retryRatio'].append(0)
        res['planTime'].append(planTime)
        res['actTime'].append(1 * actTime)
        res['totalTime'].append(1 * planTime + 1 * actTime)
        #res['totalTime'].append(time11)
        res['nu'].append(nu / totalTasks)
    else:
        res['successRatio'][k_index] += succCount/totalTasks
        if totalCountForRetries != 0:
            res['retryRatio'][k_index] += retryCount/totalCountForRetries
        else:
            res['retryRatio'][k_index] += 0
        res['planTime'][k_index] += planTime
        res['actTime'][k_index] += 1 * actTime
        res['totalTime'] += 1 * planTime + 1 * actTime
        #res['totalTime'] += time11
        res['nu'][k_index] += nu / totalTasks

def PopulateHelper1Depth(domain, f_rae, k, depth):

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

def PopulateDepth(res, domain):  
    k = K_depth[domain]
    b = B_depth[domain][0]
    for depth in Depth[domain]:
        if depth == 0:
            f_rae_name = "{}/{}_v_journal/RAE.txt".format(resultsFolder, domain)
            f_rae = open(f_rae_name, "r")
            print(f_rae_name)
            PopulateHelperDepth(res[b], domain, f_rae, k, depth)
            f_rae.close()
        else:
            fname = '{}{}_v_journal/rae_plan_b_{}_k_{}_d_{}_h_{}.txt'.format(resultsFolder, domain, b, k, depth, heuristic)
            fptr = open(fname)
            print(fname)
            PopulateHelperDepth(res[b], domain, open(fname), k, depth)
            fptr.close()

def CalculateRunningTimeDepth(domain):
    for b in B[domain]:
        for depth in Depth[domain]:
            print("b = ", b, ", depth = ", depth)
            if k == 0:
                f_rae_name = "{}_v8/RAE.txt".format(domain)
                f_rae = open(f_rae_name, "r")
                #print(f_rae_name)
                PopulateHelper1Depth(domain, f_rae, k, depth)
                f_rae.close()
            else:
                fname = '{}_v8/plan_b_{}_k_{}_d_{}.txt'.format(domain, b, k, depth)
                fptr = open(fname)
                #print(fname)
                PopulateHelper1Depth(domain, open(fname), k, depth)
                fptr.close()

def GeneratePlotsForDepth():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {},
        'SR': {},
    }

    for domain in resDict:
        resDict[domain] = {}
        for b in B_depth[domain]:
            resDict[domain][b] = {
                'successRatio': [], 
                'retryRatio': [],
                'planTime': [],
                'actTime': [],
                'totalTime': [],
                'nu': []
            }

    for d in D:
        PopulateDepth(resDict[d], d)
        #CalculateRunningTimeDepth(d)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    PlotNuAAAIDepth(resDict)

    PlotRetryRatioDepth(resDict)

    PlotSuccessRatioDepth(resDict)

    #PlotRunningTimeDepth(resDict)

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

def PlotRetryRatio(resDict):
    index1 = 'retryRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
        
        fname = '{}RetryRatio_{}.png'.format(figuresFolder, domain)
        plt.xlabel('k')
        plt.xticks([0, 1, 3, 5, 8, 10],
           ['0', '1', '3', '5', '8', '10'])
        plt.ylabel('Retry Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotRetryRatioDepth(resDict):
    index1 = 'retryRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(Depth[domain], 
            resDict[domain][B_depth[domain][0]][index1], 
            'ro:', label='b={}'.format(B_depth[domain][0]), 
            linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line2, = plt.plot(Depth[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        #line3, = plt.plot(Depth[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        #if domain == 'SD' or domain == 'SR':
        #   line4, = plt.plot(Depth[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
        
        fname = '{}AIJ_RetryRatioDepth_{}_h_{}.png'.format(figuresFolder, domain, heuristic)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Retry Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotSuccessRatio(resDict):
    index1 = 'successRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
        
        fname = '{}SuccessRatio_{}.png'.format(figuresFolder, domain)
        plt.xlabel('k')
        plt.xticks([0, 1, 3, 5, 8, 10],
           ['0', '1', '3', '5', '8', '10'])
        plt.ylabel('Success Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotSuccessRatioDepth(resDict):
    index1 = 'successRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(Depth[domain], 
            resDict[domain][B_depth[domain][0]][index1], 
            'ro:', label='b={}'.format(B_depth[domain][0]), 
            linewidth=4, 
            MarkerSize=10, markerfacecolor='white')
        
        fname = '{}AIJ_SuccessRatioDepth_{}_h_{}.png'.format(figuresFolder, domain, heuristic)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Success Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotRunningTimeDepth1(resDict):
    index1 = 'totalTime'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(Depth[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(Depth[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=4, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(Depth[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD' or domain == 'SR':
            line4, = plt.plot(Depth[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=4, MarkerSize=10, markerfacecolor='white')        
        
        fname = 'RunningTimeDepth_{}.png'.format(domain)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Running Time (in counter ticks)')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotRunningTimeDepth(resDict):
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
        
        fname = 'RunningTimeDepth_{}.png'.format(domain)
        plt.xlabel('Depth')
        plt.xticks(Depth[domain],GetString(Depth[domain]))
        plt.ylabel('Time (in counter ticks)')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=2, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def GetSum(*l):
    size = len(l[0])
    res = []
    for i in range(0, size):
        res.append(0)
        for item in l:
            res[i] += item[i]
    return res

D = None
heuristic = None

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain",
                           type=str, required=True)
    argparser.add_argument("--depth", help="depth",
                           type=int, required=True)
    argparser.add_argument("--heuristic", help="Heuristic",
                           type=str, required=True)
    args = argparser.parse_args()

    heuristic = args.heuristic
    D = [args.domain]
    if args.depth == 0:    
        GeneratePlotsForbAndk()
    else:
        GeneratePlotsForDepth()

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