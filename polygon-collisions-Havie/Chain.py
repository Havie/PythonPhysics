from Forces import *
import pygame 

class Chain(BondForce):
    def __init__(self ,k=1, naturalLen=1, damp=1,  **kwargs):
        self.k=k
        self.len=naturalLen
        self.damp=damp;
        super().__init__(**kwargs) # send the rest of arguments to superclass constructor

    def apply(self):
        for a,b in self.pairs: 
            #print(f"does this work? {a}, {b}")
            r = (a.pos - b.pos)
            v= a.velo - b.velo
            force= self.force(r, v)
            #print(f"Chain force result was {force} ")
            a.addForce(force)
            b.addForce(-force)

    def force(self, r, v):
        #force =  pygame.math.Vector2(0,0).normalize
        #Fspring= (-k * ( mag(r) - l) -b*v * r_hat) *r_hat
        #r is a vector which is pos1 - pos2 
        #r_hat is a unit vector version of r (v/mag(v)) or r.normalized)
        r_hat = r.normalize()
        mag_r = pygame.math.Vector2.magnitude(r)
        #v is the velo1 - velo2  
        k=self.k
        l=self.len
        b=self.damp

        #testDOT= (b*v) * r_hat
        #print(f"Test={testDOT}")

        return (-k * (mag_r -l) -(b*v) * r_hat) * r_hat