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

def PopulateHelper(res, domain, f_rae):
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
    if simmode == "noplan":
        f_rae_name = "outputs/{}/APE.txt".format(domain)
        f_rae = open(f_rae_name, "r")
        print(f_rae_name)
        PopulateHelper(res, domain, f_rae)
        f_rae.close()
    else:
        fname = 'outputs/{}/plan.txt'.format(domain)
        fptr = open(fname)
        print(fname)
        PopulateHelper(res, domain, open(fname))
        fptr.close()

def GeneratePlots():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {}
    }

    for domain in resDict:
        resDict[domain] = {'noplan': {}, 'plan': {}} #, 'concurrent': {}}
        for APEmode in resDict[domain]:
            resDict[domain][APEmode] = {'counter': [], 'clock': [], 'successCount': [], 'totalCount': [],  'retryCount': [], 'commandTotal': [], 'nu': [], 'rinv': [], 'commandCounts': [], 'nuDet':[]}
            Populate(resDict[domain][APEmode], domain, APEmode)

    #PrintToFile(resDict)

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    #PlotSuccessToppedSep(resDict)
    #RetryTopped(resDict)
    Nu(resDict)

def CheckIn(l, e):
    for key in l:
        if e <= key*(1.01) and e >= key*0.99:
            return (True, key)
    return (False, None)


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

def RetryTopped(resDict):
    plt.clf()
    index1 = 'retryCount'
    label1 = "noplan"
    label2 = 'plan'
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    tickLabel = ['no planning', 'APE-plan']
    val = [0, 1]

    plt.bar(EditToFitBarPlot(val, 0 * width),\
        [resDict['CR'][label1][index1][0], resDict['CR'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="/", \
        label='CR', color=color1, linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['EE'][label1][index1][0], resDict['EE'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="///", \
        label='EE', tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('Retry Ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/RetryDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), \
        [resDict['SD'][label1][index1][0], resDict['SD'][label2][index1][0]], width=width, \
        edgecolor='black', hatch=".", label='SD', \
        tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['IP'][label1][index1][0], resDict['IP'][label2][index1][0]], width=width,\
        edgecolor='black', hatch="...", label='IP',\
        tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('Retry ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/RetryNoDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

def Nu(resDict):
    plt.clf()
    index1 = 'nu'
    label1 = "noplan"
    label2 = 'plan'
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    tickLabel = ['no planning', 'APE-plan']
    val = [0, 1]

    plt.bar(EditToFitBarPlot(val, 0 * width),\
        [resDict['CR'][label1][index1][0], resDict['CR'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="/", \
        label='CR', color=color1, linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['EE'][label1][index1][0], resDict['EE'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="///", \
        label='EE', tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('Speed to Success')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/SpeedDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), \
        [resDict['SD'][label1][index1][0], resDict['SD'][label2][index1][0]], width=width, \
        edgecolor='black', hatch=".", label='SD', \
        tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['IP'][label1][index1][0], resDict['IP'][label2][index1][0]], width=width,\
        edgecolor='black', hatch="...", label='IP',\
        tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('Speed to Success')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/SpeedNoDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')


def PlotSuccessToppedSep(resDict):
    plt.clf()
    index1 = 'successCount'
    label1 = "noplan"
    label2 = 'plan'
    #label3 = "Lazy"
    color1 = 'white'

    width = 0.25
    tickLabel = ['no planning', 'APE-plan']
    val = [0, 1]

    plt.bar(EditToFitBarPlot(val, 0 * width),\
        [resDict['CR'][label1][index1][0], resDict['CR'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="/", \
        label='CR', color=color1, linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['EE'][label1][index1][0], resDict['EE'][label2][index1][0]], \
        width=width, edgecolor='black', hatch="///", \
        label='EE', tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('success ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/SuccessDeadEnds.png'
    plt.savefig(fname, bbox_inches='tight')

    plt.clf()
    plt.bar(EditToFitBarPlot(val, 0 * width), \
        [resDict['SD'][label1][index1][0], resDict['SD'][label2][index1][0]], width=width, \
        edgecolor='black', hatch=".", label='SD', \
        tick_label=val, color='white', linewidth=2)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), \
        [resDict['IP'][label1][index1][0], resDict['IP'][label2][index1][0]], width=width,\
        edgecolor='black', hatch="...", label='IP',\
        tick_label=tickLabel, color='black', linewidth=2)

    plt.xlabel('Mode')
    plt.ylabel('success ratio')
    plt.legend(bbox_to_anchor=(0.0, 1.05), loc=3, ncol=2, borderaxespad=0.)
    #fig = plt.gcf()
    #fig.set_size_inches(40, 10)

    fname = 'figures/SuccessNoDeadEnds.png'
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