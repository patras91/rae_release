__author__ = 'patras'
import matplotlib.pyplot as plt
from numpy import array

def PopulateHelper(res, domain, f_rae):
    line = f_rae.readline()
    succCount = 0
    totalCount = 0
    while(line != ''):
        parts = line.split(' ')
        if parts[0] == 'Time':
            if parts[3] == domain:
                for i in range(0, 9):
                    counts = f_rae.readline()
                    parts2 = counts.split(' ')
                    succCount += int(parts2[0])
                    totalCount += int(parts2[1])
                res['count'].append(succCount * 100 / totalCount)
                line = f_rae.readline()
                runTime = float(line.split(' ')[5])
                if line.split(' ')[6] == 'msec':
                    runTime = runTime / 1000
                res['time'].append(runTime)
                break
        line = f_rae.readline()
    if domain == 'CR':
        print(succCount, totalCount)

def Populate(res, domain, simmode):
    f_rae_name = "outputs/{}/noLA/RAE.txt".format(domain)
    f_rae = open(f_rae_name, "r")
    PopulateHelper(res, domain, f_rae)
    f_rae.close()
    for k in range(1, 4):
        if simmode == 'normal':
            fname = 'outputs/{}/normal/K{}.txt'.format(domain, k)
        elif simmode == 'lazy':
            fname = 'outputs/{}/lazy/K{}.txt'.format(domain, k)
        elif simmode == 'concurrent':
            fname = 'outputs/{}/conc/K{}.txt'.format(domain, k)
        fptr = open(fname)
        PopulateHelper(res, domain, open(fname))
        fptr.close()

def GeneratePlots():
    resDict = {
        'SD': {},
        'EE': {},
        'IP': {},
        'CR': {}
    }
    for key in resDict:
        resDict[key] = {'normal': {}, 'lazy': {}} #, 'concurrent': {}}
        for kk in resDict[key]:
            resDict[key][kk] = {'time': [], 'count': []}
            Populate(resDict[key][kk], key, kk)
        Plot([0, 1, 2, 3], resDict[key], key, 'time')
        Plot([0, 1, 2, 3], resDict[key], key, 'count')

def Edit(b, c):
    a = b[:]
    for ii in range(0, len(a)):
        a[ii] += c
    return a

def Plot(val, res, domain, mode):
    plt.clf()
    plt.bar(Edit(val, 0.1), res['normal'][mode], align='edge', width=0.2, label='normal')
    plt.bar(val, res['lazy'][mode], align='center', width=0.2, label='lazy', tick_label=[0,1,2,3])
    #plt.bar(Edit(val, -0.1), res['concurrent'][mode], align='edge', width=-0.2, label='concurrent')
    if mode == 'count':
        fname = 'figures/SuccessPercentage_{}.png'.format(domain)
        plt.ylabel('Success Percentage')
    else:
        fname = 'figures/ExecutionTime_{}.png'.format(domain)
        plt.ylabel('Execution Time')
    plt.xlabel('K')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

if __name__=="__main__":
    GeneratePlots()