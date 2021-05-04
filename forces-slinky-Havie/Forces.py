
import math
import pygame #from pygame.math import Vector2 # VECTOR CLASS 

class SingleForce:
    def __init__(self, objects=[]):
        self.objects=objects


    def apply(self):
        print("apply SingleForce");
        #forreach obh add force 

    def force(self):
        return pygame.math.Vector2(0,0)

## ** kwargs means look for stuff separated by commas, and pack into a dictionary
class PairForce:
    def __init__(self, objects=[]):
        self.objects=objects


    def apply(self):
        print(apply);       
        #need to seearch over all pairs of objs

        #third way generates pairs: 
        for a,b in itertools.combinations(self.objects,2):
            a.add_force(force);
            b.add_force(-force);
    
        def force(self):
            return pygame.math.Vector2(0,0)

class BondForce:
    def __init__ (self, pair = []):
        self.pairs= pair

        #pairs = list of objs in system 
        #pairs = [ [objects[o], objects[1] ,  [objects[1], objects[2] ] 


        def apply(self):
            #for pair in self.pairs:
            #    a,b = pair #extract [0], [1]
            #    print(f"does this work? {a}, {b}")

            for a,b in self.pairs: 
                print(f"does this work? {a}, {b}")
                a.addForce(self.force())
                b.addForce(-self.force())


        def force(self):
            return pygame.math.Vector2(0,0)