import math
from pygame.math import Vector2

class Particle:
    # constructor
    def __init__(self, pos=[0,0], vel=[0,0], mass=math.inf, angle=0, avel=0, momi=math.inf, torque=0):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.mass = mass
        self.force = Vector2(0, 0)
        self.angle = angle
        self.avel = avel
        self.momi = momi
        self.torque = torque
        self.cosangle = 0
        self.sinangle = 0

    # do physics
    def update(self, dt):
        # update velocity, assuming constant force
        self.vel += self.force / self.mass * dt
        # update postion, assuming constant velocity
        self.pos += self.vel * dt

        self.avel += self.torque/self.momi * dt
        self.angle += self.avel * dt
        self.update_rotation()
    
    def update_rotation(self):
        self.cosangle = math.cos(self.angle)
        self.sinangle = math.sin(self.angle)

    def rotated(self, v):
        return Vector2(self.cosangle * v.x - self.sinangle * v.y, self.sinangle * v.x + self.cosangle * v.y)

    def rotatedInverse(self, v):
        return Vector2(self.cosangle * v.x + self.sinangle * v.y, -self.sinangle * v.x + self.cosangle * v.y)

    # local and world coordinates
    def world(self, local):
        rotate_local = self.rotated(local)
        return self.pos + rotate_local
    
    def local(self, world):
        return self.rotatedInverse(world - self.pos)

    # add a force to the accumulator
    def add_force(self, force, pos=None):
        self.force += force
        if pos is None:
            pos = self.pos
        else:
            self.torque += Vector2.cross(pos - self.pos, force)
    
    # clear the force
    def clear_force(self):
        self.force = Vector2(0, 0)
        self.torque = 0
    
    # helper methods
    def set_pos(self, pos):
        self.pos = Vector2(pos)
    
    def delta_pos(self, delta):
        self.pos += delta

    def set_angle(self, angle):
        self.angle = angle
        self.update_rotation()
    
    def delta_angle(self, delta):
        self.angle += delta
        self.update_rotation()
    
    # apply an impulse
    def impulse(self, imp, pos=None):
        self.vel += imp/self.mass
        if pos is None:
            pos = self.pos
        else:
            self.avel += Vector2.cross(pos - self.pos, imp)/self.momi

# center of rotation = self.pos
# angular velocity = w = self.avel
# angle = theta = self.angle (radians)
# moment of inertia (angular mass) = I = self.momi
# torque T = self.torque = 0 (scalar)

# need to add rotational motion to the update function
# delta self.avel = t/self.momi * dt
# delta self.angle = self.avel * dt
# also clear the torque in clear_force()

# def world(self, local)
#   rotated = rotated_rad()
#   return self.pos + rotated
# def local(self, world)
#   return local_coordinate
# point = pos + offset.roated_rad(angle)
# def rotated_rad(angle)
#   rotated = Vector2(cosangle * offset.x - sinangle * offset.y, sinangle * offset.x + cosangle * offset.y)
#   return rotated