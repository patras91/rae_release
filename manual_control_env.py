#!/usr/bin/env python3
__author__="sunandita"
import time
import argparse
import numpy as np
import gym
import gym_minigrid
from gym_minigrid.wrappers import *
from gym_minigrid.window import Window
from gym_minigrid.envs.fetchRAE import RoomDes, Observability, World, EnvDes, TaskDes

def redraw(img):
    if not args.agent_view:
        img = env.render('rgb_array', tile_size=args.tile_size)

    window.show_img(img)

def reset():
    if args.seed != -1:
        env.seed(args.seed)

    obs = env.reset()

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)

def step(action):
    obs, reward, done, info = env.step(action)
    print('step=%s, reward=%.2f' % (env.step_count, reward))

    if done:
        print('done!')
        reset()
    else:
        redraw(obs)

def key_handler(event):
    print('pressed', event.key)

    if event.key == 'escape':
        window.close()
        return

    if event.key == 'backspace':
        reset()
        return

    if event.key == 'left':
        step(env.actions.left)
        return
    if event.key == 'right':
        step(env.actions.right)
        return
    if event.key == 'up':
        step(env.actions.forward)
        return

    # Spacebar
    if event.key == ' ':
        step(env.actions.toggle)
        return
    if event.key == '1':
        step(env.actions.pickup)
        return
    if event.key == 'd':
        step(env.actions.drop)
        return

    if event.key == 'enter':
        step(env.actions.done)
        return

    if event.key == '2':
        step(env.actions.addEmergency)
        return

    if event.key == 't':
        step(env.actions.newBall)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--env",
    help="gym environment to load",
    default='MiniGrid-fetchRAE-v0'
)
parser.add_argument(
    "--seed",
    type=int,
    help="random seed to generate the environment with",
    default=-1
)
parser.add_argument(
    "--tile_size",
    type=int,
    help="size at which to render tiles",
    default=32
)
parser.add_argument(
    '--agent_view',
    default=False,
    help="draw the agent sees (partially observable view)",
    action='store_true'
)

args = parser.parse_args()

envD = EnvDes(roomDescriptor=(
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

envD = EnvDes(roomDescriptor=(
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

tD = TaskDes(envD=envD, seed=np.random.randint(0,100))

env = gym.make(args.env, taskD=tD)

#gd = gym_minigrid.envs.goaldescriptor.GetGoalDescriptor(env)

#g = gd.refinement[2].refinement[1]#.refinement[1]
# searchKey goal = [0][0][0]
# pickupKey goal = [0][0][1]
# findDoor goal = [0][1][0]
# passDoor goal = [0][1][1]
# pickupObj goal = [1]
# enterRoom goal = [2][0]
# findRoom goal = [2][1]

#env = GoalRL.GoalEnvWrapper(env,
#               goal_id=g.goalId, goal_function=g.achieved,
#               goal_value=g.goalValue, goal_reward=1,
#               failure_function=None)

if args.agent_view:
    env = RGBImgPartialObsWrapper(env)
    env = ImgObsWrapper(env)

window = Window('gym_minigrid - ' + args.env)
window.reg_key_handler(key_handler)

reset()

#print("setting goal des")
#tD.goalDescriptor = GetGoalDescriptor(env)

# Blocking event loop
window.show(block=True)
