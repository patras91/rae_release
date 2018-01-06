__author__ = 'patras'
import matplotlib.pyplot as plt

K = {
    'SD': [0, 1, 2, 3],
    'EE': [0, 1, 2, 3],
    'IP': [0, 1, 2],
    'CR': [0, 1, 2, 3]
}

mult = {
    'SD': 15,
    'EE': 15,
    'IP': 75,
    'CR': 10
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
    res['simTime'].append(simTime/1000)
    res['runTime'].append(runTime * mult[domain]/1000)
    #res['successCount'].append(succCount * 100 / totalCount)
    res['successCount'].append(succCount)
    res['retryCount'].append(retryCount)

def Populate(res, domain, simmode):
    for k in K[domain]:
        if k == 0:
            f_rae_name = "outputs/{}/noLA/RAE.txt".format(domain)
            f_rae = open(f_rae_name, "r")
            PopulateHelper(res, domain, f_rae)
            f_rae.close()
        else:
            if simmode == 'normal':
                fname = 'outputs/{}/normal/K{}.txt'.format(domain, k)
            elif simmode == 'lazy':
                fname = 'outputs/{}/lazy/K{}.txt'.format(domain, k)
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

    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'bold',
        'size'   : 32}
    plt.rc('font', **font)
    #plt.rcParams.update({'font.size': 22})
    ii = 1
    for domain in resDict:
        #fname = '../../../hiofsm/IJCAI2018/figures/ExecutionTime.png'
        Plot(K[domain], resDict[domain], domain, 'time', ii)
        if ii == 3:
            plt.legend(bbox_to_anchor=(0.0, 1), loc=2, borderaxespad=0.)
        ii += 1
    #fig = plt.gcf()
    #fig.set_size_inches(30, 10)
    #plt.savefig(fname, bbox_inches='tight')

    #plt.clf()
    ii = 1
    for domain in resDict:
        #fname = '../../../hiofsm/IJCAI2018/figures/SuccessAndRetry.png'
        Plot(K[domain], resDict[domain], domain, 'count', 4 + ii)
        if ii == 1:
            plt.legend(bbox_to_anchor=(0.20, 1), loc=2, borderaxespad=0.)
        ii += 1
    fig = plt.gcf()
    fig.set_size_inches(50, 20)

    fname = '../../../hiofsm/IJCAI2018/figures/allTogether.png'
    plt.savefig(fname, bbox_inches='tight')

def EditToFitBarPlot(b, c):
    a = b[:]
    for ii in range(0, len(a)):
        a[ii] += c
    return a

def Plot(val, res, domain, plotMode, ii):
    #plt.clf()
    plt.subplot(2, 4, ii)
    if plotMode == 'time':
        index1 = 'simTime'
        index2 = 'runTime'
        fname = '../../../hiofsm/IJCAI2018/figures/ExecutionTime_{}.png'.format(domain)
        #ylabel = 'Execution Time in {} (in 1000 Counter Ticks)'.format(domain)
        ylabel = ''
        label1 = "Active APE-S"
        label2 = "Active APE"
        label3 = "Lazy APE-S"
        label4 = "Lazy APE"
        color1 = 'purple'
        color2 = 'black'
        color3 = 'pink'
        color4 = 'gray'
    else:
        index1 = 'successCount'
        index2 = 'retryCount'
        fname = '../../../hiofsm/IJCAI2018/figures/SuccessAndRetry_{}.png'.format(domain)
        #ylabel = 'Success and Retry Counts in {}'.format(domain)
        ylabel = ''
        label1 = "Active success count"
        label2 = "Active retry count"
        label3 = "Lazy success count"
        label4 = "Lazy retry count"
        color1 = 'green'
        color2 = 'red'
        color3 = 'blue'
        color4 = 'orange'

    width = 0.15
    plt.bar(EditToFitBarPlot(val, 0 * width), res['normal'][index1], width=width, label=label1, color=color1)
    plt.bar(EditToFitBarPlot(val, 1 * width), res['normal'][index2], width=width, label=label2, color=color2)
    plt.bar(EditToFitBarPlot(val, 2 * width), res['lazy'][index1], width=width, label=label3, tick_label=val, color=color3)
    plt.bar(EditToFitBarPlot(val, 3 * width), res['lazy'][index2], width=width, label=label4, color=color4)
    #plt.bar(Edit(val, -0.1), res['concurrent'][mode], align='edge', width=-0.2, label='concurrent') # for aligning the right edge

    plt.ylabel(ylabel)
    plt.xlabel('k1 in {}'.format(domain))
    #plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    #plt.savefig(fname, bbox_inches='tight')

if __name__=="__main__":
    GeneratePlots()