import pygame
from circle import Circle
from pygame.math import Vector2 # VECTOR CLASS 
from Gravity import *
from Contact import *
import itertools 
import constVars as const
import time
from globalFunctions import *
from TurnManager import *
from FrictionForce import *
from polygon import *
from UniformPolygon import *
from Shape import *

screenBounds=[800,600]
screen = pygame.display.set_mode(screenBounds);
fps = 60
deltaTime= 1/fps
clock = pygame.time.Clock()
#create font object
pygame.font.init();
pygame.init();
tileFont = pygame.font.SysFont('Calibri', size=25, bold=True, italic=False)
msgFont = pygame.font.SysFont('Calibri', size=15, bold=False, italic=True)

global objects
global walls
global bullets
global forces
global RUNNING
global PAUSED
global playerPoly
global startPos
global ledge
global shootingCD
global firingRate
global dropRate
global timeSinceLastDrop    
global shapesByScore
P1_COLOR = const.ORANGE


def StartGame():
    global objects
    global walls
    global bullets
    global forces
    global RUNNING
    global PAUSED
    global playerPoly
    global startPos
    global P1_COLOR
    global ledge
    global shootingCD
    global firingRate
    global dropRate
    global timeSinceLastDrop  
    global shapesByScore 
    objects = []
    forces = []
    walls= []
    bullets= []
    shootingCD=1
    firingRate=0.2 # 5 shots per second
    dropRate = 1
    timeSinceLastDrop= dropRate #drop immediately  
    startPos= [400,500]
    localOffsets=[
        [0,0],
        [20,-40],
        [40,0]
    ]
    playerPoly = Polygon(localOffsets=localOffsets,pos=startPos, color=P1_COLOR, width=0, normals_length=0, velo=[0,0], mass=1, angle=0, momentInertia=1 )
    
    ledgeOffsets=[
        [-400,0],
        [-400,-100],
        [400,-100],
        [400,400]
    ]
    ledge= Polygon(localOffsets=ledgeOffsets,pos=[400,600], color=const.GREEN, width=0, normals_length=0, velo=[0,0], mass=1, angle=0, momentInertia=1 )
    #vertical walls:
    walls.append(Wall( [0,200], [0,0] , const.BLACK))
    walls.append(Wall( [800,0] , [800,200], const.BLACK))
    #Horizontal walls:
    #walls.append(Wall( [0,0] , [800,0], const.BLACK))
    #walls.append(Wall( [800,600],[0,600], const.BLACK))

    #triangle
    shape1Offsets= [
        [0,0],
        [20,-40],
        [40,0]
    ]
    #square
    shape2Offsets= [
        [0,0],
        [0,-40],
        [40,-40],
        [40,0]
    ]
    #rombus
    shape3Offsets= [
        [0,0],
        [20,-40],
        [60,-40],
        [40,0]
    ]
    #long rect
    shape4Offsets= [
        [0,0],
        [0,-40],
        [20,-40],
        [20,0]
    ]
    #pentagon
    shape5Offsets= [
        [0,0],
        [0,-40],
        [20, -50],
        [40,-40],
        [40,0]
    ]

    #localOffsets=list(reversed(shape1Offsets))
    shape1= Shape(listOffsets=shape1Offsets, color=const.WIND_COLOR)
    shape2= Shape(listOffsets=shape2Offsets, color=const.ORANGE)
    shape3= Shape(listOffsets=shape3Offsets, color=const.PINK)
    shape4= Shape(listOffsets=shape4Offsets, color=const.LIGHT_GREEN)
    shape5= Shape(listOffsets=shape5Offsets, color=const.WHITE)

    shapesByScore=[shape1, shape2, shape3, shape4,shape5]

    forces.append(Friction(const.FRICTION_G, const.MEW, objects=[playerPoly]))

    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    startTime= time.time()



def ShootBall():
    global bullets
    global playerPoly
    global shootingCD
    global firingRate 
    global deltaTime
    bulletForce= [0,-1000]
    tipOffset= pygame.Vector2(20,-40)
    shootingCD+=deltaTime
    bulletMass = 1 * 3.14 * 12 #Circles mass should be the same density as the polygons
    if(shootingCD >=  firingRate):
        bullets.append(Circle( mass=bulletMass, radius=12, color=const.YELLOW, width=0, angle=0, angularVel=0, momentInertia=1, velo=bulletForce, pos=playerPoly.pos + tipOffset))
        shootingCD=0



def DropShapeFromSky(currScore):
    global objects
    global dropRate
    global timeSinceLastDrop  
    global deltaTime
    global shapesByScore

    timeSinceLastDrop+= deltaTime
    if(timeSinceLastDrop >= dropRate):
        #print("dropItem")
        timeSinceLastDrop=0
        shape = GetRandomShape(currScore, shapesByScore)
        #shape.pos = GetRandomPosOffScreen()
        objects.append(shape)
    dropRate = AdjustForScore(currScore)

StartGame()

stage=1
turnMessage="shoot the asteroids off screen"
RUNNING=True;
SHOW_MESSAGE=True
event1 = pygame.USEREVENT;

stagePos = [10 , 550]
titlePos = [250 , 510]
score1Pos=  [screen.get_width() - 20, 500]
CURR_COLOR=P1_COLOR

ball_shoot_force = pygame.math.Vector2(1)
ball_shoot_dir = pygame.Vector2(0, 1)
CHARGE_RATE = 10
STOPWEIGHT= -const.MEW * const.FRICTION_G * deltaTime
pointScore= 0
READ_FOR_PLAY_AGAIN=False;

shapesOnScreen=[]


while RUNNING :
    mouseCurr=pygame.math.Vector2(pygame.mouse.get_pos())
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
        if e.type ==event1:
            READ_FOR_PLAY_AGAIN=True;
        if e.type == pygame.MOUSEBUTTONUP and e.button ==1 and pygame.display.get_active(): 
                if READ_FOR_PLAY_AGAIN:
                    StartGame();
   
    stage = (int) (pointScore /100)
    DropShapeFromSky(pointScore)
    playerPoly.clearForce()
    playerMoveDir= pygame.Vector2(0)
    moveAmnt= 120;
    keys= pygame.key.get_pressed()
    if(keys[pygame.K_LEFT]):
       playerMoveDir+= pygame.Vector2(-moveAmnt,0)
    if(keys[pygame.K_RIGHT]):
        playerMoveDir+= pygame.Vector2(moveAmnt,0)
    if(keys[pygame.K_SPACE]):
        ShootBall()

    playerPoly.velo = (playerMoveDir)
    playerPoly.addForce(playerMoveDir) #trying to add extra force ontop of velo change doesnt seem to work

    playerPoly.update(deltaTime)

    restitution=1
    #collisions
    for w in walls:
        c= detectContact(playerPoly, w, restitution=restitution)
        if(c.isColliding()):
            c.resolve();

    staleShapes = []
    for o in objects :
        o.update(deltaTime)
        #print( OnScreen(o))
        if(not shapesOnScreen.__contains__(o) and OnScreen(o)):
            shapesOnScreen.append(o)
            #print("added shape on OnScreen")
        elif (shapesOnScreen.__contains__(o)):
            if(not OnScreen(o)):
                changeInPoints=0
                if(IsOffScreenHoriz(o)):  #check if it left horiz
                    changeInPoints = 0
                elif(IsOffScreenTop(o) ):  #check if left up (add point)
                    changeInPoints= o.value
                elif(IsOffScreenBot(o) ): #check if if hit ground (lose point)
                    changeInPoints = 0 - o.value
                pointScore += changeInPoints
                staleShapes.append(o)
                #print(f" {o.worldPoints} change in points = {changeInPoints} pos= {o.pos} hor={IsOffScreenHoriz(o)} , {IsOffScreenTop(o)} , {IsOffScreenBot(o)}")
        c= detectContact(playerPoly, o, restitution=restitution)
        if(c.isColliding()):
            c.resolve();
        for j in objects:
            if(not j == o):
                objCol= detectContact(j, o, restitution=restitution)
                if(objCol.isColliding()):
                    objCol.resolve();

    staleBullets=[]
    for b in bullets:
        wasStale=False
        b.update(deltaTime)
        for o in objects:
            c = detectContact(b,o, restitution=restitution)
            if(c.isColliding()):
                c.resolve();
                #staleBullets.append(b) #dont remove collided bullets, let them bounce
                wasStale=True
        #out of bounds check
        if(wasStale==False and (b.pos.y < 0 or b.pos.y >= 500)): #off screen or hit ground
            staleBullets.append(b)

    for sb in staleBullets:
        bullets.remove(sb)
    for ss in staleShapes:
        objects.remove(ss)


    #Figure out text
    stageTxt= tileFont.render(f"{stage}", True, CURR_COLOR)
    text = tileFont.render(f"{turnMessage}",True, CURR_COLOR) #Isn't on screen yet
    score1Text= tileFont.render(f"{pointScore}",True, P1_COLOR) #Isn't on screen yet
    score1Pos=  [screen.get_width() - 50 - len(str(pointScore)), 500]
    #REDRAW SCREEN
    screen.fill(const.BLACK) #erase screen 

    ledge.draw(screen)
    playerPoly.draw(screen)
    for b in bullets:
        b.draw(screen)
    for o in objects:
        o.draw(screen) 

    screen.blit(stageTxt, stagePos)
    screen.blit(text, titlePos)
    screen.blit(score1Text, score1Pos)
    #Update the Screen to show what we drew
    pygame.display.update();
    clock.tick(fps);