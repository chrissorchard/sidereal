"""A test script, that checks that basic physics is working, by
"throwing" a ball, represented by the default turtle display.

"""
import time
import math
import random
import argparse

parser = argparse.ArgumentParser(description="Throw some turtle shaped balls.")
parser.add_argument('--fixed-seed','-S',action='store_true',default=False)
parser.add_argument('--ball-number','-n',type=int,default=3)
args = parser.parse_args()

if args.fixed_seed:
    random.seed(100)


import sidereal.physics.odeobjects as odeobjects
import sidereal.turtles as turtles

d = turtles.Display()
d.autocoord_display = {'coord'}
d.tilt_type = 'rotation'
world = odeobjects.PhysicsWorld()

world.setGravity((0,0,0))

ball = odeobjects.PhysicsObject(world,1000)
ball.body.setPosition((0,0,0))
d.add(ball)

target = odeobjects.PhysicsObject(world)
target.body.setPosition((20,20,0))
d.add(target)

def vector_sub(first,second):
    return tuple([b - a for a,b in zip(first,second)])

def unit_vector(v):
    length = vector_length(v)
    return tuple([x / length for x in v])

def vector_length(v):
    squared = [x**2 for x in v]
    sum = math.fsum(squared)
    return math.sqrt(sum)

def fire_engine():
    ball.body.addRelForce((100,0,0))
    print "Forward!"

def fire_left_thruster():
    ball.body.addRelTorque((0,0,1))
    print "Left!"

def fire_right_thruster():
    ball.body.addRelTorque((0,0,-1))
    print "Right!"

def quit():
    global running
    running = False

d.screen.onkey(fire_engine,"Up")
d.screen.onkey(fire_left_thruster,"Left")
d.screen.onkey(fire_right_thruster,"Right")
d.screen.onkey(quit,"q")
d.screen.listen()

timetaken = 0
running = True
while running:
    timestamp = time.time()
    d.draw()
    elapsed = time.time() - timestamp
    timetaken += elapsed
    world.step(elapsed)
print timetaken
