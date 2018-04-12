__author__ = 'patras'

from threading import Lock

class State():
    def __init__(self):
        pass

    def __setattr__(self, key, value):
        self.__dict__[key] = StateDict(value)

    def __str__(self):
        res = ""
        if self != False:
            for (key, val) in vars(self).items():
                res = res + '   state.' + key + ' =' + val.__str__() + '\n'
        else:
            res = 'False'
        return res

    def copy(self):
        s = State()
        for (key, val) in vars(self).items():
            s.__setattr__(key, val.GetVal())
            s.__dict__[key].DeleteLocks() # because locks are not picklable
        return s

    def restore(self, s):
        for (key, val) in vars(s).items():
            self.__setattr__(key, val.GetVal())
        return s

    def ReleaseLocks(self):
        for key in self.__dict__:
            self.__dict__[key].ReleaseAllLocks()

class StateDict():
    def __init__(self, d):
        if hasattr(d, '__iter__'):
            self.lock = {}
            for key in d:
                self.lock[key] = Lock()
        else:
            self.lock = Lock()
        self.dict = d

    def GetVal(self):
        return dict(self.dict)

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value
        if key not in self.lock:
            self.lock[key] = Lock()

    def __cmp__(self, other):
        return cmp(self.dict, other)

    def __iter__(self):
        return self.dict.__iter__()

    def __str__(self):
        return self.dict.__str__()

    def AcquireLock(self, *key):
        if len(key) == 1:
            self.lock[key[0]].acquire()
        else:
            self.lock[key].acquire()

    def ReleaseLock(self, *key):
        if len(key) == 1:
            self.lock[key[0]].release()
        else:
            self.lock[key].release()

    def ReleaseAllLocks(self):
        if hasattr(self.lock, '__iter__'):
            for key in self.lock:
                if self.lock[key].locked():
                    self.lock[key].release()
        else:
            if self.lock.locked():
                self.lock.release()

    def DeleteLocks(self):
        self.lock = None