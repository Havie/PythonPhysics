from particle import Particle
import pygame
from pygame.math import Vector2

class Wall(Particle):
    def __init__(self, point1=[0,0], point2=[0,0], color=[0,0,0]):
        self.color = color
        self.point1 = Vector2(point1)
        self.point2 = Vector2(point2)
        self.update_pos_normal()
        super().__init__(pos=self.pos)

    def update_pos_normal(self):
        self.pos = (self.point1 + self.point2)/2
        dif = self.point1 - self.point2
        normal = dif.rotate(90)
        self.normal = normal.normalize()

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.point1, self.point2, 2)