from particle import Particle
import pygame
from pygame.math import Vector2

def intvec(v):
    if v != None:
        return Vector2(round(v.x), round(v.y))

class PolygonTrap(Particle):
    def __init__(self, localOffsets=[], color=[0,0,0], width=0, normals_length=0, **kwargs):
        # for loop to set localOffsets
        self.localOffsets = []
        for o in localOffsets:
            self.localOffsets.append(Vector2(o))
        self.color = color
        self.width = width
        self.normals_length = normals_length
        # calculate normals for each vertex
        self.localNormals = []
        for i in range(len(localOffsets)):
            n = (self.localOffsets[i] - self.localOffsets[i-1]).rotate(90).normalize()
            self.localNormals.append(n)

        self.worldNormals= self.localNormals.copy()
        super().__init__(**kwargs)

        #generate our world points:
        self.worldPoints =[]
        for o in self.localOffsets:
            #this could be anything as it gets over written immediately in updateWorldPoints():
            self.worldPoints.append( self.LocalToWorld(o))
            #self.points.append(self.pos +o)
    
        self.updateWorldPoints()

    def updateWorldPoints(self):
        for i in range(len(self.worldPoints)):
            # I would think self.pos is world, and they localOffsets are local:
            self.worldPoints[i] =  self.LocalToWorld(self.localOffsets[i])
            #also update our normals? todo:
            self.worldNormals[i] = self.rotate(self.localNormals[i])
            # self.points[i] = self.pos + self.localOffsets[i]



    def update(self, dt):
        super().update(dt)
        self.updateWorldPoints()


    def draw(self, screen):
        # build points
        points = []
        # for o in self.localOffsets:
        #     points.append(intvec(self.pos + o))
        for worldPoint in self.worldPoints:
            points.append(intvec(worldPoint))

        pygame.draw.polygon(screen, self.color, points, self.width)

        # draw normals
        # if self.normals_length > 0:
        #     for p, n in zip(points, self.worldNormals):
        #         pygame.draw.line(screen, self.color, p, intvec(p + n*self.normals_length))










