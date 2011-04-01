"""A test script, that checks that basic physics is working, by
"throwing" a ball, represented by the default turtle display.

"""
import time
import random
import argparse

parser = argparse.ArgumentParser(description="Throw some turtle shaped balls.")
parser.add_argument('--fixed-seed','-S',action='store_true',default=False)
parser.add_argument('--ball-number','-n',type=int,default=3)
args = parser.parse_args()

if args.fixed_seed:
    random.seed(100)


import sidereal.physics as odeobjects
import sidereal.turtles as turtles

d = turtles.Display()
d.autocoord_display = {'coord'}
world = odeobjects.PhysicsWorld()

world.setGravity((0,-9.81,0))
for i in range(args.ball_number):
    ball = odeobjects.PhysicsObject(world)
    ball.body.setPosition((random.randint(-100,100),random.randint(0,100),0))
    ball.body.setLinearVel((random.randint(-30,50),random.randint(20,40),0))
    d.add(ball)


timetaken = 0
while True:
    timestamp = time.time()
    d.draw()
    elapsed = time.time() - timestamp
    timetaken += elapsed
    world.step(elapsed)
    discard = []
    for ball in d:
        if ball.coord[1] <= 0:
            discard.append(ball)

    for ball in discard:
        d.discard(ball)

    if len(d) == 0:
        break

