#collision class 
from circle import *
from wall import *
#from pygame import math.Vector2
import itertools
import pygame


def mag(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


def detectContact(a,b, **kwargs):
    if (isinstance(a,Circle) and isinstance(b,Circle)):
        return circle_circle(a,b,**kwargs);
    if (isinstance(a,Circle) and isinstance(b,Wall)):
        return circle_wall(a,b,**kwargs);
    if (isinstance(a,Wall) and isinstance(b,Circle)):
        return circle_wall(b,a, **kwargs);

def circle_circle(obj1,obj2, **kwargs):
    #do math
    r= obj1.pos - obj2.pos
    overlap = (obj1.radius + obj2.radius) - mag(r);
    magR= mag(r);
    normal= r #r.normalize() #r/mag(r)
    if(magR!=0):
        normal= r/mag(r)
    
    return Contact(obj1,obj2, overlap, normal, **kwargs)




def circle_wall(circle, wall, **kwargs):
    #print("circle wall collision");
    # r= pos
    # R = radius 
    #distanceOfOverlap= (r_wall - r_circle) *normal_wall * Radius_circle
    normalWall= wall.normal;   
    overlap= (wall.pos - circle.pos) * normalWall + (circle.radius)
    #print(f"circle wall overlap = {overlap} , because pos={(wall.pos - circle.pos)} * normal {normalWall} = {(wall.pos - circle.pos) * normalWall} + {(circle.radius)} ")
    return Contact(circle,wall, overlap, normalWall, **kwargs)

class Contact:
    def __init__(self, obj1,obj2, overlap, normal, **kwargs):
         #if( isinstance obj1, Circle) and ( isinstance obj2, Circle):
         #   self.Circle(obj1, obj2)
         self.a=obj1;
         self.b=obj2;
         self.overlap = overlap
         self.normal = normal
         self.kwargs = kwargs

    def isColliding(self): #overload
        #print(f"calling isColliding : ov:{self.overlap} n:{self.normal}")
        return bool(self.overlap>0)
    
    def resolve(self):
        a= self.a
        b=self.b

        #check if overlapying:
        if(self.overlap >0):
            #print(f"{a} overlaps with {b}")
            #temp = m*self.overlap*self.normal
            #a.deltaPos(temp/a.mass)
            m = 1/ (1/ (a.mass + 1/b.mass))
            a.deltaPos( m/a.mass* self.overlap * self.normal)
            b.deltaPos(-m/b.mass* self.overlap * self.normal)
            # resolve velocities
            vi= a.velo - b.velo #inital relative velo 
            vin = vi *self.normal        #Vector2.dot(vi, self.normal)
            if(vin < 0): #if already moving away, dont reverse the velos to come back together 
                restitutaiton = self.kwargs["restitution"]  #dictonary look up k,v
                Jn = -(1+restitutaiton) * m * vin 
                J = Jn * self.normal
                a.impulse(J)
                b.impulse(-J)

# NB: not sure where to put this:
# DOT PRODUCT = projecting a displacement onto one of the vectors
# CROSS PRODUCT= the normal vector between the two being crossed?