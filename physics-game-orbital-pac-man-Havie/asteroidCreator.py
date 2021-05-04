from circle import Circle
from random import randrange
from globalFunctions import *
import numpy as np
import math
import constVars as const


#Creates as many asteroids to specification
class AsteroidCreator():  #
	def __init__(self, numOfAsteroids=10, color=[255,255,255], mass=1, radius=5, screenBounds=[600,600]):
		self.num= numOfAsteroids
		self.color =color
		self.boundary= screenBounds;
		self.mass = mass;
		self.radius =radius

	def validate(self, pos):
		dis = Distance(pos, [ self.boundary[0]/2, self.boundary[1]/2])
		#print(f"..distance= {dis}")
		return dis > 60


	def RandomPosOnScreen(self):
		pos = [0,0]
		invalid = True
		while invalid :
			pos[0] =randrange(0,600)  # (inclusive, exclusive)?(0,600);
			pos[1] =randrange(0,600);
			invalid = not self.validate(pos)
		#print(f"randPos={pos}")
		return pos

	def GetStartingVelo(self, PositionOnScreen):
		#The initial velocity should be orientated perpendicularly to the displacement from the sun.  
		#print(f"Asteroid Initial pos= {PositionOnScreen}")
		return GetStartingVelo(PositionOnScreen, [ self.boundary[0]/2, self.boundary[1]/2] )


	def CreateAsteroids(self):
		asteroids=[]
		for i in range(self.num):
			pos = self.RandomPosOnScreen()
			centripitalVelo=self.GetStartingVelo(pos)
			asteroid=Circle(pos= pos, velo=centripitalVelo, mass=self.mass, color=self.color , radius = self.radius)
			asteroids.append(asteroid);
			#TEST HACK for drawing dir:
			asteroid.startPos= pos
			asteroid.startVelo=centripitalVelo
		return asteroids




