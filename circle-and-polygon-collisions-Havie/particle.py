
import math
from pygame.math import Vector2 # VECTOR CLASS 

class Particle: 
    #constructor
    def __init__(self, pos=[0,0], velo=[0,0], mass=math.inf,angle=0, angularVel=0, momentInertia=math.inf ):
        self.pos = Vector2(pos[0], pos[1])
        self.velo= Vector2(velo[0], velo[1])
        self.mass = mass
        self.force= Vector2(0, 0) #np.zeros(2,float) #np.array([0,0], float )
        self.angle=angle;
        self.angularVelo=angularVel;
        self.momI=momentInertia
        self.torque=0;
        self.updateRotation()

    #do physics
    def update(self, deltaTime):
        #update the velocity assuming constant force
        self.velo += self.force/self.mass * deltaTime
        #update the position assuming constant velocity
        self.pos += self.velo*deltaTime

        self.angularVelo += self.torque/self.momI * deltaTime
        self.angle += self.angularVelo* deltaTime
        self.updateRotation()

    def updateRotation(self):
        # just store cos/sin for V2 
        self.cos= math.cos(self.angle)
        self.sin= math.sin(self.angle)


    def rotate(self, local):
        # { [cos, -sin], [sin, cos]] * [x,y] is  Rotation Matrix 
        offset = local #WorldToLocal(IDK) , v is LOCAL 
        return Vector2( self.cos * offset.x -  self.sin*offset.y  ,   self.sin * offset.x + self.cos * offset.y) #offset is local
        #return Vector2.rotate_rad(v) #Vector2 dot rotMatrix * something idk     

    def InverseRotated(self, local):
        # inverse means [[cosT , sinT ] , [-sinT, cosT]] * [x,y] is  Rotation Matrix 
        offset = local #WorldTolocal(IDK)
        return Vector2( self.cos * offset.x +  self.sin*offset.y  ,   -self.sin * offset.x + self.cos * offset.y)

    def SetAngle(self, angle):
        self.angle = angle;
        self.updateRotation();

    def deltaAngle(self, delta):
        self.angle +=delta;
        self.updateRotation()

    def LocalToWorld(self, local):
        return self.pos + self.rotate(local) 

    def WorldToLocal(self, world):
        return self.InverseRotated(world- self.pos)


    #add a force tot he accumaltor
    def addForce(self, force, pos=None):
        self.force += force
        if(pos is None):
            pos=self.pos;
        self.torque = Vector2.cross(pos-self.pos, force) # r = displacement to obj, and f = where force is being applied

    #clear
    def clearForce(self):
        self.force =  Vector2(0, 0) #[0,0]
    def clearVelo(self):
        self.velo=  Vector2(0, 0)

    def getVelocity(self):
        return self.velo

    #helper methods:
    def setPos(self, pos):
        self.pos= Vector2(pos[0], pos[1]);

    def deltaPos(self, delta):
        self.pos +=Vector2(delta);
    
    def impulse(self, force, pos =None):
        #change in velo = impulse / mass 
        if(pos is None):
            pos=self.pos;
        self.velo += Vector2(force[0], force[1])/self.mass;
        #self.velo += force/self.mass; # think these r both V2s now?
        self.angularVelo += Vector2.cross(pos-self.pos, force) / self.momI;



        #do something by hand:
        #<-w s_y , w s_x> 

