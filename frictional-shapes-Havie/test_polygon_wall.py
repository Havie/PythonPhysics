import pygame
from circle import Circle
from polygon import Polygon
from UniformPolygon import *
from wall import Wall
#import Contact as contact
from Contact import *#
import math

# initialize pygame and open window
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode([width, height])

# set timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# set objects
objects = [] 
wall = Wall( [800,600], [0,300])
my_poly = Polygon(localOffsets=[[-50,-50], [-20, 40], [40,-20]], mass=1, 
                  color=[0,0,255], width=1, normals_length=0)


localOffsets=[[0,0], [100, 0], [100,20], [0,20]]
uniformPoly= UniformPolygon(density=0.1,  localOffsets=localOffsets, pos=[0,0],
                  color=[0,0,255], width=1, normals_length=0)

objects = [wall, my_poly]

# game loop
running = True
while running:
    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    my_poly.setPos(pygame.mouse.get_pos())
    
    # collisions
    overlap = False
    contacts = []

    c = detectContact(my_poly, wall, restitution=0.2)
    if c.isColliding():
        overlap = True

    # DRAW section
    # clear the screen
    if overlap:
        screen.fill([255,255,0])
    else:
        screen.fill([255,255,255])

    # draw objects
    for o in objects:
        o.update(dt)
        o.draw(screen)

    if c.isColliding():
        pos = my_poly.pos
        vel = my_poly.velo
        c.resolve()
        my_poly.draw(screen)
        my_poly.pos = pos
        my_poly.velo = vel
        pygame.draw.circle(screen, [0,0,0], c.contactPoint(), 5)

    # update the display
    pygame.display.update()

    # delay for correct timing
    clock.tick(fps)
