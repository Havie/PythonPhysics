#collision class 
from circle import *
from wall import *
from polygon import *
from UniformPolygon import *
#from pygame import math.Vector2
import itertools
import pygame
import math

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
    if (isinstance(a,Polygon) and isinstance(b,Polygon)):
        return polygon_polygon(a,b,**kwargs);
    if (isinstance(a,Polygon) and isinstance(b,Wall)):
        return polygon_wall(a,b, **kwargs);
    if (isinstance(a,Wall) and isinstance(b,Polygon)):
        return polygon_wall(b,a,  **kwargs);



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
    min_normal= pygame.math.Vector2(0); 
    min_overlap = math.inf;
    for i in range(len(poly.worldPoints)):
        overlap = ((poly.worldPoints[i] - circ.pos) *poly.worldNormals[i]) + circ.radius
        if(overlap < min_overlap):
            min_overlap= overlap;
            min_i=i
            if(min_overlap <=0):
                break;

    if 0 < min_overlap < circ.radius:
        point1 = poly.worldPoints[min_i]
        point2 = poly.worldPoints[min_i-1]

        dis1= (point1-circ.pos).magnitude()
        dis2= (point2-circ.pos).magnitude()

        if(dis1 < dis2):
            closest = point1;
            other=point2;
        else:
            closest= point2
            other=point1;

        s= circ.pos - closest;
        vector= closest-other;

        if(s *vector > 0): #dot overload
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
    min_normal = poly.worldNormals[min_i];
    polyRadius = min_overlap; # Polygon does not have a radius attribute poly.radius TODO?
    contactPoint = circ.pos - polyRadius *min_normal
    return Contact(circ,poly, min_overlap, min_normal, circ, contactPoint,  **kwargs);

def polygon_polygon(poly1,poly2, **kwargs):
    penetrator1 = poly1
    wall1 = poly2
    # Find smallest overlapped side of a from all points in penetrator
    minOverlapA = math.inf
    iSmallest1= math.inf
    jSmallest1 = math.inf
    for i in range(len(wall1.localNormals)):
        maxOverlap = (0 - math.inf)
        for j in range(len(penetrator1.worldPoints)):
            overlap = (wall1.worldPoints[i] - penetrator1.worldPoints[j]) * wall1.localNormals[i]
            if overlap > maxOverlap:
                maxOverlap = overlap
                iMax = i
                jMax = j
        if maxOverlap < minOverlapA:
            minOverlapA = maxOverlap
            iSmallest1 = iMax
            jSmallest1 = jMax
    #Reverse the order, swapping the two polys
    penetrator2 = poly1
    wall2 = poly2
    minOverlapB = math.inf
    iSmallest2= math.inf
    jSmallest2 = math.inf
    for i in range(len(wall2.localNormals)):
        maxOverlap = (0 - math.inf)
        for j in range(len(penetrator2.worldPoints)):
            overlap = (wall2.worldPoints[i] - penetrator2.worldPoints[j]) * wall2.localNormals[i]
            if overlap > maxOverlap:
                maxOverlap = overlap
                iMax = i
                jMax = j
        if maxOverlap < minOverlapA:
            minOverlapB = maxOverlap
            iSmallest2 = iMax
            jSmallest2 = jMax

    #compare results to identify which is penetrator
    #assume first is true
    correctWall = poly2;
    correctPenetrator=poly1;
    correctMinI=iSmallest1
    correctMinJ=jSmallest1
    correctMaxOverlap = minOverlapA
    #correct it if not
    if(minOverlapB < minOverlapA):
        correctWall = poly1;
        correctPenetrator=poly2;
        correctMinI=iSmallest2
        correctMinJ=jSmallest2
        correctMaxOverlap = minOverlapB

    #calculate the rest of the info using correct circumstance
    smallestOverlappedPen = correctWall.localNormals[correctMinI]
    smallestOverlappedPoint = correctPenetrator.worldPoints[correctMinJ]

    return Contact(poly1, poly2, correctMaxOverlap, smallestOverlappedPen, correctPenetrator, smallestOverlappedPoint,  **kwargs);


def polygon_wall(poly,wall, **kwargs):
    #find most embedded point in a wall? find overlap between each point and the wall (maximumOverlap is most embedded)
    #overlap = maxOverlap, point= pointOfMaxOverlap, penetrator = poly1
    maxPointOfOverlap=0
    maxOverlap = 0 - math.inf
    normal = wall.normal
    contactPoint= None #first one will become contact, wont be null
    for worldPoint in poly.worldPoints:
        overlap =  (wall.pos - worldPoint) * normal
        #print(f"Found point= {worldPoint} normal={ wall.normal} ... overlap= {overlap} vs {maxOverlap} ")
        if(overlap > maxOverlap):
            maxOverlap = overlap;
            contactPoint = worldPoint;

    
    return Contact(poly,wall, maxOverlap, normal, poly, contactPoint,  **kwargs);


class Contact:
    def __init__(self, obj1,obj2, overlap, normal, penetrator, point, **kwargs):
         #if( isinstance obj1, Circle) and ( isinstance obj2, Circle):
         #   self.Circle(obj1, obj2)
         self.a=obj1;
         self.b=obj2;
         self.overlap = overlap
         self.normal = normal
         self.pen= penetrator
         self.offset = penetrator.WorldToLocal(point)
         self.kwargs = kwargs

    def isColliding(self): #overload
        #print(f"calling isColliding : ov:{self.overlap} n:{self.normal}")
        return bool(self.overlap > 0)
    
    def contactPoint(self):
        #print("each caluclate function must calculate and save the contact point");
        return self.pen.LocalToWorld(self.offset);

    def resolve(self):
        obj1= self.a
        obj2= self.b

        #print(f"overlap to resolve={self.overlap}")
        #check if overlapying:
        if(self.overlap > 0):
            #print(f"{a} overlaps with {b}")
            #temp = m*self.overlap*self.normal
            #a.deltaPos(temp/a.mass)
            m = 1 / (1 / obj1.mass + 1/obj2.mass)
            obj1.deltaPos( m / obj1.mass * self.overlap * self.normal)
            obj2.deltaPos(-m / obj2.mass * self.overlap * self.normal)
            # resolve velocities
            #velo A at contactPoint = V_a + V_aRotational       V_aRotational =(w_a cross S_a)    S_a = rcontact-r??
            contactPoint= self.contactPoint()
            # formerly sa and sb, s stands for distance?
            displacementObj1= contactPoint - obj1.pos 
            displacementObj2= contactPoint - obj2.pos 
            #    float  + float * Vector?
            veloObj1 = obj1.velo + obj1.angularVelo * pygame.math.Vector2(-displacementObj1.y, displacementObj1.x) # NOT SURE?
            veloObj2 = obj2.velo + obj2.angularVelo * pygame.math.Vector2(-displacementObj2.y, displacementObj2.x) # NOT SURE?
            #formerly vi
            veloInitial = veloObj1 - veloObj2;
            #formerly vin
            veloInitialRelative = veloInitial * self.normal        #Vector2.dot(vi, self.normal)
            if(veloInitialRelative < 0): #if already moving away, dont reverse the velos to come back together 
                restitution = self.kwargs["restitution"]  #dictonary look up k,v
                #J stands for impulse, no idea what this forumla derives from?
                newMForRotation = 1 / ( (1 / obj1.mass + 1/obj2.mass) + pygame.Vector2.cross(displacementObj1, self.normal)**2/obj1.momI  + pygame.Vector2.cross(displacementObj2, self.normal)**2/obj2.momI )
                Jn = -(1 + restitution) * newMForRotation * veloInitialRelative 
                J = Jn * self.normal
                obj1.impulse(J, contactPoint)
                obj2.impulse(-J, contactPoint)

# NB: not sure where to put this:
# DOT PRODUCT = projecting a displacement onto one of the vectors
# CROSS PRODUCT= the normal vector between the two being crossed?