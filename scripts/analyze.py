__author__ = 'patras'
import matplotlib.pyplot as plt

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

def Populate(res, domain, simmode):
    f_rae = open("test_noLA_output.txt", "r")
    PopulateHelper(res, domain, f_rae)
    f_rae.close()
    for k in range(1, 4):
        if simmode == 'normal':
            fname = 'test_normalLA{}_output.txt'.format(k)
        elif simmode == 'lazy':
            fname = 'test_lazyLA{}_output.txt'.format(k)
        elif simmode == 'concurrent':
            fname = 'test_concLA{}_output.txt'.format(k)
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
        resDict[key] = {'normal': {}, 'lazy': {}, 'concurrent': {}}
        for kk in resDict[key]:
            resDict[key][kk] = {'time': [], 'count': []}
            Populate(resDict[key][kk], key, kk)
        Plot([0, 1, 2, 3], resDict[key], key, 'time')
        Plot([0, 1, 2, 3], resDict[key], key, 'count')

def Plot(val, res, domain, mode):
    plt.clf()
    plt.plot(val, res['normal'][mode], label='normal')
    plt.plot(val, res['lazy'][mode], label='lazy')
    plt.plot(val, res['concurrent'][mode], label='concurrent')
    if mode == 'count':
        fname = 'SuccessPercentage_{}.png'.format(domain)
        plt.ylabel('Success Percentage')
    else:
        fname = 'ExecutionTime_{}.png'.format(domain)
        plt.ylabel('Execution Time')
    plt.xlabel('K')
    plt.legend(bbox_to_anchor=(1.05, 0.9), loc=2, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

if __name__=="__main__":
    GeneratePlots()