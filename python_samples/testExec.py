__author__ = 'patras'


def testExec():
    global mod
    #mod = __import__("problem1_STE")
    mod = __import__("problem1_STE", globals())
    print(mod.DURATION_TIME)

def test1():
    global mod
    print(mod.DURATION_TIME)