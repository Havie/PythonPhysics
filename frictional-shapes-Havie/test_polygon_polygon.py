import pygame
from circle import Circle
from polygon import Polygon
from Contact import *
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

offsets =[
        [0,0],
        [200,0],
        [200,100],
        [100,200],
        [0,100]
    ]

polygons = []
polygons.append(Polygon(localOffsets=list(reversed(offsets)), mass=1, pos=[300,200], color=[255,0,0], normals_length=50))
my_poly = Polygon(localOffsets=[[-50,-50], [-20, 40], [40,-20]], mass=math.inf, 
                  color=[0,0,255], width=1, normals_length=20)

objects = polygons + [my_poly]

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

    for p in polygons:
        c = detectContact(my_poly, p, restitution=0)
        if c.isColliding():
            overlap = True
            if pygame.mouse.get_pressed()[0]: # left mouse button down
                c.resolve()

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

    # update the display
    pygame.display.update()

    # delay for correct timing
    clock.tick(fps)
