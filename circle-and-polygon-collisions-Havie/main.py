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
global puttingGreens
global forces
global walls
global RUNNING
global PAUSED
global ONETIME
global TEST
global tm;
global currentBallToBeThrown;
global golfBall
global endHole
global polygon
global frictionTraps
global waterTraps
global startPos
global extraFriction

global globalBALLS_STOPPED
global BALLS_AIMING 
global BALLS_CHARGING 
global BALLS_ROLLING 
global ROUND_END
global WAITING
global stage  
P1_COLOR = const.ORANGE
P2_COLOR = const.LIGHT_BLUE
tm = TurnManager(P1_COLOR,P2_COLOR)
BALLS_STOPPED = 0
PLACE_BALL = BALLS_STOPPED
BALLS_AIMING = 1
BALLS_CHARGING = 2
BALLS_ROLLING = 3
ROUND_END = 4
WAITING=5
stage = BALLS_AIMING

def StartGame():
    global objects
    global puttingGreens
    global forces
    global walls
    global RUNNING
    global PAUSED
    global ONETIME
    global TEST
    global tm;
    global currentBallToBeThrown;
    global golfBall
    global endHole
    global stage 
    global placedBallPos
    global polygon
    global frictionTraps
    global waterTraps
    global startPos
    global extraFriction
    objects=[]
    walls = []
    forces = []
    waterTraps=[]
    frictionTraps=[]

    thingsToAvoid=[]


    endPos= GetRandomStartPos()
    rad=const.SPHERE_RADIUS
    puttingGreens=Circle(50, color=const.LIGHT_GREEN, width= 0, pos=endPos, velo=[0,0], mass=math.inf)
    endHole=Circle(rad, color=const.BLACK, width= 0, pos=endPos, velo=[0,0], mass=const.BALL_MASS)
    thingsToAvoid.append(endHole);
    thingsToAvoid.append(puttingGreens);
    
    startPos= [700,500]

    currentBallToBeThrown=Circle(rad, color=const.WHITE, width= 0, pos=startPos, velo=[0,0], mass=const.BALL_MASS)
    golfBall=currentBallToBeThrown
    placedBallPos = golfBall.pos
    thingsToAvoid.append(golfBall);
    
    #Spinning obstacles
    for i in range(2):
        polyPos= GetRandomStartPosNoCollisions(thingsToAvoid)
        polygon = MakeARandomPolygon(polyPos)
        polyPos.append(polygon)
        walls.append(polygon);
        thingsToAvoid.append(polygon);
    
    walls.append(Wall( [0,600], [0,0] , const.BLACK))
    walls.append(Wall( [800,0] , [800,600], const.BLACK))
    walls.append(Wall( [0,0] , [800,0], const.BLACK))
    walls.append(Wall( [800,600],[0,600], const.BLACK))

    #water
    offsetsWater=[
        [0,0],
        [10,50],
        [50,100],
        [100,50],
        [50,10],
        [10,0]
        ]

    waterPos=GetRandomStartPosNoCollisions(thingsToAvoid)
    water = Polygon(offsetsWater,pos=waterPos, color=const.LIGHT_BLUE,width=0, normals_length=10, angularVel=0)
    waterTraps.append(water)
    thingsToAvoid.append(water)

    offsetsSand=[
        [0,20],
        [20,160],
        [100,50],
        [50,0]
        ]
    sandPos=GetRandomStartPosNoCollisions(thingsToAvoid)
    sand = Polygon(offsetsSand,pos=sandPos, color=const.BROWN,width=0, normals_length=10, angularVel=0)
    frictionTraps.append(sand)
    thingsToAvoid.append(sand)   
    
    extraFriction=Friction(const.FRICTION_G * 10, const.MEW, objects=[golfBall])
    forces.append(Friction(const.FRICTION_G, const.MEW, objects=[golfBall]))

    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    startTime= time.time()
    tm.StartGame();

def NextRound():
    global RUNNING
    global PAUSED
    global GAMEOVER
    global READ_FOR_PLAY_AGAIN
    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    StartGame()
    global stage
    global pointScore
    stage = BALLS_AIMING
    pointScore=0

StartGame()


turnMessage="shoot the golfBall in the hole"
RUNNING=True;
SHOW_MESSAGE=True
event1 = pygame.USEREVENT;


titlePos = [screen.get_width()/2 , 10]
score1Pos=  [10, 10]
CURR_COLOR=P1_COLOR

placedBallPos= pygame.Vector2(golfBall.pos)

ball_shoot_force = pygame.math.Vector2(1)
ball_shoot_dir = pygame.Vector2(0)
CHARGE_RATE = 10
STOPWEIGHT= -const.MEW * const.FRICTION_G * deltaTime
rollingBall= None
pointScore=0
READ_FOR_PLAY_AGAIN=False;
def GetCommandNameHack(command):
    if(command == BALLS_STOPPED):
        return "Click ur golfball"
    if(command == BALLS_AIMING):
        return "Aim your shot"
    if(command == BALLS_CHARGING):
        return "is charging up"
    if(command == BALLS_ROLLING):
        return "..nice shot!"
    if(command == ROUND_END):
        return "ROUND_END"
    if(command == WAITING):
        return f"took {pointScore} strokes! , click to play Again"


stage = BALLS_AIMING
while RUNNING :
    mouseCurr=pygame.math.Vector2(pygame.mouse.get_pos())
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
        if e.type ==event1:
            READ_FOR_PLAY_AGAIN=True;
        if (e.type == pygame.KEYUP) or (e.type == pygame.MOUSEBUTTONUP and e.button ==2):
            if READ_FOR_PLAY_AGAIN:
                NextRound();
        elif e.type == pygame.MOUSEBUTTONUP and e.button ==1 and pygame.display.get_active(): 
                if READ_FOR_PLAY_AGAIN:
                    NextRound();
                elif stage == BALLS_STOPPED:
                    #print("check in range of gray circle");
                    if(CheckCollision(mouseCurr, golfBall.pos, 5, golfBall.radius)): #
                        #print("Clicked in gray circle during ball placement mode")
                        currentBallToBeThrown=golfBall;
                        stage= BALLS_AIMING
                elif stage == BALLS_CHARGING:
                        #print(f"Added force= {ball_shoot_force} ")
                        golfBall.addForce(ball_shoot_force)
                        golfBall.update(deltaTime)
                        rollingBall=golfBall
                        stage= BALLS_ROLLING;
                        pointScore= pointScore+1

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button ==1 and pygame.display.get_active(): 
                if stage == BALLS_AIMING:
                    #print("Begin AIM ");
                    stage= BALLS_CHARGING
   

    #print(stage)   
    golfBall.clearForce();
    if stage != WAITING : 
        endCollision=detectContact(endHole, golfBall,  restitution=0.3)
        if(endCollision.isColliding()):
            # figure out if balls velo is too high to sink in gently:
            speed= golfBall.getVelocity().magnitude();
            #print(speed)
            if(speed < 100):
                #the balls the same size as the hole, so if their pos is the same, they are completely overlapping, with a bit of grace
                if( (endHole.pos - golfBall.pos).magnitude() < 5):
                    print("GAME WON");
                    pygame.time.set_timer(event1, 1000, True) #1000 milisec is 1 sec
                    print("Set Waiting:")
                    stage = WAITING
            #add a force towards the center of hole:
            if(speed!=0):
                displacement = golfBall.pos - endHole.pos
                displacement= displacement.normalize()
                golfBall.addForce(displacement)

        #collisions
        for w in walls :
            #if(rollingBall==o):
            #print(f"checking collision between rolling ball and {w}")
            c= detectContact(golfBall,w, restitution=0.3)
            if(c.isColliding()):
                #print(f"We think theres a colliison WALLS" , c.overlap, c.normal)
                c.resolve();

        for trap in frictionTraps:
            c= detectContact(golfBall,trap, restitution=0.5)
            if(c.isColliding() and (golfBall.velo.magnitude() > 10)):
                #print("slow ball down")
                extraFriction.apply()

        for wTrap in waterTraps:
            c= detectContact(golfBall,wTrap, restitution=0.3)
            if(c.isColliding()):
                #print("resetBall")
                golfBall.clearForce();
                golfBall.clearVelo();
                golfBall.setPos(startPos);

        for f in forces:
            f.apply();

        if( (golfBall.velo.magnitude() > 10)):
            stage == BALLS_ROLLING

        if(stage == BALLS_ROLLING ):
            BallsRolling=False
            #print(f"ball mag= {golfBall.velo.magnitude()} vs {STOPWEIGHT}")
            velo=golfBall.velo.magnitude()
            if(velo > STOPWEIGHT):
                BallsRolling=True;
                if(golfBall==rollingBall):
                    rollingBall=None # hack when only 1 ball *starts* moving, something wfirst frame still having mag=0
            elif(velo!=0):
                golfBall.clearForce()
                golfBall.velo=pygame.math.Vector2(0)
                #print("trying to stop a ball")
            elif(golfBall==rollingBall):
                BallsRolling=True; # hack when only 1 ball *starts* moving, something wfirst frame still having mag=0
            
            if(BallsRolling==False):
                stage = BALLS_STOPPED
            #FIND CLOSEST BALL FOR EACH TEAM
            #DETERMINE CLOSEST COLOR
            #FIND ALL OTHER BALLS FOR TEAM COLOR CLOSER TO golfBall THAN CLOSEST BALL ON OTHER TEAM
            # HOLD ON TO THIS # for final scoring if round ends 

            #print("switch to BALLS_STOPPED")

        
            

        golfBall.update(deltaTime)
        #i dont think we need to do these?
        for w in walls:
            w.update(deltaTime)
        for f in frictionTraps:
            f.update(deltaTime)
        for w2 in waterTraps:
            w2.update(deltaTime)



    currCommand=GetCommandNameHack(stage)
    CURR_COLOR= tm.WhosTurnColor()
    turnMessage=(f"{tm.WhosTurnName()} {currCommand}")
    #Figure out text
    text = tileFont.render(f"{turnMessage}",True, CURR_COLOR) #Isn't on screen yet
    titlePos = [screen.get_width()/2 - text.get_width()/2, 10]
    score1Text= tileFont.render(f"{pointScore}",True, P1_COLOR) #Isn't on screen yet
    
    #REDRAW SCREEN
    screen.fill(const.GREEN) #erase screen 
    # Put the image of the text on the screen at a POS
    if stage != BALLS_ROLLING:
        if(SHOW_MESSAGE):
            screen.blit(text, titlePos)
    
    screen.blit(score1Text, score1Pos)


    puttingGreens.draw(screen)
    if(currentBallToBeThrown!=None):
        currentBallToBeThrown.draw(screen)
    
    #Contains polygons
    for w in walls:
        w.draw(screen) 
    for f in frictionTraps:
        f.draw(screen)
    for w2 in waterTraps:
        w2.draw(screen)

    if stage == BALLS_AIMING :
        #todo figure out projection to limit length of line
        pygame.draw.line(screen, const.BLACK, golfBall.pos ,mouseCurr,1)
        ball_shoot_dir= mouseCurr-golfBall.pos;
        ball_shoot_force= pygame.math.Vector2(1)#reset charge
        #print(f"LOCKED IN AIM DIR= {ball_shoot_dir} , {ball_shoot_force}")

    if stage == BALLS_CHARGING:
        if(ball_shoot_force.magnitude() < 150000): 
            newForce= pygame.math.Vector2(ball_shoot_dir.x*CHARGE_RATE, ball_shoot_dir.y*CHARGE_RATE)
            #print(f" {ball_shoot_dir}  + {newForce}==> Charing ball force= {ball_shoot_force} ");
            ball_shoot_force+=newForce
        #else:
        #    print(f"Magnitude={ball_shoot_force.magnitude()}")
    
    if(stage == BALLS_STOPPED):
        stage=BALLS_AIMING # Hack to skip over ball selection
        

    endHole.draw(screen)
    golfBall.draw(screen)


    #Update the Screen to show what we drew
    pygame.display.update();
    clock.tick(fps);