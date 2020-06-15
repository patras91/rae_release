__author__ = 'patras'
import GLOBALS

class Utility():
    def __init__(self, val):
        if GLOBALS.GetUtility() == 'min':
            if val == 'Success':
                self.value = 0
            elif val == 'Failure':
                self.value = float("inf")
            else:
                self.value = val    
        elif GLOBALS.GetUtility() == 'efficiency':
            if val == 'Failure':
                self.value = 0
            elif val == 'Success':
                self.value = float("inf")
            else:
                self.value = val
        elif GLOBALS.GetUtility() == "successRatio":
            if val == "Failure":
                self.value = 0
            elif val == "Success":
                self.value = 1
            else:
                if val != "UNK":
                    assert(val >= 0 and val <= 1)
                self.value = val

    def __gt__(self, other): 
        if self.value == 'UNK':
            return False
        if self.value > other.value: 
            return True
        else: 
            return False

    def __ge__(self, other): 
        if self.value >= other.value: 
            return True
        else: 
            return False

    def __lt__(self, other):
        if self.value < other.value: 
            return True
        else: 
            return False

    def __le__(self, other):
        if self.value <= other.value: 
            return True
        else: 
            return False

    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if GLOBALS.GetUtility() == "efficiency":
            e1 = self.value
            e2 = other.value
            if e1 == float("inf"):
                res = e2
            elif e2 == float("inf"):
                res = e1
            elif e1 == 0 and e2 == 0:
                res = 0
            else:
                res = e1 * e2 / (e1 + e2)
            return Utility(res)
        elif GLOBALS.GetUtility() == "successRatio":
            sr1 = self.value
            sr2 = other.value
            return Utility(sr1 * sr2)

    def SetValue(self, val):
        self.value = val

    def GetValue(self):
        return self.value

if __name__=="__main__":

    a = Utility(1)
    b = Utility(5)

    print(a>b)
    print(a>=b)
    print(a<b)
    print(a<=b)
    print(a==b)

