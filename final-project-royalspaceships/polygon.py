from particle import Particle
import pygame
from pygame.math import Vector2

def intvec(v):
    if v != None:
        return Vector2(round(v.x), round(v.y))

class Polygon(Particle):
    def __init__(self, offsets=[], color=[0,0,0], width=0, normals_length=0, **kwargs):
        # for loop to set offsets
        self.offsets = []
        for o in offsets:
            self.offsets.append(Vector2(o))
        
        self.color = color
        self.width = width
        self.normals_length = normals_length

        # calculate normals for each vertex
        self.local_normals = []
        for i in range(len(offsets)):
            n = (self.offsets[i] - self.offsets[i-1]).rotate(90).normalize()
            self.local_normals.append(n)
        
        self.normals = self.local_normals.copy()

        super().__init__(**kwargs)
        self.points = self.offsets.copy()
        # for o in offsets:
        #     self.points.append(self.pos + o)
        self.update_points()
    
    def update_points(self):
        for i in range(len(self.points)):
            self.points[i] = self.world(self.offsets[i])
            self.normals[i] = self.rotated(self.local_normals[i])

    def update(self, dt):
        super().update(dt)
        self.update_points()
    
    def set_pos(self, pos):
        super().set_pos(pos)
        self.update_points()
    
    def delta_pos(self, delta):
        super().delta_pos(delta)
        self.update_points()
    
    def draw(self, screen):
        # build points
        points = []
        # for o in self.points:
        #     points.append(intvec(self.pos + o))
        pygame.draw.polygon(screen, self.color, self.points, self.width)

        # draw normals
        if self.normals_length > 0:
            for p, n in zip(self.points, self.normals):
                pygame.draw.line(screen, self.color, p, intvec(p + n*self.normals_length))

class UniformPolygon(Polygon):
    def __init__(self, density=1, pos=[0,0], offsets=[], **kwargs):

        sides = []
        for o in offsets:
            sides.append(Vector2(o))

        polygon_mass_of_center_of_mass = Vector2(0)
        total_polygon_mass = 0
        total_polygon_momi = 0

        for i in range(len(sides)):
            triangle_area = (Vector2.cross(sides[i], sides[i-1]))/2
            triangle_mass = density * triangle_area
            total_polygon_mass += triangle_mass

            triangle_momi = triangle_mass / 6 * (sides[i-1].magnitude()**2 + sides[i].magnitude()**2 + Vector2.dot(sides[i-1], sides[i]))
            total_polygon_momi += triangle_momi

            triangle_mass_of_center_of_mass = triangle_mass * (1/3) * (sides[i-1] + sides[i])
            polygon_mass_of_center_of_mass += triangle_mass_of_center_of_mass
        polygon_center_of_mass = polygon_mass_of_center_of_mass / total_polygon_mass

        # move origin to center of mass
        new_offsets = []
        for o in offsets:
            new_offsets.append(o - polygon_center_of_mass)
        
        new_pos = pos + polygon_center_of_mass

        momi_center_of_mass = total_polygon_momi - (total_polygon_mass * polygon_center_of_mass.magnitude()**2)

        # call superclass constructor
        super().__init__(mass=total_polygon_mass, momi=momi_center_of_mass, pos=new_pos, offsets=new_offsets, **kwargs)