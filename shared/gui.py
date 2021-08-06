__author__ = 'patras'
#!/usr/bin/python

from tkinter import *
from queue import Queue
import turtle
from shared import GLOBALS

import time
import numpy as np
# import gym
# import gym_minigrid
#from gym_minigrid.wrappers import *
#from gym_minigrid.window import Window
#from gym_minigrid.envs.keycorridor_GBLA import RoomDes, Observability, World, EnvDes, TaskDes

globalQueue = Queue()

class GUIParams():
    def __init__(self, domain, showOutputs):
        self.domain = domain
        self.showOutputs = showOutputs

class GUI():
    def __init__(self):
        if gParams.showOutputs == "on":
            # if gParams.domain == "fetch":
            #     view = MinigridSimulator()
            # else:
            if True:
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
        #elif gParams.domain == "fetch":
        #    pass
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
    # elif gParams.domain == "fetch" and gParams.showOutputs == "on":
    #     pass
    #elif gParams.showOutputs == "on":
    else:
        globalQueue.put(t)

def start(domain, showOutputs):
    global gParams
    gParams = GUIParams(domain, showOutputs)
    GUI()


class MinigridSimulator():
    def __init__(self):
        self.envD = EnvDes(roomDescriptor=(
            RoomDes.NO_DOOR,
            RoomDes.LOCKED_VAULT,
            RoomDes.NO_DOOR,
            RoomDes.LOCKED_VAULT,
            RoomDes.NO_DOOR,
            RoomDes.LOCKED_VAULT,
            RoomDes.NO_DOOR,
            RoomDes.LOCKED_VAULT
        ),
            observability=Observability.FULL,
            world=World.CLOSED,
            roomSize=4, # can't be less than 3
        )

        self.envD = EnvDes(roomDescriptor=(
            RoomDes.NO_DOOR,
            RoomDes.NOT_A_ROOM,
            RoomDes.NOT_A_ROOM,
            RoomDes.NOT_A_ROOM,
            RoomDes.NOT_A_ROOM,
            RoomDes.NOT_A_ROOM,
        ),
            observability=Observability.FULL,
            world=World.CLOSED,
            roomSize=3, # can't be less than 3
        )

        self.tD = TaskDes(envD=envD, seed=np.random.randint(0,100))

        self.env = gym.make("MiniGrid-KeyCorridorGBLA-v0", taskD=tD)

        self.window = Window('gym_minigrid - MiniGrid-KeyCorridorGBLA-v0')

        def key_handler(self, event):
            print('pressed', event.key)

            if event.key == 'escape':
                window.close()
                return

            if event.key == 'backspace':
                reset()
                return

            if event.key == 'left':
                self.step(self.env.actions.left)
                return
            if event.key == 'right':
                self.step(self.env.actions.right)
                return
            if event.key == 'up':
                self.step(self.env.actions.forward)
                return

            # Spacebar
            if event.key == ' ':
                self.step(self.env.actions.toggle)
                return
            if event.key == '1':
                self.step(self.env.actions.pickup)
                return
            if event.key == 'd':
                self.step(self.env.actions.drop)
                return

            if event.key == 'enter':
                self.step(self.env.actions.done)
                return

        self.window.reg_key_handler(key_handler)

        self.reset()

        # Blocking event loop
        self.window.show(block=True)

    def redraw(self, img):
        img = self.env.render('rgb_array', tile_size=32)

        self.window.show_img(img)

    def reset(self):
        obs = self.env.reset()

        if hasattr(env, 'mission'):
            print('Mission: %s' % env.mission)
            self.window.set_caption(env.mission)

        self.redraw(obs)

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        print('step=%s, reward=%.2f' % (self.env.step_count, reward))

        if done:
            print('done!')
            self.reset()
        else:
            self.redraw(obs)




