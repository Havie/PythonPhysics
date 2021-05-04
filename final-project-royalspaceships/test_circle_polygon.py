import pygame
from pygame.math import Vector2
from circle import Circle
from polygon import Polygon
import contact

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
polygons.append(Polygon(offsets=list(reversed(offsets)), pos=[300,200], color=[255,0,0], avel=1, normals_length=50))
circle = Circle(radius=100, mass=1, color=[0,0,255], width=1)

objects = polygons + [circle]

# game loop
running = True
while running:
    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    circle.set_pos(pygame.mouse.get_pos())
    #circle.pos = np.array(pygame.mouse.get_pos(), dtype=float)

    # collisions
    overlap = False
    contacts = []

    for p in polygons:
        c = contact.circle_polygon(circle, p)
        if c.overlap > 0:
            overlap = True
            contacts.append(c)

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

    for c in contacts:
        pygame.draw.circle(screen, [0,0,0], Vector2(circle.pos + c.overlap * c.normal), circle.radius, 1)

    # update the display
    pygame.display.update()

    # delay for correct timing
    clock.tick(fps)
