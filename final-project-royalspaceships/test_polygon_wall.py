import pygame
import numpy as np
from circle import Circle
from polygon import Polygon
from wall import Wall
from contact import contact
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
wall = Wall([0,300], [800,600])
my_poly = Polygon(offsets=[[-50,-50], [-20, 40], [40,-20]], mass=1, 
                  color=[0,0,255], width=1, normals_length=0)

objects = [wall, my_poly]

# game loop
running = True
while running:
    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    my_poly.set_pos(pygame.mouse.get_pos())
    
    # collisions
    overlap = False
    contacts = []

    c = contact(my_poly, wall, restitution=0)
    if bool(c):
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

    if bool(c):
        pos = my_poly.pos
        vel = my_poly.vel
        c.resolve()
        my_poly.draw(screen)
        my_poly.pos = pos
        my_poly.vel = vel
        pygame.draw.circle(screen, [0,0,0], c.contact_point(), 5)

    # update the display
    pygame.display.update()

    # delay for correct timing
    clock.tick(fps)
