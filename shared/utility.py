__author__ = 'patras'
import GLOBALS

class Utility():
    def __init__(self, val):
        if GLOBALS.GetOpt() == 'min':
            if val == 'Success':
                self.value = 0
            elif val == 'Failure':
                self.value = float("inf")
            else:
                self.value = val    
        else:
            if val == 'Failure':
                self.value = 0
            elif val == 'Success':
                self.value = float("inf")
            else:
                self.value = val

    def __gt__(self, other): 
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
        return Utility(self.value + other.value)

    def SetValue(self, val):
        self.value = val

    def GetValue(self):
        return self.value

if __name__=="__main__":
    a = Utility('min')
    b = Utility('min')
    a.SetVal(1)
    b.SetVal(5)

    print(a>b)
    print(a>=b)
    print(a<b)
    print(a<=b)
    print(a==b)

