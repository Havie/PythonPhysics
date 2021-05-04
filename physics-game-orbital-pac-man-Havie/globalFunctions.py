import math
import numpy as np
import constVars as const
#testVelo=[]
#testPos=[]


def Distance(pos1, pos2):
    #guess i need to abs value something here, unsure why
   
    pos1x = abs(pos1[0])
    pos2x = abs(pos2[0])
    
    pos1y = abs(pos1[1])
    pos2y = abs(pos2[1])

    x= pos1x - pos2x
    y= pos1y - pos2y

    #x= pos2[0] - pos1[0]
    #y= pos2[1] - pos2[0]

    x= x*x 
    y= y*y

    return math.sqrt(x+y)


def DisX(pos1, pos2):
    #comment
    return pos2[0]- pos1[0]

def DisY(pos1, pos2):
    #comment
    return pos2[1]- pos1[1]

def Magnitude(v2):
    return math.sqrt( v2[0] * v2[0] + v2[1] * v2[1])


def Normalize(v2):
    return v2/Magnitude(v2)


def GetPosForValidDistanceFromPos(pos1, desiredDis):
    #no idea  dis= (x2-x1)^2 +  (y2-y1)^2
    validPos= np.array([54,100])

    #so just force guess a pos that is 250 px away

    #print(Distance(pos1, validPos))
    return validPos

def GetGravityForceOLD(mass1, mass2, disX, disY):
    # 20 = (G*200*1) / (300*300)
    
    gameGravity= 1 #9000

    forceX= (gameGravity * mass1 * mass2) / (disX*disX)
    forceY= (gameGravity * mass1 * mass2) / (disY*disY)

    #make in dir of Sun aka mass1
    if(disX >0):
        forceX= 0-forceX
    if(disY >0):
        forceY= 0-forceY

    #print(f"ForceX:{disX} = {forceX} , ForceY:{disY} = {forceY} ")
    return [forceX, forceY]


def GetGravityForceNew(obj1 , obj2):
    mass1 = obj1.mass
    mass2 = obj2.mass
    r =  obj2.pos - obj1.pos;  # r = displacement (or Direction?)
    #r =  obj1.pos - obj2.pos;
    magR= Magnitude(r)
    force = ((-const.GRAVITY * mass1 * mass2) / (magR * magR * magR)) * r
    return force 

def GetStartingVelo(PositionOnScreen, SUNPOS):

    np1=  np.array(PositionOnScreen)
    np2 = np.array(SUNPOS)
    rDir= (np2 - np1) #direction
                                                    # distance = magnitude
    v= math.sqrt((const.GRAVITY * const.SUN_MASS)/ Distance(PositionOnScreen, SUNPOS)**3)  # v= sqrt(Gravity*MASS/ r^3) sometimes you cube the r, sometimes you dont
    retval= (np.cross([0,0,-1], rDir)[0:2] * v) 
    #print(f"The starting velo = {retval}")
    return retval


def GetStartingVeloNormalized(PositionOnScreen, SUNPOS):

    np1=  np.array(PositionOnScreen)
    np2 = np.array(SUNPOS)
    r= (np2 - np1) #direction
    rDir = r/Magnitude(r)  #Normalize
    v= math.sqrt((const.GRAVITY * const.SUN_MASS)/ Distance(PositionOnScreen, SUNPOS))  # v= sqrt(Gravity*MASS/ r^3) sometimes you cube the r, sometimes you dont
    retval= (np.cross([0,0,-1], rDir)[0:2] * v) 
    return retval

def GetStartingVeloCOMPLETELYBROKEN(PositionOnScreen, SUNPOS): 
	#The initial velocity should be oriented perpendicularly to the displacement from the sun.  

    #We shud be doing Velo = sqrt( G* massSun / radius^2 ) , however this np.cross is assuming mSun=1 ?? and G = ???
    #magnitude= 1
	disX= DisX(PositionOnScreen, SUNPOS)
	disY= DisY(PositionOnScreen, SUNPOS)
		
	rDir= np.array([disX, disY])
	return np.cross([0,0,-1], rDir)[0:2]   


def CheckCollision(pos1, pos2, radius1, radius2):
    ##  dis between 2 obj is less than sum of 2 radius ? 
    #print(f"pos1={pos1} pos2={pos2} -> [dis= {Distance(pos1, pos2)}  , rad={radius1+ radius2} ] result= {Distance(pos1, pos2) < radius1+ radius2}")
    return Distance(pos1, pos2) < radius1+ radius2





