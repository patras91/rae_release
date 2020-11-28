__author__ = 'patras'
#!/usr/bin/python

from tkinter import *
from queue import Queue
import turtle
import GLOBALS

globalQueue = Queue()

class GUI():
    def __init__(self, domain, showOutputs):
        self.domain = domain
        self.showOutputs = showOutputs
        if showOutputs == "on":
            self.root = Tk()
            self.text = Text(self.root)
            self.text.pack()
            self.root.after(1, self.simulate)
            self.root.mainloop()

    def simulate(self):
        if self.domain == 'IP_':
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
    global g
    if (GLOBALS.GetPlanningMode() == True or g.showOutputs == 'off'):
        return
    elif GLOBALS.GetDomain() == "AIRS" and g.showOutputs == "on":
        print(t)
    globalQueue.put(t)

def start(domain, showOutputs):
    if showOutputs == 'on':
        global g
        g = GUI(domain, showOutputs)
        print("GUI is initialized ...")