from particle import Particle
from pygame import *
from pygame.math import Vector2

def intvec(v):
    if v != None:
        return Vector2(round(v.x), round(v.y))

class Circle(Particle):
    def __init__(self, radius=10, color=[255, 255, 255], width=0, **kwargs):
        self.radius = radius
        self.color = color
        self.width = width
        super().__init__(**kwargs) # send rest of arguments to super Particle class

    def draw(self, screen):
        draw.circle(screen, self.color, self.pos, self.radius, self.width)