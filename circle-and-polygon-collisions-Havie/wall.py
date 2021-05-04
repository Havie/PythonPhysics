import pygame
from particle import *


def intVec(v):
    return [int(v.x), int(v.y)]

class Wall(Particle):
    def __init__(self, point1=[0,0], point2=[0,0], color=[0,0,0], **kwargs):
        self.color=color;
        self.point1= pygame.math.Vector2(point1[0],point1[1])
        self.point2= pygame.math.Vector2(point2[0],point2[1])
        self.UpdatePosAndNormal()
        super().__init__(pos= self.pos)
        

    def UpdatePosAndNormal(self): 
        self.pos= (self.point1 + self.point2)/2; #midpoint between us
        normal =  (self.point2-self.point1).rotate(90)
        self.normal = normal.normalize();

    def draw(self, screen):
        pygame.draw.line(screen, self.color, intVec(self.point1), intVec(self.point2))

