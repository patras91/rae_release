__author__ = 'patras'
#!/usr/bin/python

from Tkinter import *
from Queue import Queue

globalQueue = Queue()

class GUI():
    def __init__(self):
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
    globalQueue.put(t)

def start():
    g = GUI()