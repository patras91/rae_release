__author__ = 'patras'
import matplotlib.pyplot as plt

K = {
    'SD': [0, 1, 2, 3],
    'EE': [0, 1, 2, 3, 4],
    'IP': [0, 1, 2],
    'CR': [0, 1, 2, 3]
}

mult = {
    'SD': 15,
    'EE': 15,
    'IP': 75,
    'CR': 10
}

penalty = {
    'SD': 0.2,
    'EE': 0.1,
    'CR': 0.0,
    'IP': 0.1
}
def PopulateHelper(res, domain, f_rae):
    line = f_rae.readline()
    succCount = 0
    totalCount = 0
    retryCount = 0
    simTime = 0
    runTime = 0
    while(line != ''):
        parts = line.split(' ')
        if parts[0] == 'Time':
            for i in range(0, 3):
                counts = f_rae.readline()
                print(counts)
                parts2 = counts.split(' ')
                succCount += int(parts2[0])
                totalCount += int(parts2[1])
                retryCount += int(parts2[2])
                simTime += int(parts2[3])
                runTime += int(parts2[4])
        line = f_rae.readline()

    #res['successCount'].append(succCount * 100 / totalCount)
    sucNorm = succCount - penalty[domain] * retryCount
    if sucNorm < 0:
        sucNorm = 0
    res['successCount'].append(sucNorm)
    res['retryCount'].append(retryCount)
    res['simTime'].append(simTime/1000)

    if len(res['runTime']) >= 1:
        succ0 = res['successCount'][0] + penalty[domain] * res['retryCount'][0]
        res['runTime'].append(runTime * succ0/succCount / 1000)
    else:
        res['runTime'].append(runTime / 1000)

def Populate(res, domain, simmode):
    for k in K[domain]:
        if k == 0:
            if domain == 'IP' or domain == 'CR':
                f_rae_name = "outputs/{}/noLA/RAE.txt".format(domain)
            else:
                f_rae_name = "output_with_costs/{}/noLA/RAE.txt".format(domain)
            f_rae = open(f_rae_name, "r")
            PopulateHelper(res, domain, f_rae)
            f_rae.close()
        else:
            if simmode == 'normal':
                if domain == 'IP':
                    fname = 'outputs/{}/normal/K{}.txt'.format(domain, k)
                else:
                    fname = 'output_with_costs/{}/active/K{}.txt'.format(domain, k)
            elif simmode == 'lazy':
                if domain == 'IP':
                    fname = 'outputs/{}/lazy/K{}.txt'.format(domain, k)
                else:
                    fname = 'output_with_costs/{}/lazy/K{}.txt'.format(domain, k)
            elif simmode == 'concurrent':
                fname = 'outputs/{}/conc/K{}.txt'.format(domain, k)
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
        resDict[domain] = {'normal': {}, 'lazy': {}} #, 'concurrent': {}}
        for APEmode in resDict[domain]:
            resDict[domain][APEmode] = {'simTime': [], 'runTime': [], 'successCount': [], 'retryCount': []}
            Populate(resDict[domain][APEmode], domain, APEmode)

    resDict['IP']['normal']['simTime'].append(0)
    resDict['IP']['normal']['runTime'].append(0)
    resDict['IP']['lazy']['simTime'].append(0)
    resDict['IP']['lazy']['runTime'].append(0)
    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 24}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})

    #PlotSimTimes(resDict)

    plt.clf()
    PlotSuccessCounts(resDict)

    #plt.clf()
    #PlotRunningTimes(resDict)

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


def EditToFitBarPlot(b, c):
    a = b[:]
    for ii in range(0, len(a)):
        a[ii] += c
    return a

def GetSum(*l):
    res = [0, 0, 0, 0]
    for i in range(0, 4):
        for item in l:
            res[i] += item[i]
    return res

def PlotSimTimes(resDict):
    index1 = 'simTime'
    width = 0.25

    for domain in resDict:
        for mode in resDict[domain]:
            resDict[domain][mode][index1] = resDict[domain][mode][index1][0:4]
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['CR']['normal'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['CR']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['EE']['normal'][index1], bottom=resDict['CR']['normal'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['normal'][index1], bottom=GetSum(resDict['CR']['normal'][index1], resDict['EE']['normal'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[0, 1, 2, 3])

    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['normal'][index1], bottom=GetSum(resDict['CR']['normal'][index1], resDict['EE']['normal'][index1], resDict['SD']['normal'][index1]), width=width, color='white', edgecolor='black', hatch="////", tick_label=[0, 1, 2, 3])
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
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['CR']['normal'][index1], width=width, label='Active', color='white', edgecolor='black', hatch="/", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['CR']['lazy'][index1], width=width, label='Lazy', color='white', edgecolor='black', hatch="*", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['EE']['normal'][index1], bottom=resDict['CR']['normal'][index1], width=width, color='white', edgecolor='black', hatch="//", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['EE']['lazy'][index1], bottom=resDict['CR']['lazy'][index1], width=width, color='white', edgecolor='black', hatch="**", tick_label=[0, 1, 2, 3])

    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['SD']['normal'][index1], bottom=GetSum(resDict['CR']['normal'][index1], resDict['EE']['normal'][index1]), width=width, color='white', edgecolor='black', hatch="///", tick_label=[0, 1, 2, 3])
    plt.bar(EditToFitBarPlot([0, 1, 2, 3], 1 * width), resDict['SD']['lazy'][index1], bottom=GetSum(resDict['CR']['lazy'][index1], resDict['EE']['lazy'][index1]), width=width, color='white', edgecolor='black', hatch="***", tick_label=[0, 1, 2, 3])

    #plt.bar(EditToFitBarPlot([0, 1, 2, 3], 0 * width), resDict['IP']['normal'][index1], bottom=GetSum(resDict['CR']['normal'][index1], resDict['EE']['normal'][index1], resDict['SD']['normal'][index1]), width=width, color='white', edgecolor='black', hatch="////", tick_label=[0, 1, 2, 3])
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
    plt.bar(EditToFitBarPlot(val, 0 * width), res['normal'][index1], width=width, edgecolor='black', hatch="/", label=label1, color=color1, linewidth=3)
    plt.bar(EditToFitBarPlot(val, 1.25 * width), res['lazy'][index1], width=width, edgecolor='black', hatch="***", label=label3, tick_label=val, color='white', linewidth=3)
    #plt.bar(Edit(val, -0.1), res['concurrent'][mode], align='edge', width=-0.2, label='concurrent') # for aligning the right edge

    #plt.ylabel(ylabel)
    plt.xlabel('k1 in {}'.format(domain))
    #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #plt.savefig(fname, bbox_inches='tight')

if __name__=="__main__":
    GeneratePlots()