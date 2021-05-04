import pygame
from circle import Circle
from Contact import *
from polygon import *
import constVars as const
from random import randrange


def CheckCollision(pos1, pos2, radius1, radius2):
    ##  dis between 2 obj is less than sum of 2 radius ? 
    #print(f"pos1={pos1} pos2={pos2} -> [dis= {Distance(pos1, pos2)}  , rad={radius1+ radius2} ] result= {Distance(pos1, pos2) < radius1+ radius2}")
    dis = pygame.math.Vector2.magnitude(pos1 - pos2)
    return dis < radius1+ radius2


def InstantiateBall(pos, color):
    return Circle(radius = const.SPHERE_RADIUS,color=color,width=0,pos=pos, velo=[0,0], mass=const.BALL_MASS )

def InstantiateBall(radius, pos, color):
    return Circle(radius = radius,color=color,width=0,pos=pos, velo=[0,0], mass=const.BALL_MASS )

def GetRandomStartPos():
    valueRandX= randrange(200,500)  # (inclusive, exclusive)?.
    valueRandY= randrange(100,500)  # (inclusive, exclusive)?.
    return [valueRandX, valueRandY]


def MakeARandomPolygon(polyPos):
    offsets=[
        [0,0],
        [0,10],
        [10,60],
        [100,50],
        [70,0]
        ]
    return Polygon(offsets,pos=polyPos, color=const.BLACK,width=0, normals_length=50, angularVel=randrange(1,2))

def GetRandomStartPosNoCollisions(listOfLocToAvoid):
        isColliding=True
        while(isColliding):
            pos= GetRandomStartPos()
            dummy=  Circle(10, pos=pos); #Circle(50, color=const.LIGHT_GREEN, width= 0, pos=endPos, velo=[0,0], mass=math.inf)
            isColliding=False
            for thing in listOfLocToAvoid:
                c= detectContact(dummy,thing, restitution=0.3)
                tooClose = (pos- thing.pos).magnitude() < 100
                if(c.isColliding() or tooClose):
                    isColliding = True
        return pos

def IdentifyWinner(pallino, closestBall_P1, closestBall_P2):

    if(pallino == None or closestBall_P1 ==None or closestBall_P2 ==None):
        #print("fake return")
        return -1

    dis1= abs( (pallino.pos - closestBall_P1.pos).magnitude())
    dis2= abs( (pallino.pos - closestBall_P2.pos).magnitude())
    if(dis1==dis2):
            return 0
    elif(dis1<dis2):
            return 1
    else:
            return 2

def IsClosestPlayersTurn(sName, iNum):
     if(sName=="Player1" and iNum==1):
         return True
     if(sName=="Player2" and iNum==2):
         return True
     return False;

def TryAdvanceTurn(tm, objects, pallino, closestBall_P1, closestBall_P2):
    if(len(objects)>0):
        closestPlayerNum=IdentifyWinner(pallino, closestBall_P1, closestBall_P2)
        #tm.SwitchTurn();
        #COULDNT FIGURE THIS OUT, not worth the 1 point >.< built this wrong from the beginning 
        if(closestPlayerNum == -1):
            tm.SwitchTurn()
        else:
           closestPlayersTurn= tm.WhosTurnNum() == closestPlayerNum;
           #print(f"closest player={closestPlayerNum} ... their turn = {closestPlayersTurn}")
           if(closestPlayersTurn or tm.IsCurrPlayerOutOfBalls()):
                #print("want to switc turn becuz winning player")
                if(not tm.IsNextPlayerOutOfBalls()):
                    tm.SwitchTurn();
                    #print("safe to switch becuz IsNextPlayerOutOfBalls")
