import pygame
from circle import Circle
from pygame.math import Vector2 # VECTOR CLASS 
from Gravity import *

screenBounds=[600,600]
screen = pygame.display.set_mode(screenBounds);

fps = 60
deltaTime= 1/fps
clock = pygame.time.Clock()


objects=[]
forces = []
forces.append(Gravity(objects=objects, acc = [0,980]))


RUNNING=True;

#"wat is air density per cubic meter"

while RUNNING :


    for o in objects:
        o.clear_force();

    for f in forces:
        f.apply();
