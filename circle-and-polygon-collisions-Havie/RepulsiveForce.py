from Forces import *
from globalFunctions import *

class Repulsion(BondForce):
    def __init__(self, k=0 , objList=[] , **kwargs):
        self.k=k
        self.objs=objList
        super().__init__(**kwargs) # send the rest of arguments to superclass constructor



    def apply(self):
        # COLLISION: Check dis between 2 obj is less than sum of 2 radius
        #for a,b in self.pairs: 
        #    #print(f"does this work? {a}, {b}")
        #    R_a= a.radius
        #    R_b= b.radius
        #    if(self.CheckCollision(a.pos, b.pos, R_a, R_b)):
        #        r = (a.pos - b.pos)
        #        force= self.force(r, R_a, R_b)
        #        print(f"Repulsion force result was {force} ")
        #        a.addForce(force)
        #        b.addForce(-force)
        
        #DO THINGS THIS WAY TO REPLY OFF EVERY SPHERE,NOT JUST PAIRS:
        for a in self.objs:
            for b in self.objs:
                if(a!=b):
                    R_a= a.radius
                    R_b= b.radius
                    #if(CheckCollision(a.pos, b.pos, R_a, R_b)):  #I am double checking for a collision >.< whoops
                    r = (a.pos - b.pos)
                    force= self.force(r, R_a, R_b)
                    #print(f"Repulsion force result was {force} ")
                    a.addForce(force)
                    b.addForce(-force)



    def force(self, r, R_a, R_b):
        #R = radius of a circle 
        #r = posVector
        r_hat = r.normalize()
        k= self.k

        collision= R_a + R_b - pygame.math.Vector2.magnitude(r)
        retVal= pygame.math.Vector2(0,0) 
        if(collision>0): # Mathy way of doing collision check
            retVal = k * collision * r_hat

        # k * (r_a + r_b - mag(r)) * r_hat    OR V2.zero
        return retVal