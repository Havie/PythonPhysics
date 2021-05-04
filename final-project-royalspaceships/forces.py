import math
from pygame.math import Vector2
import pygame
import itertools

G = 18000

def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

class SingleForce:
    def __init__(self, objects=[]):
        self.objects = objects

    def force(self, obj):
        return Vector2(0)
    
    def apply(self):
        for obj in self.objects:
            f = self.force(obj)
            obj.add_force(f)

class Gravity(SingleForce):
    def __init__(self, acc=[0,0], **kwargs):
        self.acc = Vector2(acc)
        super().__init__(**kwargs)

    def force(self, obj):
        return obj.mass * self.acc

class AirDrag(SingleForce):
    def __init__(self, wind_vel=[0,0], **kwargs):
        self.wind_vel = Vector2(wind_vel)
        super().__init__(**kwargs)
    
    def force(self, obj):
        V = 4/3 * math.pi * obj.radius**3
        A = 4 * math.pi * obj.radius**2
        massdensity = obj.mass / V
        Cd = 0.5
        v = obj.vel - self.wind_vel
        return -(1/2) * massdensity * v * v.magnitude() * Cd * A
    
    def set_wind_vel(self, v):
        self.wind_vel = Vector2(v)

class Friction(SingleForce):
    def __init__(self, coefficient=1, g=1, **kwargs):
        self.coefficient = coefficient
        self.g = g
        super().__init__(**kwargs)
    
    def force(self, obj):
        if obj.vel.magnitude() > 0:
            vhat = obj.vel / obj.vel.magnitude()
            return -self.coefficient * obj.mass * self.g * vhat
        else:
            return Vector2(0, 0)

class PairForce:
    def __init__(self, objects=[]):
        self.objects = objects

    def force(self, a, b):
        return Vector2(0)

    def apply(self):
        for a, b in itertools.combinations(self.objects, 2): # generates all pairs
            force = self.force(a, b)
            a.add_force(force)
            b.add_force(-force)

class Gravitation(PairForce):
    def __init__(self, G=0, **kwargs):
        self.G = G
        super().__init__(**kwargs)
    
    def force(self, a, b):
        global G
        r = a.pos - b.pos
        return -G * a.mass * b.mass / r.magnitude()**3 * r

class BondForce:
    def __init__(self, objects=[]):
        self.objects = objects
    
    def force(self, a, b):
        return Vector2(0, 0)
    
    def apply(self):
        for a in self.objects:
            for b in self.objects:
                if a != b:
                    force = self.force(a, b)
                    a.add_force(force)
                    b.add_force(-force)

class Spring(BondForce):
    def __init__(self, k=20, l=100, b=2, **kwargs):
        self.k = k
        self.l = l
        self.b = b
        super().__init__(**kwargs)

    def force(self, a, b):
        v = a.vel - b.vel
        r = a.pos - b.pos
        return (-self.k * (pygame.math.Vector2.magnitude(r) - self.l) - (self.b*v*r.normalize())) * r.normalize()

    def apply(self):
        for x in range(len(self.objects)-1):
            a = self.objects[x]
            b = self.objects[x+1]
            force = self.force(a, b)
            a.add_force(force)
            b.add_force(-force)

class Repulsive(BondForce):
    def __init__(self, k=0, **kwargs):
        self.k = k
        super().__init__(**kwargs)

    def force(self, a, b):
        r = a.pos - b.pos
        retVec = Vector2(0, 0)
        if (b.radius + a.radius) - pygame.math.Vector2.magnitude(r) > 0:
            retVec = self.k * (b.radius + a.radius - pygame.math.Vector2.magnitude(r)) * r.normalize()
        return retVec