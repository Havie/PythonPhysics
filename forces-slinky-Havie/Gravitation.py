
import math
import pygame
from Forces import *
#from pygame.math import Vector2 # VECTOR CLASS 


## ** kwargs means look for stuff separated by commas, and pack into a dictionary
class Gravitation(PairForce):
    def __init__(self, G=0 , **kwargs):
        self.G=G   
        super().__init__(**kwargs) # send the rest of arguments to superclass constructor



    def force(self, a,b):
        r= a.pos-b.pos
        return -self.G * a.mass * b.mass / r.magnitude()**3 *r
