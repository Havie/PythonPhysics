from polygon import *
from pygame.math import Vector2 # VECTOR CLASS 

class UniformPolygon(Polygon):
    def __init__(self, density=1,localOffsets=[], pos=[0,0], value=1,  **kwargs):
        self.value = value
        # for loop to set localOffsets
        #print("implement whatever logic is happening ")
        #calculate mass Triange, Inertia Triangle, massT times CenterMass Triangle 
        #calculate M * I * R
        #adjust center and I 

        #mass  = density * area of Triangle 
        #break all of our local offsets down into sub triangles?????
        #localOffsets=[[0,0], [100, 0], [100,20], [0,20]]
        # point1= offset[i] , point2= offset[i+1] , point Center = pos.center? even tho its not passed in 
        totalMass= 0
        totalMomi= 0
        SumCenterMass= pygame.Vector2(0)
        for i in range(len(localOffsets)):
            #points are actually sides becuz local origin is zero zero
            point1=  Vector2(localOffsets[i-1]) # PYTHON WILL GRAB THE LAST INDEX CUZ ITS WEIRD, so this is desired 
            point2=  Vector2(localOffsets[i])
            triangleMass = (density * (0.5 * Vector2.cross(point2,  point1)))
            totalMass += triangleMass
            triangleMomi = (triangleMass/6) * (point1.magnitude_squared() + point2.magnitude_squared() + pygame.Vector2.dot(point1, point2) )
            totalMomi += triangleMomi
            triangleCenterMass =  (1/3) * (point1+point2) 
            SumCenterMass += triangleCenterMass * triangleMass
            
        centerOfMassActual = SumCenterMass / totalMass

        newOffsets=[]
        for offset in localOffsets:
            newOffsets.append(offset - centerOfMassActual)
            #print(f"newOffset: {offset - centerOfMassActual}")

        newPos = pos+centerOfMassActual
        momiCentered  = totalMomi  - totalMass * centerOfMassActual.magnitude_squared()  
        
        #print(f"TotalMass= {totalMass} , centerOfMassActual= {centerOfMassActual} , momiCentered={momiCentered}")

        super().__init__(mass=totalMass, momentInertia=momiCentered, pos=newPos, localOffsets=newOffsets, **kwargs)
 





#mass of a triangle = density * areaOfTriangle       
    #area of triangle = 0.5 base * height, but we dont have that we have sides (vectors)
    # Instead find vol of parraell pipet from Linear Algebra?
        #which is a cross product of a rombus, then we divid that by 2 (aka 0.5)
        # Density * (0.5 side1 CROSS side 2)
            # Cross prod can be neg or pos, and thats signed area , if we do it the right way, shud be pos when all added 2gether??

#moment of inertia of a Triangle = I spun by corner 
    #  = mass_triangle/6 * (mag(Side 1)^2 + mag(Side 2)^2 + Side1 dot Side2)


#center of Mass, = CAPITAL R as a vector
    # Sum of the mass of each obj that composes it * the Center of mass for each part,  divide by the sum of the masses?
    #  (sum each mass * Center of mass each ?) / Sum of Mass       ?????????
    #  M*R =   1/3(Side1+Side2)        I think this is for each side?


    #Next need to move local origin to center???
    # Shift this somehow, but subracting center of mass  - origin = R , from each of our offsets?
    # then add R to the position

# finally use the parallel Axis theorem to find the correct  moment of intertia?

    # I offcenter  = I centered  + Mass of shape * mag(displacement)^2  
    #displamcen is the pivot point from center of mass

    # IcenterMass = IOffset-  Mass of shape * mag(displacement)^2  
    # call super class constructor 




#this might be how to check by hand? not in code
# I = M/ 12 (leng^2 + height^2)






#MORE notes on Torque and impulse off-center
# r= obj pos 
# r_f = force Position
# F  = force vector 
# s= displamcent (r_f - r)
# Torque=  s cross F 
# def add_force(self,force, impulsePos=None):
# self.force += force
# if (pos is not None):
#   self.torque += Vec2.Cross(pos=self.pos , force) 


#need rotation on impulse:
# Impulse =  Force * deltaTime
# so if there is an impulse offcenter, then we'll have a rotational impulse too
# rotationalImpulse = Torque * deltaTime
# Torque = displacement cross Force 
# rotaitonalImpulse = s Cross (J)
# J = impulse

#change in angular mommentum
# deltaL = I * deltaW
# deltaW = deltaL / I 
# def impulse(self,impulse, pos=None):
# self.velo += impulse / mass 
# if(pos is not None):
#  rotationalImpulse = Vector2.Cross(s, F)
#  self.aVelo += rotationalImpulse / self.momI 


#Modify Resolve Function to include rotation
# something has a linear velo and an angular velo 
# i guess a means shape A 
# sa = rc - ra (displacement = contact point - center?)
# velo_contactPoint = veloPrime?
# velo_contactPointA = veloA + Wa cross Sa 
    # S_aPerpendicular = <- S_ay, S_ax > is result??
# velo_contactPointB = veloB + Wb cross Sb
# V =   velo_contactPointA - velo_contactPointB
# we want the normal component of V to multiped by -E 
# -E = coefficient of restitituion
# vNi = Vi * normal 
# vNf = -E * VNi 
# ChangInVelo = deltaVn 
# deltaVn = -(1 + E) * vNi
# without rotation deltaV = J / mass 
# so delta Vn = Jn/ mass     becuz impulse is only in the normal DIR 
# m is the reduced mass (whatver that means?) 
# reducedMass = 1 / (1/ma + 1/mb) 
# what is the response of an impulse H = Jn * n
# change in VeloA = J / ma 
# change in angularMomA= (Sa cross J)  / momIa
# change in VeloB = - J / mb 
# change in angularMomB= -(Sb cross J)  / momIb
# changeVeloADelta = changeVeloA + changeWa * SaPerpindeicular 
    # J / Ma + (Sa cross J / momIa)  * SaPerpindeicular 
    # J / Ma * N +  (Sa cross J / momIa)  * SaPerpindeicular 
    # dot both sides by Normal (N)
    # changeInVeloA * N =  Jn/Ma + (AWHOLE BUNCH OF STUFF)
        # N is like x, tangental T is like y
        # Sa = SanN + SatT
        # Sa = -Sat N + San T
    # Sa cross N = San N cross N + S at T cross N 

# changeInVeloAPrime * N = Jn/massA + [ (SaT)^2 / momIa] * Jn
# changeInVeloBPrime * N = -Jn/massB - [ (SbT)^2 / momIb] * Jn
# deltaV* N  = I GIVE UP 
# Jn = some massive thing 
# If infinity makes it into here somehow, Ia = Ib = Inf , we cant rotate 
# something goes to zero, and were left w reduce mass?
# if our shapes can rotate, it increases the denomnitor, so less impulse is needed to resolve the collision (watever this means)

#Sat = Sa dot T where T = perpidicular to Normal <-ny , nx> 
# or
#Sat = Sa Cross N 

# recommend minV = (1/a.mass + 1/b.mass ) + sAt * 2/a.momi + sBt * 2/b.momi
# m = 1/minV  
