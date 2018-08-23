__author__ = 'patras'
import matplotlib.pyplot as plt
import csv

B = {
    'SD': [1, 2, 3, 4],
    'EE': [1, 2, 3],
    'IP': [1, 2],
    'CR': [1, 2, 3],
}

K = {
    'SD': [0, 1,2,3,4],
    'EE': [0, 1, 2, 3, 4, 8, 12, 16],
    'IP': [0, 1, 2],
    'CR': [0, 1, 2, 3, 4, 8, 12, 16],
}
penalty = {
    'SD': 0.2,
    'EE': 0.1,
    'CR': 0.0,
    'IP': 0.1
}

succCases = {
    'SD': [],
    'EE': [],
    'IP': [],
    'CR': [],
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
    res['successRatio'].append(succCount/totalTasks)
    if totalCountForRetries != 0:
        res['retryRatio'].append(retryCount/totalCountForRetries)
    else:
        res['retryRatio'].append(0)
    res['planTime'].append(planTime)
    res['actTime'].append(actTime)
    res['nu'].append(nu / totalTasks)

def Populate(res, domain):
    for b in B[domain]:
        for k in K[domain]:
            if k == 0:
                f_rae_name = "{}/RAE.txt".format(domain)
                f_rae = open(f_rae_name, "r")
                print(f_rae_name)
                PopulateHelper(res[b], domain, f_rae, k)
                f_rae.close()
            else:
                fname = '{}/plan_b_{}_k_{}.txt'.format(domain, b, k)
                fptr = open(fname)
                print(fname)
                PopulateHelper(res[b], domain, open(fname), k)
                fptr.close()

def GeneratePlots():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {}
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
    Populate(resDict['CR'], 'CR')
    Populate(resDict['SD'], 'SD')
    Populate(resDict['EE'], 'EE')

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
    D = ['CR', 'EE', 'SD']
    index1 = 'nu'
    width = 0.25
    #K = [0, 1, 2, 3, 4, 8, 16]

    for domain in D:
        plt.clf()
        fname = 'Nu_{}.png'.format(domain)
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
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
        plt.ylabel('Efficiency, $\\nu$') 
        plt.savefig(fname, bbox_inches='tight')

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
    D = ['CR', 'EE', 'SD']
    index1 = 'retryRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
        
        fname = 'RetryRatio_{}.png'.format(domain)
        plt.xlabel('k')
        plt.ylabel('Retry Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotSuccessRatio(resDict):
    D = ['CR', 'EE', 'SD']
    index1 = 'successRatio'
    width = 0.25

    for domain in D:
        plt.clf()
        line1, = plt.plot(K[domain], resDict[domain][1][index1], 'ro:', label='b=1', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line2, = plt.plot(K[domain], resDict[domain][2][index1], 'bs--', label='b=2', linewidth=2, MarkerSize=10, markerfacecolor='white')
        line3, = plt.plot(K[domain], resDict[domain][3][index1], 'm^-.', label='b=3', linewidth=4, MarkerSize=10, markerfacecolor='white')
        
        if domain == 'SD':
            line4, = plt.plot(K[domain], resDict[domain][4][index1], 'go--', label='b=4', linewidth=3, MarkerSize=10, markerfacecolor='white')        
        
        fname = 'SuccessRatio_{}.png'.format(domain)
        plt.xlabel('k')
        plt.ylabel('Success Ratio')
        plt.legend(bbox_to_anchor=(-0.2, 1.05), loc=3, ncol=3, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')


def GetSum(*l):
    size = len(l[0])
    res = []
    for i in range(0, size):
        res.append(0)
        for item in l:
            res[i] += item[i]
    return res

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

if __name__=="__main__":
    GeneratePlots()