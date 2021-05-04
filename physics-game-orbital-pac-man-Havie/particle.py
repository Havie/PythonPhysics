import numpy as np   #should be part of anaconda 
import math
from pygame.math import Vector2 # VECTOR CLASS 

class Particle: 
    #constructor
    def __init__(self, pos=[0,0], velo=[0,0], mass=math.inf):
        self.pos = np.array(pos, float)
        self.velo= np.array(velo, float)
        self.mass = mass
        self.force= np.zeros(2,float) #np.array([0,0], float )

    #do physics
    def update(self, deltaTime):
        #update the velocity assuming constant force
        self.velo += self.force/self.mass * deltaTime
        #update the position assuming constant velocity
        self.pos += self.velo*deltaTime

    #add a force tot he accumaltor
    def addForce(self, force):
        self.force += force

    #clear
    def clearForce(self):
        self.force = np.zeros(2,float) #[0,0]

    def getVelocity(self):
        return self.velo
    



