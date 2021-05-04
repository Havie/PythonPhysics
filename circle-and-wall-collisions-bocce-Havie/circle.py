#from pygame import *
import pygame
import numpy as np
from particle import Particle
from pygame.math import Vector2 # VECTOR CLASS 

class Circle(Particle):  #how to do inheritance
	                                              #keyword arguments from Particle into a Dict
	def __init__(self, radius=10, color=[255,255,255], width=0, **kwargs): # widwth=0 means filled in
		self.radius = int(radius) 
		self.color =color
		self.width =width;
		self.startPos= Vector2(0, 0)
		self.startVelo= Vector2(0, 0)
		super().__init__(**kwargs) # send the rest of arguments to superclass constructor




	# has to be an int so we type cast to int using np.array()
	def draw(self, screen):
		pygame.draw.circle(screen, self.color ,self.pos, self.radius, self.width);




