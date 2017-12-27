
"""File: draw.py -- Sunandita Patra, Dec 22, 2017
You'll need to call turtle.Screen() before calling any of the functions
"""

import turtle

robot_colors = {}

def get_color(r):
    colors = ['orange', 'red', 'pink', 'blue']
    if r in robot_colors:
        return robot_colors[r]
    else:
        robot_colors[r] = colors[len(robot_colors)]
        return robot_colors[r]

def write_text(t, x, y, colour, type='normal'):
    turtle.penup()
    turtle.color(colour)
    turtle.goto(x, y)
    turtle.write(t, font=('Arial', 20, type))

def draw_one_machine(p, loc, map, colour, x_pos, y_pos, type='normal'):
    square = map[loc]
    if x_pos == True:
        x = min(min(x1, x2) for [(x1, y1), (x2, y2)] in square) + 1
    else:
        x = max(max(x1, x2) for [(x1, y1), (x2, y2)] in square) - 4
    if y_pos == True:
        y = min(min(y1, y2) for [(x1, y1), (x2, y2)] in square) + 1
    else:
        y = max(max(y1, y2) for [(x1, y1), (x2, y2)] in square) - 2
    write_text(p, x, y, colour, type)

def draw_machines_helper(pm, locations, map, colour, x_pos, y_pos):
    for p in pm:
        draw_one_machine(p, locations[p], map, colour, x_pos, y_pos)

    turtle.color('black')

def draw_machines(machines, locations, map):
    for key in machines:
        draw_machines_helper(machines[key], locations, map, machine_color[key], x_pos[key], y_pos[key])

def draw_buffers(buff, map):
    draw_machines_helper(buff.keys(), buff, map, 'black', True, False)

def draw_problem(grid=True, title='', rv=None):
    clear()
    walls = []
    global rVars
    rVars = rv
    for key in rv.MAP:
        walls += rv.MAP[key]

    set_scale(walls, grid=False)
    draw_lines(walls)
    draw_buffers(rv.BUFFERS, rv.MAP)
    draw_machines(rv.MACHINES, rv.MACHINE_LOCATION, rv.MAP)
    #if s0:
    #	draw_dot(s0,color='blue',size=8)
    #if finish_line:
#		draw_lines([finish_line], color='brown', width=2, dots=0)
    if title:
        draw_title(title, lowerleft, upperright)

def draw_title(title,ll,ur):
    """Write title at the top of the drawing."""
    turtle.penup()
    size = upperright - lowerleft
    turtle.goto(ur/2.5,ur+size*.01)
    turtle.write(title,font=('Arial',20,'normal'))

def draw_path(path):
    """draw a path"""
    x0 = False
    for (x1,y1) in path:
        if x0:
            draw_lines([((x0,y0),(x1,y1))], color='red', width=2, dots=8)
        (x0,y0) = (x1,y1)

# for each node status, What width, color, and dot size to use
status_options = {
    'add':            (1, 'green', 0),  # generated nodes being put into frontier
    'discard':        (1, 'orange', 0), # generated nodes being discarded
    'expand':         (2, 'blue', 5),   # node expanded
    'frontier_prune': (2, 'purple', 0), # nodes pruned from frontier
    'explored_prune': (2, 'purple', 0), # nodes pruned from explored
    'solution':       (3, 'red', 8),    # nodes in the solution path
    }


def draw_edges(edges,status):
    """
    Draw the line for an individual edge. Use status to tell what kind of
    edge: add, discard, expand, re-exand, prune, retract, solution
    """
    (width, color, dots) = status_options[status]
    draw_lines(edges, width=width, color=color, dots=dots)


################## Primitives #######################
# These get called by the above functions.
# You probably won't need to call any of them directly.

def clear():
    """Clear the graphics window."""
    turtle.clear()

def set_scale(lines,grid=True):
    """This sets the coordinate scale for a square window whose dimensions are large
    enough to accommodate the lines that you need to draw. If grid=True, it will draw
    grid lines.
    """
    global lowerleft
    global upperright
    lowerleft = min([min(x0,y0,x1,y1) for ((x0,y0),(x1,y1)) in lines])
    upperright = max([max(x0,y0,x1,y1) for ((x0,y0),(x1,y1)) in lines])
    size = upperright - lowerleft
    margin = size*.1
    turtle.setworldcoordinates(lowerleft - margin, lowerleft - margin, \
        upperright + margin, upperright + margin)
    turtle.pen(speed=0,shown=False)			# 0 means use maximum possible speed
    if grid: draw_grid(lowerleft,upperright)

def draw_lines(lines, color='black', width=3, dots=0):
    """draw every line in lines"""
    turtle.pen(speed=0,shown=False)
    turtle.color(color)
    turtle.width(width)
    for line in lines:
        (p0, p1) = list(line)
        if p0 != p1:
            turtle.penup()
            turtle.goto(p0)
            turtle.pendown()
            turtle.goto(p1)
        if dots>0: draw_dot(p1,color=color,size=dots)


def draw_dot(loc,color='red',size=8):
    """put a dot at location loc"""
    turtle.penup()
    turtle.goto(loc)
    turtle.dot(size,color)

def draw_finish(loc,color='red',size=8):
    """put a dot at location loc"""
    (x,y) = loc
    turtle.penup()
    turtle.goto((x,y))
    turtle.dot(size,color)

def draw_grid(ll,ur):
    size = ur - ll
    for gridsize in [1, 2, 5, 10, 20, 50, 100 ,200, 500]:
        lines = (ur-ll)/gridsize
        if lines <= 11: break
    turtle.color('darkgray')
    turtle.width(1)

    x = ll
    while x <= ur:
        if x == ur or int(x/gridsize)*gridsize == x:
            turtle.penup()
            turtle.goto(x, ll-.35*gridsize)
            turtle.write(str(x),align="center",font=("Arial",16,"normal"))
            turtle.goto(x,ll)
            turtle.pendown()
            turtle.goto(x,ur)
        x += 1

    y = ll
    while y <= ur:
        if y == ur or int(y/gridsize)*gridsize == y:
            turtle.penup()
            turtle.goto(ll-.1*gridsize, y - .06*gridsize)
            turtle.write(str(y),align="right",font=("Arial",16,"normal"))
            turtle.goto(ll,y)
            turtle.pendown()
            turtle.goto(ur,y)
        y += 1

def get_center(loc):
    global rVars
    square = rVars.MAP[loc]
    x = [(x1 + x2)/2 for [(x1, y1), (x2, y2)] in square]
    y = [(y1 + y2)/2 for [(x1, y1), (x2, y2)] in square]
    return (sum(x)/len(x), sum(y)/len(y))

def draw_line(loc1, loc2, color):
    p1 = get_center(loc1)
    p2 = get_center(loc2)

    turtle.pen(speed=1,shown=False)
    turtle.color(color)
    turtle.width(3)

    turtle.penup()
    turtle.goto(p1)
    turtle.pendown()
    turtle.pen(shown=True)
    turtle.goto(p2)

def simulate_move(args):
    robot = args[0]
    loc1 = args[1]
    loc2 = args[2]
    draw_line(loc1, loc2, get_color(robot))

x_pos = {
    'paint': False,
    'assemble': False,
    'pack': True,
    'wrap': True
}

y_pos = {
    'paint': False,
    'assemble': True,
    'pack': False,
    'wrap': True
}

machine_color = {
    'paint': 'red',
    'assemble': 'blue',
    'wrap': 'pink',
    'pack': 'orange'
}

def get_machine_type(m):
    if m in rVars.MACHINES['paint']:
        return 'paint'
    elif m in rVars.MACHINES['assemble']:
        return 'assemble'
    elif m in rVars.MACHINES['wrap']:
        return 'wrap'
    else:
        return 'pack'

def simulate_busy(m):
    loc = rVars.MACHINE_LOCATION[m]
    key = get_machine_type(m)
    draw_one_machine(m, loc, rVars.MAP, machine_color[key], x_pos[key], y_pos[key], 'bold')

def simulate(t):
    if t[0] == 'move':
        simulate_move(t[1:])
    elif t[0] == 'busy':
        simulate_busy(t[1])