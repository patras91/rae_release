__author__ = 'patras'
import matplotlib.pyplot as plt
import csv

totalCommandCount = 0
K = {
    'SD': [0, 1, 2, 3, 4],
    'EE': [0, 1, 2, 3, 4],
    'IP': [0, 1, 2],
    'CR': [0, 1, 2, 3]
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

COMMANDS = {
    'CR': {
        'put': 0, #for domain CR
        'take': 0,
        'charge': 0,
        'move': 0,
        'addressEmergency': 0,
        'moveToEmergency': 0,
        'wait': 0,
    },
    'SD': {
        'openDoor': 0, #for domain SD
        'holdDoor': 0,
        'passDoor': 0,
        'releaseDoor': 0,
        'closeDoors': 0,
        'move': 0,
        'take': 0,
        'put': 0,
    },
    'EE': {
        'survey': 0, # for domain EE
        'monitor': 0,
        'screen': 0,
        'sample': 0,
        'process': 0,
        'fly': 0,
        'deposit': 0,
        'transferData': 0,
        'take': 0,
        'put': 0,
        'move': 0,
        'charge': 0,
        'handleAlien': 0
    },
    'IP': {
        'paint': 0, # for domain IP
        'assemble': 0,
        'pack': 0,
        'move': 0,
        'take': 0,
        'put': 0,
        'wrap': 0,
        'damage': 0,
        'repair': 0
    }
}

def PopulateHelper(res, domain, f_rae, k):
    line = f_rae.readline()
    succCount = 0
    totalCount = 0
    totalTasks = 0
    retryCount = 0
    simTime = 0
    runTime = 0
    commandTotal = 0
    resCmdCount = {}
    clock = 0
    nu = 0
    id = 0
    rinv = 0
    nudet = []
    while(line != ''):

        parts = line.split(' ')

        if parts[0] == 'Time':

            commSum = 0
            succ = 0
            total = 0
            for i in range(0, 6):
                id += 1
                counts = f_rae.readline()
                parts2 = counts.split(' ')
                succCount += int(parts2[0])
                totalTasks += int(parts2[1])

                #for rinv
                if int(parts2[0]) == int(parts2[1]):
                    if int(parts2[2]) == 0:
                        rinv += 2
                    else:
                        rinv += 1/int(parts2[2])

                # for retry ratio
                if ( True or int(parts2[0]) == int(parts2[1])) or (domain in ['EE', 'CR'] and (int(parts2[0]) > 0)): # or (domain in ['CR', 'EE', 'SD', 'IP']):
                    if (True or ((id in succCases[domain]) and k > 0)): #or (domain in ['CR', 'EE', 'SD', 'IP']):
                        #print(succCases[domain])
                        retryCount += int(parts2[2])
                        totalCount += int(parts2[1])
                    elif k == 0:
                        succCases[domain].append(id)
                        retryCount += int(parts2[2])
                        totalCount += int(parts2[1])
                    else:
                        pass
                        #print(id, domain)
                else:
                    pass
                    #print("error")

                simTime += int(parts2[3])
                runTime += int(parts2[4])
                commandCounts = f_rae.readline()
                commands = commandCounts.split(' ')

                for comm in commands:
                    commParts = comm.split('-')
                    if commParts[0] in resCmdCount:
                        resCmdCount[commParts[0]] += int(commParts[1])
                    else:
                        resCmdCount[commParts[0]] = int(commParts[1])
                    commandTotal += int(commParts[1])
                    commSum += int(commParts[1])

                if int(parts2[0]) == int(parts2[1]):
                    succ += int(parts2[0])
                total += int(parts2[1])

            secTimeLine = f_rae.readline()
            secParts = secTimeLine.split(' ')
            sec = float(secParts[5])
            if secParts[6] == 'msec':
                sec = sec / 1000

            if succ / total >= 1:
                #print(domain, succ/total)
                nu += 1 / (sec*total + 250 * commSum)
                nudet.append(1000 / (sec*total + 250 * commSum))
                clock += 1/sec
            else:
                nudet.append(0)
        line = f_rae.readline()

    #res['successCount'].append(succCount * 100 / totalCount)
    #sucNorm = succCount - penalty[domain] * retryCount
    #if sucNorm < 0:
    #    sucNorm = 0
    #print(succCount/totalTasks, totalTasks)
    res['successCount'].append(succCount/totalTasks)
    if domain == 'IP':
        retryCount *= 10
    #elif domain in ['EE', 'CR']:
    #    retryCount /= 4
    #print(domain, succCases[domain])
    #if totalCount != 0:
    if domain == 'EE':
        print(retryCount/totalCount)
    res['retryCount'].append(retryCount/totalCount)
    #else:
        #res['retryCount'].append(0)
    res['counter'].append(simTime + runTime)
    res['totalCount'].append(totalCount)
    res['commandTotal'].append(commandTotal)
    global totalCommandCount
    totalCommandCount += commandTotal
    # if len(res['runTime']) >= 1:
    #     succ0 = res['successCount'][0] + penalty[domain] * res['retryCount'][0]
    #     res['runTime'].append(runTime * succ0/succCount)
    # else:
    res['clock'].append(clock)
    res['commandCounts'].append(resCmdCount)
    res['nu'].append(nu * 10000)
    res['rinv'].append(rinv)
    res['nuDet'].append(nudet)

def Populate(res, domain, simmode):
    for k in K[domain]:
        if k == 0:
            f_rae_name = "outputs_with_arbitrary_order/{}/RAE.txt".format(domain)
            f_rae = open(f_rae_name, "r")
            PopulateHelper(res, domain, f_rae, k)
            f_rae.close()
        else:
            if simmode == 'active':
                fname = 'outputs_with_arbitrary_order/{}/active/K{}.txt'.format(domain, k)
            elif simmode == 'lazy':
                fname = 'outputs_with_arbitrary_order/{}/lazy/K{}.txt'.format(domain, k)
            elif simmode == 'concurrent':
                fname = 'outputs_with_arbitrary_order/{}/conc/K{}.txt'.format(domain, k)
            fptr = open(fname)
            print(fname)
            PopulateHelper(res, domain, open(fname), k)
            fptr.close()

def GeneratePlots():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {}
    }

    for domain in resDict:
        resDict[domain] = {'active': {}, 'lazy': {}} #, 'concurrent': {}}
        for APEmode in resDict[domain]:
            resDict[domain][APEmode] = {'counter': [], 'clock': [], 'successCount': [], 'totalCount': [],  'retryCount': [], 'commandTotal': [], 'nu': [], 'rinv': [], 'commandCounts': [], 'nuDet':[]}
            Populate(resDict[domain][APEmode], domain, APEmode)

    #PrintToFile(resDict)
    resDict['IP']['active']['counter'].append(0)
    resDict['IP']['active']['clock'].append(0)
    resDict['IP']['active']['commandTotal'].append(resDict['IP']['active']['commandTotal'][-1])

    resDict['IP']['lazy']['counter'].append(0)
    resDict['IP']['lazy']['clock'].append(0)
    resDict['IP']['lazy']['commandTotal'].append(resDict['IP']['lazy']['commandTotal'][-1])

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    #PlotSimTimes(resDict)

    #plt.clf()
    #PlotRunningTimes(resDict)
    #plt.clf()
    #PlotSuccessCounts(resDict)

    plt.clf()
    resDict['IP']['active']['retryCount'].append(resDict['IP']['active']['retryCount'][-1])
    resDict['IP']['active']['retryCount'].append(resDict['IP']['active']['retryCount'][-1])
    resDict['CR']['active']['retryCount'].append(resDict['CR']['active']['retryCount'][-1])
    resDict['IP']['lazy']['retryCount'].append(resDict['IP']['lazy']['retryCount'][-1])
    resDict['IP']['lazy']['retryCount'].append(resDict['IP']['lazy']['retryCount'][-1])
    resDict['CR']['lazy']['retryCount'].append(resDict['CR']['lazy']['retryCount'][-1])
    #PlotRetrySideBySide(resDict)
    #PlotRetryTopped(resDict)
    PlotRetryToppedSep(resDict)

    resDict['IP']['active']['rinv'].append(resDict['IP']['active']['rinv'][-1])
    resDict['IP']['active']['rinv'].append(resDict['IP']['active']['rinv'][-1])
    resDict['CR']['active']['rinv'].append(resDict['CR']['active']['rinv'][-1])
    resDict['IP']['lazy']['rinv'].append(resDict['IP']['lazy']['rinv'][-1])
    resDict['IP']['lazy']['rinv'].append(resDict['IP']['lazy']['rinv'][-1])
    resDict['CR']['lazy']['rinv'].append(resDict['CR']['lazy']['rinv'][-1])
    plt.clf()
    #PlotRetryInv(resDict)
    #PlotRetryCounts(resDict)

    plt.clf()
    resDict['IP']['active']['successCount'].append(resDict['IP']['active']['successCount'][-1])
    resDict['IP']['active']['successCount'].append(resDict['IP']['active']['successCount'][-1])
    resDict['CR']['active']['successCount'].append(resDict['CR']['active']['successCount'][-1])
    resDict['IP']['lazy']['successCount'].append(resDict['IP']['lazy']['successCount'][-1])
    resDict['IP']['lazy']['successCount'].append(resDict['IP']['lazy']['successCount'][-1])
    resDict['CR']['lazy']['successCount'].append(resDict['CR']['lazy']['successCount'][-1])
    #PlotSuccessTopped(resDict)
    plt.clf()
    #PlotCommandTotals(resDict)
    PlotSuccessToppedSep(resDict)

    #plt.clf()
    #PlotNu(resDict)


    #plt.clf()
    #PlotNuTogether(resDict)

    resDict['IP']['active']['nu'].append(resDict['IP']['active']['nu'][-1])
    resDict['IP']['active']['nu'].append(resDict['IP']['active']['nu'][-1])
    resDict['CR']['active']['nu'].append(resDict['CR']['active']['nu'][-1])
    resDict['IP']['lazy']['nu'].append(resDict['IP']['lazy']['nu'][-1])
    resDict['IP']['lazy']['nu'].append(resDict['IP']['lazy']['nu'][-1])
    resDict['CR']['lazy']['nu'].append(resDict['CR']['lazy']['nu'][-1])

    plt.clf()
    #PlotNuAcc(resDict)
    PlotNuToppedSep(resDict)
    #PlotNuDet(resDict)

def PlotNu(resDict):
    index1 = 'nu'
    width = 0.25

    for domain in resDict:
        plt.clf()
        plt.bar(EditToFitBarPlot(K[domain], 0 * width), resDict[domain]['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=K[domain], linewidth=3)
        plt.bar(EditToFitBarPlot(K[domain], 1 * width), resDict[domain]['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch=".", tick_label=K[domain], linewidth=3)

        fname = '../../../hiofsm/IJCAI2018/figures/Nu{}.png'.format(domain)
        plt.xlabel('k1')
        plt.ylabel('Speed $\\nu$') # for {}'.format(domain))
        #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
        plt.savefig(fname, bbox_inches='tight')

def PlotNuTogether(resDict):
    index1 = 'nu'
    width = 0.25
    plt.clf()
    i = 1
    for domain in ['CR', 'EE', 'SD', 'IP']:
        plt.subplot(1,4,i)

        plt.bar(EditToFitBarPlot(K[domain], 0 * width), resDict[domain]['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="//", tick_label=K[domain], linewidth=3)
        plt.bar(EditToFitBarPlot(K[domain], 1.25 * width), resDict[domain]['lazy'][index1], width=width, label='Lazy', color='black', edgecolor='black', hatch="...", tick_label=K[domain], linewidth=2)
        plt.xlabel('k1')
        plt.ylabel('nu for {}'.format(domain))
        if i==1:
            plt.legend(bbox_to_anchor=(0.1, 0.9), loc=2, borderaxespad=0.)
        i += 1

    fname = '../../../hiofsm/IJCAI2018/figures/Nu.png'
    fig = plt.gcf()
    fig.set_size_inches(55, 10)

    plt.savefig(fname, bbox_inches='tight')

def PlotNuAcc(resDict):
    index1 = 'nu'
    width = 0.25
    krange = [0, 1, 2, 3, 4]
    for domain in resDict:
        plt.clf()
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:5]
    domain = 'CR'
    plt.bar(EditToFitBarPlot(krange, 0 * width), resDict[domain]['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=krange)
    plt.bar(EditToFitBarPlot(krange, 1 * width), resDict[domain]['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=krange)

    plt.bar(EditToFitBarPlot(krange, 0 * width), resDict['EE']['active'][index1], bottom=resDict['CR']['active'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=krange)
    plt.bar(EditToFitBarPlot(krange, 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=krange)

    plt.bar(EditToFitBarPlot(krange, 0 * width), resDict['SD']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=krange)
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot(krange, 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=krange)
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot(krange, 0 * width), resDict['IP']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1], resDict['SD']['active'][index1]), width=width, color='white', edgecolor='black', hatch="/////", tick_label=krange)
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/////", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot(krange, 1 * width), resDict['IP']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1], resDict['SD']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="*****", tick_label=krange)
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="+++++", tick_label=[0, 1, 2, 3])

    fname = '../../../hiofsm/IJCAI2018/figures/Nu_together.png'
    plt.xlabel('k1')
    plt.ylabel('nu')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def PlotNuToppedSep(resDict):
    index1 = 'nu'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'red'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5

    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['CR'][label1][index1][0:l],
         width=width, edgecolor='black', 
         label='CR', 
         color='red', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['EE'][label1][index1][0:l], 
        width=width, edgecolor='black', 
         label='EE', 
        tick_label=val, color='blue', 
        linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('Speed $\\nu$') # for {}'.format(domain))
    plt.legend(bbox_to_anchor=(0.1, 1.05), 
        loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'NuDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['SD'][label1][index1][0:l], 
        width=width, edgecolor='black', 
        label='SD', tick_label=val,
        color='orange', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['IP'][label1][index1][0:l], 
        width=width, edgecolor='black', 
         label='IP', 
        tick_label=val, color='green', linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('Speed $\\nu$') # for {}'.format(domain))
    plt.legend(bbox_to_anchor=(0.1, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'NuNoDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

def CheckIn(l, e):
    for key in l:
        if e <= key*(1.01) and e >= key*0.99:
            return (True, key)
    return (False, None)

def PlotNuDet(resDict):
    index1 = 'nuDet'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5

    #plt.bar(EditToFitBarPlot(val, 0 * width), resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="/", label='CR', color=color1, linewidth=2)
    #plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['EE'][label1][index1][0:l], width=width, edgecolor='black', hatch="///", label='EE', tick_label=val, color='black', linewidth=2)
    for domain in resDict:
        x = 0
        plt.clf()
        for yy in resDict[domain][label1][index1][0:l]:
            y_final = {}
            for y in yy:
                if CheckIn(y_final, y)[0] == True:
                    k = CheckIn(y_final, y)[1]
                    y_final[k] += 1
                else:
                    y_final[y] = 1

            for key in y_final:
                y_final[key] =  30 * 1.5 ** y_final[key]

            x_val = [x]*len(y_final)
            y_val = list(y_final.keys())
            s_val = list(y_final.values())
            print(x_val)
            print(y_val)
            print(s_val)
            plt.scatter(x_val, y_val, s=s_val)
            x += 1

        plt.xlabel('$b$')
        plt.ylabel('Speed $\\nu$ for {}'.format(domain))
        plt.legend(bbox_to_anchor=(0.1, 1.05), loc=3, ncol=2, borderaxespad=0.)
        #plt.tick_label = val
        #fig = plt.gcf()
        #fig.set_size_inches(40, 10)

        fname = '../../../hiofsm/IJCAI2018/figures/Nu{}points.png'.format(domain)
        plt.savefig(fname, bbox_inches='tight')

    #plt.clf()
    #plt.bar(EditToFitBarPlot(val, 0 * width), resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch=".", label='SD', tick_label=val, color='white', linewidth=2)
    #plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['IP'][label1][index1][0:l], width=width, edgecolor='black', hatch="...", label='IP', tick_label=val, color='black', linewidth=2)

    #plt.xlabel('$k_1$')
    #plt.ylabel('Speed $\\nu$') # for {}'.format(domain))
    #plt.legend(bbox_to_anchor=(0.1, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    #fname = '../../../hiofsm/IJCAI2018/figures/NuNoDeadEnds.png'
    #plt.savefig(fname, bbox_inches='tight')

def normalize(l):
    #m = max(l)
    lret = []
    for i in range(1, len(l)):
        if (l[0] - l[i])*100/l[0]/4 > 0:
            lret.append((l[0] - l[i])*100/l[0])
        else:
            lret.append(0)
    return lret

def PlotCommandTotals(resDict):
    index1 = 'commandTotal'
    width = 0.25

    for domain in resDict:
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:4]
            resDict[domain][mode][index1] = normalize(resDict[domain][mode][index1])

    plt.bar(EditToFitBarPlot([0, 1, 2], 0 * width), resDict['SD']['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2], 1 * width), resDict['SD']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2], 0 * width), resDict['IP']['active'][index1], bottom=resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2], 1 * width), resDict['IP']['lazy'][index1], bottom=resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2], 0 * width), resDict['CR']['active'][index1], bottom=GetSum(resDict['SD']['active'][index1], resDict['IP']['active'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2], 1 * width), resDict['CR']['lazy'][index1], bottom=GetSum(resDict['SD']['lazy'][index1], resDict['IP']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2], 0 * width), resDict['EE']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['IP']['active'][index1], resDict['SD']['active'][index1]), width=width, color='white', edgecolor='black', hatch="/////", tick_label=[ 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/////", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2], 1 * width), resDict['EE']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['IP']['lazy'][index1], resDict['SD']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="*****", tick_label=[1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="+++++", tick_label=[0, 1, 2, 3])

    fname = '../../../hiofsm/IJCAI2018/figures/CommandTotals.png'
    plt.xlabel('k1')
    plt.ylabel('#Commands saved')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')


def PlotRetryCounts(resDict):
    index1 = 'retryCount'
    width = 0.25

    for domain in resDict:
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:4]
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['CR']['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['CR']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['EE']['active'][index1], bottom=resDict['CR']['active'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1], resDict['SD']['active'][index1]), width=width, color='white', edgecolor='black', hatch="/////", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=resDict['SD']['active'][index1], width=width, color='white', edgecolor='black', hatch="/////", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1], resDict['SD']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="*****", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=resDict['SD']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="+++++", tick_label=[0, 1, 2, 3])

    fname = '../../../hiofsm/IJCAI2018/figures/RetryCounts.png'
    plt.xlabel('k1')
    plt.ylabel('Retry ratio')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def PrintToFile(resDict):
    with open("output_with_ordering.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        for domain in resDict:
            header = ['Domain', 'Mode', 'k1', 'Total Counter', 'Total Clock', 'Success Count', 'Total Count', 'Retry Count', 'Commands Total', 'nu'] + list(COMMANDS[domain].keys())
            writer.writerow(header)
            for mode in resDict[domain]:
                for k in K[domain]:
                    row = [domain, mode, k]
                    for data in resDict[domain][mode]:
                        if data != 'commandCounts':
                            row.append(resDict[domain][mode][data][k])
                        else:
                            cmdDict = resDict[domain][mode][data][k]
                            cmdCount = COMMANDS[domain].copy()
                            for cmd in cmdDict:
                                cmdCount[cmd] += cmdDict[cmd]
                            row += list(cmdCount.values())
                    writer.writerow(row)

def PlotSuccessCounts(resDict):
    ii = 1
    for domain in resDict:
        Plot(K[domain], resDict[domain], domain, 'count', ii)
        if ii == 1:
            plt.legend(bbox_to_anchor=(0.0, 1), loc=2, borderaxespad=0.)
        ii += 1
    fig = plt.gcf()
    fig.set_size_inches(40, 10)

    fname = '../../../hiofsm/IJCAI2018/figures/SuccessWithRetryPenalty.png'
    plt.savefig(fname, bbox_inches='tight')

    #for domain in resDict:
    #    fname = '../../../hiofsm/IJCAI2018/figures/ExecutionTime.png'
    #    Plot(K[domain], resDict[domain], domain, 'time', ii)
    #    if ii == 3:
    #        plt.legend(bbox_to_anchor=(0.0, 1), loc=2, borderaxespad=0.)
    #    ii += 1
    #fig = plt.gcf()
    #fig.set_size_inches(30, 10)
    #plt.savefig(fname, bbox_inches='tight')

    #plt.clf()
    #ii = 1

def PlotRetrySideBySide(resDict):
    index1 = 'retryCount'
    label1 = "lazy"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.15
    val = [0, 1, 2, 3, 4]
    l = 5
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="/", label='CR', color=color1, linewidth=1)
    plt.bar(EditToFitBarPlot(val, 1 * width), resDict['EE'][label1][index1][0:l], width=width, edgecolor='black', hatch="*", label='EE', tick_label=val, color='white', linewidth=1)
    plt.bar(EditToFitBarPlot(val, 2 * width), resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch="-", label='SD', tick_label=val, color='white', linewidth=1)
    plt.bar(EditToFitBarPlot(val, 3 * width), resDict['IP'][label1][index1][0:l], width=width, edgecolor='black', hatch="", label='IP', tick_label=val, color='black', linewidth=1)

    plt.xlabel('k1')
    plt.ylabel('Retry Ratio')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)
    fname = '../../../hiofsm/IJCAI2018/figures/RetriesAllDomains.png'
    plt.savefig(fname, bbox_inches='tight')

def PlotSuccessTopped(resDict):
    index1 = 'successCount'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="/", label='CR', color=color1, linewidth=1)
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['EE'][label1][index1][0:l], bottom=resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="///", label='EE', tick_label=val, color='white', linewidth=1)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch=".", label='SD', tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['IP'][label1][index1][0:l], bottom=resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch="...", label='IP', tick_label=val, color='white', linewidth=2)

    plt.xlabel('k1')
    plt.ylabel('success ratio')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = '../../../hiofsm/IJCAI2018/figures/SuccessAllDomains.png'
    plt.savefig(fname, bbox_inches='tight')

def PlotSuccessToppedSep(resDict):
    index1 = 'successCount'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5

    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['CR'][label1][index1][0:l], 
        width=width, 
        edgecolor='black',  
        label='CR', 
        color='red', 
        linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['EE'][label1][index1][0:l], 
        width=width, edgecolor='black',  
        label='EE', tick_label=val, 
        color='blue', linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('Success ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'SuccessDeadEnds_poster.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['SD'][label1][index1][0:l],
        width=width, edgecolor='black', 
        label='SD', tick_label=val, 
        color='orange', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['IP'][label1][index1][0:l], 
        width=width, edgecolor='black', 
        label='IP', tick_label=val, 
        color='green', linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('Success ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), 
        loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'SuccessNoDeadEnds_poster.png'
    plt.savefig(fname, bbox_inches='tight')

def PlotRetryTopped(resDict):
    index1 = 'retryCount'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="/", label='CR', color=color1, linewidth=1)
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['EE'][label1][index1][0:l], bottom=resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="///", label='EE', tick_label=val, color='white', linewidth=1)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch=".", label='SD', tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['IP'][label1][index1][0:l], bottom=resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch="...", label='IP', tick_label=val, color='white', linewidth=2)

    plt.xlabel('k1')
    plt.ylabel('Retry Ratio')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = '../../../hiofsm/IJCAI2018/figures/RetriesAllDomains.png'
    plt.savefig(fname, bbox_inches='tight')

def PlotRetryToppedSep(resDict):
    index1 = 'retryCount'
    label1 = "active"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5
    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['EE'][label1][index1][0:l], 
        width=width, edgecolor='black', 
        label='EE', color='red', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['CR'][label1][index1][0:l], 
        width=width, edgecolor='black', label='CR', 
        tick_label=val, color='blue', linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('retry ratio')
    plt.legend(bbox_to_anchor=(0.6, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'RetriesDeadEnds_poster.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), 
        resDict['SD'][label1][index1][0:l], 
        width=width, edgecolor='black',  
        label='SD', tick_label=val, 
        color='orange', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), 
        resDict['IP'][label1][index1][0:l], 
        width=width, edgecolor='black',  
        label='IP', tick_label=val, color='green', linewidth=2)

    plt.xlabel('Search breadth $b$')
    plt.ylabel('Retry ratio')
    plt.legend(bbox_to_anchor=(0.6, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'RetriesNoDeadEnds_poster.png'
    plt.savefig(fname, bbox_inches='tight')

def PlotRetryInv(resDict):
    index1 = 'rinv'
    label1 = "lazy"
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    val = [0, 1, 2, 3, 4]
    l = 5
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="/", label='CR', color=color1, linewidth=1)
    plt.bar(EditToFitBarPlot(val, 0 * width), resDict['EE'][label1][index1][0:l], bottom=resDict['CR'][label1][index1][0:l], width=width, edgecolor='black', hatch="///", label='EE', tick_label=val, color='white', linewidth=1)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch=".", label='SD', tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), resDict['IP'][label1][index1][0:l], bottom=resDict['SD'][label1][index1][0:l], width=width, edgecolor='black', hatch="...", label='IP', tick_label=val, color='white', linewidth=2)

    plt.xlabel('k1')
    plt.ylabel('sum of 1/#retries')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = '../../../hiofsm/IJCAI2018/figures/RetryInvAllDomains.png'
    plt.savefig(fname, bbox_inches='tight')

def EditToFitBarPlot(b, c):
    a = b[:]
    for ii in range(0, len(a)):
        a[ii] += c
    return a

def GetSum(*l):
    size = len(l[0])
    res = []
    for i in range(0, size):
        res.append(0)
        for item in l:
            res[i] += item[i]
    return res

def PlotSimTimes(resDict):
    index1 = 'simTime'
    width = 0.25

    for domain in resDict:
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:4]
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['CR']['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['CR']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['EE']['active'][index1], bottom=resDict['CR']['active'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[0, 1, 2, 3])

    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1], resDict['SD']['active'][index1]), width=width, color='white', edgecolor='black', hatch="////", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1], resDict['SD']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="++++", tick_label=[0, 1, 2, 3])

    fname = '../../../hiofsm/IJCAI2018/figures/SimulationTimes.png'
    plt.xlabel('k1')
    plt.ylabel('Simulation time')
    plt.legend(bbox_to_anchor=(0.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def PlotRunningTimes(resDict):
    index1 = 'runTime'
    width = 0.25

    for domain in resDict:
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:4]
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['CR']['active'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['CR']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['EE']['active'][index1], bottom=resDict['CR']['active'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[0, 1, 2, 3])

    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['active'][index1], bottom=GetSum(resDict['CR']['active'][index1], resDict['EE']['active'][index1], resDict['SD']['active'][index1]), width=width, color='white', edgecolor='black', hatch="////", tick_label=[0, 1, 2, 3])
    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['IP']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1], resDict['SD']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="++++", tick_label=[0, 1, 2, 3])

    fname = '../../../hiofsm/IJCAI2018/figures/RunningTimes.png'
    plt.xlabel('k1')
    plt.ylabel('Running time')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def Plot(val, res, domain, plotMode, ii):
    plt.subplot(1, 4, ii)
    #if plotMode == 'simtime':
    #   index1 = 'simTime'
    #index2 = 'runTime'
    #fname = '../../../hiofsm/IJCAI2018/figures/simTime_{}.png'.format(domain)
    #ylabel = 'Execution Time in {} (in 1000 Counter Ticks)'.format(domain)
    ylabel = ''
  #  label1 = "Active"# APE-plan"
    #label2 = "Active APE"
   # label3 = "Lazy" # APE-plan"
    #label4 = "Lazy APE"
    #color1 = 'white'
    #color2 = 'black'
    #color3 = 'pink'
    #color4 = 'gray'
    index1 = 'successCount'
    #index2 = 'retryCount'
    #fname = '../../../hiofsm/IJCAI2018/figures/SuccessAndRetry_{}.png'.format(domain)
    #ylabel = 'Success and Retry Counts in {}'.format(domain)
    ylabel = ''
    label1 = "Active"
    #label2 = "Active retry count"
    label3 = "Lazy"
    #label4 = "Lazy retry count"
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