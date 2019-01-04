__author__ = 'patras'
#!/usr/bin/python

from tkinter import *
from queue import Queue
import globals

globalQueue = Queue()

class GUI():
    def __init__(self, domain, rv):
        self.domain = domain
        self.root = Tk()
        self.text = Text(self.root)
        self.text.pack()
        self.root.after(1, self.simulate)
        self.root.mainloop()

    def simulate(self):
        if globalQueue.empty() == False:
            t = globalQueue.get()
            t1 = ' '.join(map(str, t))
            self.text.insert(END, t1)
        self.root.after(1, self.simulate)

def Simulate(*t):
    if (globals.GetPlanningMode() == True or globals.GetShowOutputs() == 'off'):
        return
    globalQueue.put(t)

def start(domain, rv):
    if (globals.GetShowOutputs() == 'on'):
        global g
        g = GUI(domain, rv)