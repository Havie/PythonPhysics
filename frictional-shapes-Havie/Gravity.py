
import math
import pygame
from Forces import *
#from pygame.math import Vector2 # VECTOR CLASS 


## ** kwargs means look for stuff separated by commas, and pack into a dictionary
class Gravity(SingleForce):
    def __init__(self, acc=[0,0] , **kwargs):
        self.acc =pygame.math.Vector2(acc[0], acc[1]) #        np.array(acc, float) # or vector2
        super().__init__(**kwargs) # send the rest of arguments to superclass constructor

    def force(self, obj):
        return obj.mass * self.acc

    def apply(self):
        #print("apply Gravity");
        for o in self.objects:
            o.addForce(self.force(o))