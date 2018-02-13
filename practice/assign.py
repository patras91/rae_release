__author__ = 'patras'
from threading import Lock

class State():
    def __init__(self):
        pass

    def __setattr__(self, key, value):
        self.__dict__[key] = StateDict(value)
        '''self.locks[key] = {}
        for subkey in value:
            self.locks[key][subkey] = RLock()
        '''

    def assign(self, preCond, assignments):
        self.AcquireLocks(preCond + assignments)
        if self.Eval(preCond) == True:
            self.MakeAssignments(assignments)
        self.ReleaseLocks(preCond + assignments)

    def AcquireLocks(self, vars):
        for varName, subkey, val in vars:
            print('acquire: ', varName, subkey, val, '\n')
            self.__dict__[varName].lock[subkey].acquire()

    def ReleaseLocks(self, vars):
        for varName, subkey, val in vars:
            print('release: ', varName, subkey, val, '\n')
            self.__dict__[varName].lock[subkey].release()

    def MakeAssignments(self, assignments):
        for varName, subkey, val in assignments:
            print('assign: ', varName, subkey, val, '\n')
            self.__dict__[varName].dict[subkey] = val
        pass

    def Eval(self, conds):
        res = True
        for varName, subkey, val in conds:
            if self.__dict__[varName].dict[subkey] != val:
                res = False
        return res

    def __str__(self):
        res = ""
        if self != False:
            for (key, val) in vars(self).items():
                res = res + '   state.' + key + ' =' + val.__str__() + '\n'
        else:
            res = 'False'
        return res

class StateDict():
    def __init__(self, d):
        self.lock = {}
        for key in d:
            self.lock[key] = Lock()
        self.dict = d

    '''def __setitem__(self, key, value):
        self.dict[key] = value

    def __setitem__(self, key, value):
        if hasattr(value, '__iter__'):
            newVal, preCond = value
            self.AcquireLocks(preCond)
            if self.Eval(preCond) == True:
                self.SetValue(key, value)
            self.ReleaseLocks()
        else:
            self.SetValue(key, value)

    def SetValue(self, key, value):
        dict.__setitem__(self, key, value)'''

    def AcquireLock(self):
        self.lock.acquire()

    def ReleaseLock(self):
        self.lock.release()

    def __str__(self):
        return self.dict.__str__()
    '''def Eval(self, conds):
        return True'''

def assign():
    s = State()
    s.var1 = {'a': 1, 'b': 2}
    s.var2 = {'c': 3, 'd': 4}

    #s.var1['a'] = 5, [(s.var2['c'], 3)]
    #s.var2['c'] = 2
    #print(s.var1)
    #print(s.var2)

    s.assign(preCond=[('var1', 'a', 1)], assignments=[('var2','d', 5)])
    print s
    s.assign(preCond=[('var1', 'b', 7)], assignments=[('var1','a', 1)])
    print s

def paramTest(a, b):
    print a


    #def assign(self, preCond, assignments):
    #    self.AcquireLocks(preCond + assignments)
    #    if self.Eval(preCond) == True:
    #        self.MakeAssignments(assignments)
    #    self.ReleaseLocks(preCond + assignments)

    #def AcquireLocks(self, vars):
    #    for varName, subkey, val in vars:
    #        self.__dict__[varName].lock[subkey].acquire()

    #def ReleaseLocks(self, vars):
    #    for varName, subkey, val in vars:
    #        self.__dict__[varName].lock[subkey].release()

    #def MakeAssignments(self, assignments):
    #    for varName, subkey, val in assignments:
    #        self.__dict__[varName].dict[subkey] = val
    #    pass

    #def Eval(self, conds):
    #    res = True
    #    for varName, subkey, val in conds:
    #        if self.__dict__[varName].dict[subkey] != val:
    #            res = False
    #    return res
