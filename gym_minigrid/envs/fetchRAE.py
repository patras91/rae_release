__author__="sunandita"

from gym_minigrid.roomgrid import RoomGrid, Room
from gym_minigrid.register import register

from ..minigrid import *
from random import choice
from enum import Enum, IntEnum
import math

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __sub__(self, other):
        if self.__class__ is other.__class__:
            return self.value - other.value
        return NotImplemented

class RoomDes(OrderedEnum):
    NOT_A_ROOM = 0
    NO_DOOR = 1
    UNLOCKED = 2
    LOCKED_VAULT = 3
    LOCKED_UNK = 4

    def increment(self):
        return RoomDes(self.value + 1)

class Observability(OrderedEnum):
    FULL = 0
    PARTIAL = 1 # maybe include area here later

    def increment(self):
        return Observability(self.value + 1)


class World(OrderedEnum):
    CLOSED = 0
    OPEN = 1

    def increment(self):
        return World(self.value + 1)

class EnvDes():
    class MAX(IntEnum):
        roomSize = 5

    def __init__(self, roomDescriptor, observability, world, roomSize):
        """
        @param roomDescriptor: the room descriptor array (self.roomDescriptor)
        @param roomSize: the room size (self.roomSize)
        @param observability: the observability (full or partial) (self.observability)

        self.roomDescriptor
        0 = fully closed
        1 = fully open (no wall)
        2 = closed but unlocked door
        3 = closed and locked door, key in vault
        4 = closed and locked door, key in corridor

        self.roomSize
        The size of the rooms and corridors, including the walls.  The smallest room is a room of size 3, with one
            interior cell and two walls.

        self.observability
        True if fully observable, False if partially observable.
        """

        self.roomDescriptor=roomDescriptor
        self.observability=observability
        self.world=world
        self.roomSize=roomSize

        for item in self.roomDescriptor:
            assert(item <= RoomDes.LOCKED_UNK)

        assert self.roomSize >= 3 and self.roomSize <= 5

    def IncrementByOneStep(self, item):
        res = []

        if item == "roomDescriptor":
            for i in range(len(self.roomDescriptor)):
                if self.roomDescriptor[i] < RoomDes.LOCKED_VAULT: # max value
                    l = list(self.roomDescriptor)
                    l[i] = l[i].increment()
                    res.append(
                        EnvDes(roomDescriptor=tuple(l),
                               roomSize=self.roomSize,
                               observability=self.observability,
                               world=self.world)
                    )

        elif item == "roomSize":
            if self.roomSize < self.MAX.roomSize:
                res.append(
                    EnvDes(roomDescriptor=self.roomDescriptor,
                           roomSize=self.roomSize + 1,
                           observability=self.observability,
                           world=self.world)
                )

        elif item == "observability":
            if self.observability < Observability.FULL:
                res.append(
                    EnvDes(rmDesc=self.roomDescriptor,
                           roomSize=self.roomSize,
                           observability=Observability.PARTIAL,
                           world=self.world)
                )

        elif item == "world":
            if self.world < World.CLOSED:
                res.append(
                    EnvDes(rmDesc=self.roomDescriptor,
                           roomSize=self.roomSize,
                           observability=self.observability,
                           world=World.OPEN)
                )

        return res

    def __str__(self):
        """
        Calculate a string representation of the task descriptor object.

        @return: the string representing the task descriptor.
        """
        return 'envD'+ str(self.roomDescriptor) + '-' + \
               str(self.world) + '-' + \
               str(self.roomSize) + '-' + \
               str(self.observability)

    def __repr__(self):
        return self.__str__()


    def __eq__(self, v):
        return self.roomDescriptor == v.roomDescriptor and \
               self.world == v.world and \
               self.roomSize == v.roomSize and \
               self.observability == v.observability

    def __hash__(self):
        return hash(self.roomDescriptor) + \
               hash(self.world) + \
               hash(self.roomSize) + \
               hash(self.observability)

    def distance(self, t):
        d = 0
        for item in zip(self.roomDescriptor, t.roomDescriptor):
            d += abs(item[0] - item[1])

        d += abs(self.roomSize - t.roomSize) + abs(self.observability - t.observability) + abs(self.world - t.world)

        return d

    def ToDict(self):
        d = {}
        for key in self.__dict__:
            if key == 'roomDescriptor':
                d[key] = [str(item) for item in self.roomDescriptor]
            else:
                d[key] = str(self.__dict__[key])

        return d

class TaskDes():
    def __init__(self, envD, seed):
        """
        Initialization method for the TaskDescriptor() class.

        This method stores each input the corresponding object properties.


        self.seed
            Integer seed value for the random environment creation.


        @param seed: the seed (self.seed)
        """
        self.envDescriptor=envD
        self.seed=seed

    def distance(self, tD):
        return self.envDescriptor.distance(tD.envDescriptor) # need to return the goal distance as well

    def IncrementByOneStep(self):
        res = []
        for item in self.envDescriptor.__dict__:
            neighbors = self.envDescriptor.IncrementByOneStep(item)
            for envD in neighbors:
                res.append((TaskDes(envD=envD, seed=self.seed), 1))
        return res

    def __str__(self):
        """
        Calculate a string representation of the task descriptor object.

        @return: the string representing the task descriptor.
        """
        return 'taskD-'+ str(self.envDescriptor)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, v):
        return self.envDescriptor == v.envDescriptor

    def ToDict(self):
        return {
            'seed': self.seed,
            'envD': self.envDescriptor.ToDict()
        }

def RecreateEnvDes(d):
    return EnvDes(roomDescriptor=tuple(getattr(RoomDes, item.split('.')[1]) for item in d['roomDescriptor']),
                  observability=getattr(Observability,d['observability'].split(".")[1]),
                  world=getattr(World,d['world'].split(".")[1]),
                  roomSize=int(d['roomSize']))

def RecreateTaskDes(d):
    return TaskDes(RecreateEnvDes(d['envD']), d['seed'])


class RoomGBLA(Room):
    def __init__(
            self,
            top,
            size,
            roomType
    ):
        super().__init__(top, size)
        self.type = roomType

    def __repr__(self):
        return "room: " + str(self.top) + str(self.size) + str(self.type)

    def HasSouthDoor(self):
        return self.door_pos[1]

    def HasNorthDoor(self):
        return self.door_pos[3]

class fetchRAE(RoomGrid):
    """
    The door-key-object domain for Goal biased learning Agenda
    """

    def __init__(
            self,
            taskD
    ):
        """
        This is the initialization function for the RoomDescriptor object.

        @param taskD:
        """
        #for item in taskD.envDescriptor.roomDescriptor:
        #    print(item)
        self.roomGridMap = self.createGridMap(taskD.envDescriptor.roomDescriptor)
        self.roomSize = taskD.envDescriptor.roomSize
        self.obj_type = "ball"

        super().__init__(
            room_size=taskD.envDescriptor.roomSize,
            num_rows=self.roomGridMap.shape[0],
            num_cols=self.roomGridMap.shape[1],
            max_steps=30*taskD.envDescriptor.roomSize, # may need to be updated
        )

        del(taskD)
        #print("initialized GBLA Key Corridor Domain with shape ", self.roomGridMap.shape[0], self.roomGridMap.shape[1])

    def createGridMap(self, roomDes):
        num_rooms = 0
        for item in roomDes:
            if not item == RoomDes.NOT_A_ROOM:
                num_rooms += 1

        k = math.floor(math.sqrt(num_rooms))
        if k*k >= num_rooms:
            num_rows = k
            num_cols = k
        elif (k+1)*k >= num_rooms:
            num_rows = k
            num_cols = k + 1
        else:
            num_rows = k+1
            num_cols = k+1

        grid = [[RoomDes.NOT_A_ROOM]*(num_cols+2)] # the corridor above

        for i in range(num_rows):
            row = [RoomDes.NOT_A_ROOM] # empty space in coln 0
            for j in range(num_cols):
                index = num_cols*i + j
                if index < len(roomDes):
                    row.append(roomDes[index])
                else:
                    row.append(RoomDes.NOT_A_ROOM)
            row.append(RoomDes.NOT_A_ROOM) # empty space in last coln (num_rooms - 1)
            grid.append(row)

        grid.append([RoomDes.NOT_A_ROOM]*(num_cols+2)) # the corridor below

        grid = [[RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM],
                [RoomDes.NOT_A_ROOM, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NOT_A_ROOM],
                [RoomDes.NOT_A_ROOM, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NOT_A_ROOM],
                [RoomDes.NOT_A_ROOM, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NO_DOOR, RoomDes.NOT_A_ROOM],
                [RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM, RoomDes.NOT_A_ROOM],
                ]
        return np.array(grid)

    def set_goal_info(self, goal_function, goal_value, goal):
        gd = GetGoalDescriptor(self)
        self.goalDescriptor = gd
        #       self.goalDescriptor = None
        return None

    def reset(self):
        return super().reset()

    def add_passage(self, room):
        l = self.roomLoc[room]
        if room in ['delivery', 0, 1, 2]:
            self.remove_wall(l[1], l[0], 3)
        else:
            self.remove_wall(l[1], l[0], 1)

    def parseDescriptor(self, roomDesc):

        # roomType = (roomDesc & int('0000000011', 2))
        # doorNorth = (roomDesc & int('0000001100', 2))/4
        # doorEast = (roomDesc & int('0000110000', 2))/16
        # doorSouth = (roomDesc & int('0011000000', 2))/64
        # doorWest = (roomDesc & int('1100000000', 2))/256

        roomType = roomDesc
        doorEast = False
        doorWest = roomDesc

        if not roomType == RoomDes.NOT_A_ROOM:
            doorNorth = roomDesc
            doorSouth = roomDesc
        else:
            doorNorth = False
            doorSouth = False

        return roomType, (doorNorth, doorEast, doorSouth, doorWest)

    def descriptorDistance(self, roomDesc1, roomDesc2):
        rType1, rDoors1 = self.parseDescriptor(roomDesc1)
        rType2, rDoors2 = self.parseDescriptor(roomDesc2)
        return None

    def _gen_grid(self, width, height):
        # Create the grid

        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        self.room_grid = []

        # For each row of rooms
        for j in range(0, self.num_rows):
            row = []

            # For each column of rooms
            for i in range(0, self.num_cols):
                roomType, doorLocs = self.parseDescriptor(self.roomGridMap[j, i])

                room = RoomGBLA(
                    (i * (self.room_size-1), j * (self.room_size-1)),
                    (self.room_size, self.room_size),
                    roomType
                )
                row.append(room)

                # Generate the walls for this room
                if not roomType  == RoomDes.NOT_A_ROOM:
                    self.grid.wall_rect(*room.top, *room.size)

            self.room_grid.append(row)



        # Place the agent in the middle
        self.place_agent(0, 2)

        self.agent_dir = 0

        # For each row of rooms
        for j in range(0, self.num_rows):
            # For each column of rooms
            for i in range(0, self.num_cols):
                roomType, (doorNorth, doorEast, doorSouth, doorWest) = \
                    self.parseDescriptor(self.roomGridMap[j, i])
                room = self.room_grid[j][i]

                x_l, y_l = (room.top[0] + 1, room.top[1] + 1)
                x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)

                # Door positions, order is right, down, left, up
                if doorEast:
                    #room.neighbors[0] = self.room_grid[j][i+1]
                    room.door_pos[0] = (x_m, self._rand_int(y_l, y_m))
                    self.set_door(doorEast, (i, j), room.door_pos[0])

                if doorSouth:
                    room.neighbors[1] = self.room_grid[j+1][i]
                    if not room.neighbors[1].HasNorthDoor():
                        room.door_pos[1] = (self._rand_int(x_l, x_m), y_m)
                        self.set_door(doorSouth, (i, j), room.door_pos[1])

                if doorWest:
                    #room.neighbors[2] = self.room_grid[j][i-1]
                    room.door_pos[2] = (x_l-1, self._rand_int(y_l, y_m))
                    self.set_door(doorWest, (i,j), room.door_pos[2])

                if doorNorth:
                    room.neighbors[3] = self.room_grid[j-1][i]
                    if not room.neighbors[3].HasSouthDoor():
                        room.door_pos[3] = (self._rand_int(x_l, x_m), y_l-1)
                        self.set_door(doorNorth, (i,j), room.door_pos[3])


        # Add two object in the rooms
        self.obj = []
        n_obj = 1
        if self.roomSize >= 3:
            while(len(self.obj) < n_obj):
                locs = [(r,c) for r in range(self.num_rows) for c in range(self.num_cols)
                        if not self.room_grid[r][c].type == RoomDes.NOT_A_ROOM]
                loc = choice(locs)
                try:
                    obj, _ = self.add_object(loc[1], loc[0], kind=self.obj_type)
                    self.obj.append(obj)
                    # until we integrate with a planner, we need this info for the sub-goals in the goal descriptors
                    self.object_room = self.get_room(loc[1], loc[0])
                except:
                    pass

        else:
            obj, _ = self.add_object(self._rand_int(1, self.num_cols), 0, kind=self.obj_type, color='green')
            self.obj.append(obj)

        self.gap_pos = np.array((
            self._rand_int(2, width - 5),
            self._rand_int(1, height - 5),
        ))

        # Place the obstacle wall
        self.grid.vert_wall(self.gap_pos[0], 1, height - 7, Lava)


        # Make sure all rooms are accessible
        self.mission = ""  # "pick up the %s %s" % (obj.color, obj.type)

    def set_door(self, doorType, roomLoc, doorLoc):
        if doorType == RoomDes.NOT_A_ROOM:
            pass
        elif doorType == RoomDes.NO_DOOR:
            self.grid.set(*doorLoc, None)
        elif doorType == RoomDes.UNLOCKED:
            self.add_door(*roomLoc, locked=False)
        elif doorType == RoomDes.LOCKED_UNK or doorType == RoomDes.LOCKED_VAULT:
            doorColor = self._rand_color()
            self.add_door(*roomLoc, locked=True, color=doorColor)

            n = 0
            while n<100:
                n+=1
                locs = [(r, c) for r in range(self.num_rows) for c in range(self.num_cols)
                        if self.room_grid[r][c].type == RoomDes.NOT_A_ROOM]
                loc = choice(locs)
                try:
                    self.add_object(*loc, 'key', doorColor)
                    n+=100
                except:
                    pass

    def step(self, action):
        return super().step(action)

register(
    id='MiniGrid-fetchRAE-v0',
    entry_point='gym_minigrid.envs:fetchRAE'

)

