__author__ = 'patras'

class Utility():
    def __init__(self, opt):
        assert(opt == 'min' or opt == 'max')
        self.opt = opt
        if opt == 'min':
            self.value = 0
        elif opt == 'max':
            self.value = float("inf")

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

    def SetVal(self, val):
        self.value = val

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

