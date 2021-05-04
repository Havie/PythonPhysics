from circle import Circle
from wall import Wall
from polygon import Polygon
from polygon import UniformPolygon
import math
import pygame
from pygame.math import Vector2

def mag(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# Detect the Contact, return Contact object
def contact(a, b, **kwargs):
    if isinstance(a, Circle) and isinstance(b, Circle):
        return circle_circle(a, b, **kwargs)
    elif isinstance(a, Circle) and isinstance(b, Wall):
        return circle_wall(a, b, **kwargs)
    elif isinstance(a, Wall) and isinstance(b, Circle):
        return circle_wall(b, a, **kwargs)
    elif isinstance(a, Circle) and isinstance(b, Polygon):
        return circle_polygon(a, b, **kwargs)
    elif isinstance(a, Polygon) and isinstance(b, Circle):
        return circle_polygon(b, a, **kwargs)
    elif isinstance(a, Polygon) and isinstance(b, Wall):
        return polygon_wall(a, b, **kwargs)
    elif isinstance(a, Wall) and isinstance(b, Polygon):
        return polygon_wall(b, a, **kwargs)
    elif isinstance(a, Polygon) and isinstance(b, Polygon):
        return polygon_polygon(a, b, **kwargs)
    elif isinstance(a, UniformPolygon) and isinstance(b, UniformPolygon):
        return polygon_polygon(a, b, **kwargs)

def circle_circle(a, b, **kwargs):
    r = a.pos - b.pos
    overlap = a.radius + b.radius - mag(r)
    normal = r / mag(r)
    contact_point = a.radius * -normal
    return Contact(a, b, overlap, normal, a, contact_point, restitution=0.5, **kwargs)

def circle_wall(circle, wall, **kwargs):
    r = circle.pos - wall.pos
    normal = wall.normal.normalize()
    overlap = pygame.math.Vector2.dot(wall.pos - circle.pos, normal) + circle.radius
    contact_point = circle.pos - circle.radius * normal
    return Contact(circle, wall, overlap, normal, circle, contact_point, restitution=0.3, **kwargs)

def polygon_wall(polygon, wall, **kwargs):
    r = polygon.pos - wall.pos
    normal = wall.normal.normalize()
    # for loop to find point of max overlap
    max_overlap = 0
    # find smallest overlap
    for i in range(len(polygon.points)):
        overlap = (wall.pos - polygon.points[i]) * normal
        if overlap > max_overlap:
            max_overlap = overlap
            max_i = i
    
    if max_overlap > 0:
        return Contact(polygon, wall, max_overlap, normal, polygon, polygon.points[max_i], **kwargs)

    return Contact(polygon, wall, 0, normal, polygon, wall.pos, **kwargs)

def polygon_polygon(a, b, **kwargs):
    penetrator = b
    wall = a
    # Find smallest overlapped side of a from all points in penetrator
    min_overlap_of_max_overlaps1 = math.inf
    for i in range(len(wall.normals)):
        max_overlap = -math.inf
        for j in range(len(penetrator.points)):
            overlap = (wall.points[i] - penetrator.points[j]) * wall.normals[i]
            if overlap > max_overlap:
                max_overlap = overlap
                max_i = i
                max_j = j
        if max_overlap < min_overlap_of_max_overlaps1:
            min_overlap_of_max_overlaps1 = max_overlap
            min_max_i1 = max_i
            min_max_j1 = max_j
    
    # Switch roles
    penetrator = a
    wall = b
    min_overlap_of_max_overlaps2 = math.inf
    # Find smallest overlapped side of a from all points in penetrator
    for i in range(len(wall.normals)):
        max_overlap = -math.inf
        for j in range(len(penetrator.points)):
            overlap = (wall.points[i] - penetrator.points[j]) * wall.normals[i]
            if overlap > max_overlap:
                max_overlap = overlap
                max_i = i
                max_j = j
        if max_overlap < min_overlap_of_max_overlaps2:
            min_overlap_of_max_overlaps2 = max_overlap
            min_max_i2 = max_i
            min_max_j2 = max_j

    # smallest overlapped side of penetrator = wall.normals[min_max_i]
    # point of smallest overlap is = penetrator.points[min_max_j]
    # if min_overlap_of_max_overlaps1 > 0 or min_overlap_of_max_overlaps2 > 0:
    if min_overlap_of_max_overlaps1 < min_overlap_of_max_overlaps2:
        penetrator = b
        wall = a
        smallest_overlapped_side = wall.normals[min_max_i1]
        smallest_overlapped_point = penetrator.points[min_max_j1]
        return Contact(penetrator, wall, min_overlap_of_max_overlaps1, smallest_overlapped_side, penetrator, smallest_overlapped_point, restitution=1, **kwargs)
    else:
        penetrator = a
        wall = b
        smallest_overlapped_side = wall.normals[min_max_i2]
        smallest_overlapped_point = penetrator.points[min_max_j2]
        return Contact(penetrator, wall, min_overlap_of_max_overlaps2, smallest_overlapped_side, penetrator, smallest_overlapped_point, restitution=1, **kwargs)

def circle_polygon(circle, polygon, **kwargs):
    min_overlap = math.inf
    # find smallest overlap
    for i in range(len(polygon.points)):
        overlap = ((polygon.points[i] - circle.pos) * polygon.normals[i]) + circle.radius
        if overlap < min_overlap:
            min_overlap = overlap
            min_i = i
            if min_overlap <= 0:
                break
    
    # return contact
    if 0 < min_overlap < circle.radius:
        point1 = polygon.points[min_i]
        point2 = polygon.points[min_i - 1]

        dist1 = mag(point1 - circle.pos)
        dist2 = mag(point2 - circle.pos)

        if dist1 < dist2:
            closest = point1
            other = point2
        else:
            closest = point2
            other = point1

        s = circle.pos - closest
        vector = closest - other

        if s * vector > 0:
            mags = mag(s)
            overlap = circle.radius - mags
            normal = s / mags
            return Contact(circle, polygon, overlap, normal, polygon, closest, restitution=0.3, **kwargs)

    return Contact(circle, polygon, min_overlap, polygon.normals[min_i], polygon, polygon.points[min_i], restitution=0.3, **kwargs)

class Contact:
    def __init__(self, a, b, overlap, normal, penetrator, point, **kwargs):
        self.a = a
        self.b = b
        self.normal = normal
        self.overlap = overlap
        self.penetrator = penetrator
        self.offset = penetrator.local(point)
        self.kwargs = kwargs
    
    def __bool__(self):
        return self.overlap > 0
    
    def contact_point(self):
        return self.penetrator.world(self.offset)

    def resolve(self):
        # Resolve Overlap
        m = 1/(1/self.a.mass + 1/self.b.mass)
        self.a.delta_pos(m / self.a.mass * self.overlap * self.normal)
        self.b.delta_pos(-m / self.b.mass * self.overlap * self.normal)

        # Resolve Vel
        contact_point = self.contact_point()
        # find displacements
        sa = contact_point - self.a.pos
        sb = contact_point - self.b.pos

        # find velocities
        va = self.a.vel + self.a.avel * Vector2(-sa[1], sa[0])
        vb = self.b.vel + self.b.avel * Vector2(-sa[1], sa[0])


        # if self.a.momi == self.b.momi == math.inf:
        #   sat**2/Ia = 0
        #   sbt**2/Ib = 0

        vi = va - vb
        vin = vi * self.normal
        if vin < 0:
            restitution = self.kwargs["restitution"]
            # n = self.normal
            t = Vector2(-self.normal[1], self.normal[0])
            # sa perpendicular
            sat = sa * t
            # sb perpendicular
            sbt = sb * t
            minv = 1/self.a.mass + 1/self.b.mass + sat**2/self.a.momi + sbt**2/self.b.momi
            # reduced mass
            new_m = 1/minv
            Jn = -(1 + restitution) * new_m * vin
            J = Jn * self.normal

            #Mnn, Mtt, Mnt, Qn, Qt, vns, vnf, Jn, Jt
            # impulse = Jn * n + Jt * t

            self.a.impulse(J, contact_point)
            self.b.impulse(-J, contact_point)