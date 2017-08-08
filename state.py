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

class StateDict():
    def __init__(self, d):
        if hasattr(d, '__iter__'):
            self.lock = {}
            for key in d:
                self.lock[key] = Lock()
        else:
            self.lock = Lock()
        self.dict = d

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value
        if key not in self.lock:
            self.lock[key] = Lock()

    def __iter__(self):
        return self.dict.__iter__()

    def __str__(self):
        return self.dict.__str__()

    def AcquireLock(self, key):
        self.lock[key].acquire()

    def ReleaseLock(self, key):
        self.lock[key].release()