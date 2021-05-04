from Forces import *
import pygame
import math

class AirDrag(SingleForce):
    def __init__(self, windVel=[0, 0], **kwargs):
        self.windVel = pygame.math.Vector2(windVel)
        super().__init__(**kwargs)
    

    def force(self, obj):
        V = 4/3 * math.pi * obj.radius**3
        A = 4 * math.pi * obj.radius**2
        massdensity = obj.mass / V #row
        c_d = 0.5
        v = obj.velo - self.windVel
        v_mag= pygame.math.Vector2.magnitude(v)
        # 0.5 *c_d * row * A * mag(v) * v
        return (-0.5 *c_d* massdensity *A* v_mag * v  )

    def apply(self):
        #print("apply Gravity");
        for o in self.objects:
            o.addForce(self.force(o))
            
    def setWindVelo(self, v):
        self.windVel += v
    def GetWindVelo(self):
        return self.windVel