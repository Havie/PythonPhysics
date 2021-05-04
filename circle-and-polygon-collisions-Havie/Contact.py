#collision class 
from circle import *
from wall import *
from polygon import *
from polygonTrap import *
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
    if (isinstance(a,Circle) and isinstance(b,Polygon)):
        return circle_polygon(a,b,**kwargs);
    if (isinstance(a,Polygon) and isinstance(b,Circle)):
        return circle_polygon(b,a, **kwargs);
    if (isinstance(a,PolygonTrap) and isinstance(b,Circle)):
        return circle_polygon(b,a, **kwargs);
    if (isinstance(a,Circle) and isinstance(b,PolygonTrap)):
        return circle_polygon(a,b,**kwargs);

def circle_circle(obj1,obj2, **kwargs):
    #do math
    r= obj1.pos - obj2.pos  # r = displacement
    overlap = (obj1.radius + obj2.radius) - mag(r);
    magR= mag(r);
    normal= r #r.normalize() #r/mag(r)
    if(magR!=0):
        normal= r/mag(r)
    #figure out contactPoint
    contactPoint = obj1.pos - (obj2.radius * normal); #how does obj2 get a Normal? this is for wall class?
    return Contact(obj1,obj2, overlap, normal,obj1, contactPoint, **kwargs)


def circle_wall(circle, wall, **kwargs):
    #print("circle wall collision");
    # r= pos
    # R = radius 
    #distanceOfOverlap= (r_wall - r_circle) *normal_wall * Radius_circle
    normalWall= wall.normal;   
    overlap= (wall.pos - circle.pos) * normalWall + (circle.radius)
    #print(f"circle wall overlap = {overlap} , because pos={(wall.pos - circle.pos)} * normal {normalWall} = {(wall.pos - circle.pos) * normalWall} + {(circle.radius)} ")
    # r_contact = r_circle - R_circle * normal 
    contactPoint = circle.pos - circle.radius* normalWall;
    return Contact(circle,wall, overlap, normalWall,circle, contactPoint, **kwargs)


def circle_polygon(circ, poly,  **kwargs):
    #apparently you dont need to instantiate  min_vertex, min_normal outside the foor loop in pythons scope:
    #min_vertex= None;
    min_normal= pygame.math.Vector2(0); # IDK if this is right??
    min_overlap = math.inf;

    #for o, n in zip(poly.offsets,poly.worldNormals):
    #    overlap = (((poly.pos + o )- circle.pos ) * n) + circle.radius; # multiplication = Dot overload in V2 
    #    if(overlap < min_overlap):
    #        min_overlap=overlap;
    #        min_vertex=poly.pos + o  # IDK WHAT THIS IS USED FOR?
    #        min_normal=n

    min_overlap= math.inf
    for i in range(len(poly.worldPoints)):
        overlap = ((poly.worldPoints[i] - circ.pos) *poly.worldNormals[i]) + circ.radius
        if(overlap < min_overlap):
            min_overlap= overlap;
            min_i=i
            if(min_overlap <=0):
                break;

    if 0 < min_overlap <circ.radius:
        point1 = poly.worldPoints[min_i]
        point2 = poly.worldPoints[min_i-1]

        dis1= (point1-circ.pos).magnitude()
        dis2= (point2-circ.pos).magnitude()

        if(dis1 <dis2):
            closest = point1;
            other=point2;
        else:
            closest= point2
            other=point1;

        s= circ.pos - closest;
        vector= closest-other;

        if(s *vector >0): #dot overload
            mags= s.magnitude()
            overlap = circ.radius - mags
            if(mags != 0): 
                normal = s.normalize() #s/mags
            else:
                normal = pygame.math.Vector2(0) # NO IDEA?
            contactPoint =closest;
            return Contact(circ, poly, min_overlap,poly.worldNormals[i],circ, contactPoint, **kwargs)


     #Have to figure out whos the penetrator.. Just default it to the circle?
     #figure out contactPoint
     #TODO- No idea? default to circle pos , "its the closest vertex as the contact point" 
     # dont have access to a normal ?
    min_normal =poly.worldNormals[min_i];
    polyRadius = min_overlap; # Polygon does not have a radius attribute poly.radius TODO?
    contactPoint = circ.pos - polyRadius *min_normal
    return Contact(circ,poly, min_overlap, min_normal, circ, contactPoint,  **kwargs);

class Contact:
    def __init__(self, obj1,obj2, overlap, normal, penetrator, point, **kwargs):
         #if( isinstance obj1, Circle) and ( isinstance obj2, Circle):
         #   self.Circle(obj1, obj2)
         self.a=obj1;
         self.b=obj2;
         self.overlap = overlap
         self.normal = normal
         self.pen= penetrator
         self.offset = penetrator.LocalToWorld(point)
         self.kwargs = kwargs

    def isColliding(self): #overload
        #print(f"calling isColliding : ov:{self.overlap} n:{self.normal}")
        return bool(self.overlap>0)
    
    def contactPoint(self):
        #print("each caluclate function must calculate and save the contact point");
        return self.pen.WorldToLocal(self.offset);

    def resolve(self):
        a= self.a
        b= self.b

        #check if overlapying:
        if(self.overlap >0):
            #print(f"{a} overlaps with {b}")
            #temp = m*self.overlap*self.normal
            #a.deltaPos(temp/a.mass)
            m = 1 / (1/ (a.mass + 1/b.mass))
            a.deltaPos( m/a.mass* self.overlap * self.normal)
            b.deltaPos(-m/b.mass* self.overlap * self.normal)
            # resolve velocities
            #velo A at contactPoint = V_a + V_aRotational       V_aRotational =(w_a cross S_a)    S_a = rcontact-r??
            contactPoint= self.contactPoint()
            sa= contactPoint - a.pos 
            sb= contactPoint - b.pos 
            #    float  + float * Vector?
            va = a.velo + a.angularVelo * pygame.math.Vector2(-sa.y, sa.x) # NOT SURE?
            vb = a.velo + b.angularVelo * pygame.math.Vector2(-sb.y, sb.x) # NOT SURE?
            vi = va-vb;
            #vi= a.velo - b.velo #inital relative velo 
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