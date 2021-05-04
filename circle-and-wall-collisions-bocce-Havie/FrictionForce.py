
import math
import pygame
from Forces import *
#from pygame.math import Vector2 # VECTOR CLASS 


## ** kwargs means look for stuff separated by commas, and pack into a dictionary
class Friction(SingleForce):
    def __init__(self, g=10, mew=-0.3 , **kwargs):
        self.g=g
        self.mew=mew;
        super().__init__(**kwargs) # send the rest of arguments to superclass constructor

    def force(self, obj):
        #Force = -mew * m * g * v_hat
        mew = self.mew
        m= obj.mass
        g=  self.g #who knows?
        v_hat= obj.velo;
        if(v_hat.magnitude()!=0):
            v_hat=v_hat.normalize()
            #print(f".. friction = { mew*m*g*v_hat}")
        return mew*m*g*v_hat

    def apply(self):
        #print(f"apply Friction to #{len(self.objects)}Objs");
        for o in self.objects:
            o.addForce(self.force(o))