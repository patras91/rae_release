__author__ = 'patras'
#!/usr/bin/python

from tkinter import *
from queue import Queue
import turtle
from shared import GLOBALS

globalQueue = Queue()

class GUIParams():
    def __init__(self, domain, showOutputs):
        self.domain = domain
        self.showOutputs = showOutputs

class GUI():
    def __init__(self):
        if gParams.showOutputs == "on":
            self.root = Tk()
            self.text = Text(self.root)
            self.text.pack()
            self.root.after(1, self.simulate)
            self.root.mainloop()

    def simulate(self):
        if gParams.domain == 'IP_':
            if globalQueue.empty() == False:
                t = globalQueue.get()
                tdraw.simulate(t)
        else:
            if globalQueue.empty() == False:
                t = globalQueue.get()
                t1 = ' '.join(map(str, t))
                self.text.insert(END, t1)
            self.root.after(1, self.simulate)

def Simulate(*t):
    if (GLOBALS.GetPlanningMode() == True): #or gParams.showOutputs == "off"):
        return
    elif gParams.domain in ["AIRS_dev", "AIRS", "Mobipick"] and gParams.showOutputs == "on":
        print(t)
    globalQueue.put(t)

def start(domain, showOutputs):
    global gParams
    gParams = GUIParams(domain, showOutputs)
    GUI()
