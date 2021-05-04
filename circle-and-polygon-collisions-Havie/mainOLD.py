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
global grayCircle
global forces
global walls
global RUNNING
global PAUSED
global ONETIME
global TEST
global tm;
global currentBallToBeThrown;
global pallino 
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
    global grayCircle
    global forces
    global walls
    global RUNNING
    global PAUSED
    global ONETIME
    global TEST
    global tm;
    global currentBallToBeThrown;
    global pallino
    global stage 
    global placedBallPos
    objects=[]
    walls = []
    forces = []

    rad=const.SPHERE_RADIUS
    grayCircle=Circle(100, color=const.LIGHT_GRAY, width= 0, pos=[100,100], velo=[0,0], mass=math.inf)
    currentBallToBeThrown=Circle(rad, color=const.WHITE, width= 0, pos=[100,100], velo=[0,0], mass=const.BALL_MASS)
    pallino=currentBallToBeThrown

    
    walls.append(Wall( [0,600], [0,0] , const.BLACK))
    walls.append(Wall( [800,0] , [800,600], const.BLACK))
    walls.append(Wall( [0,0] , [800,0], const.BLACK))
    walls.append(Wall( [800,600],[0,600], const.BLACK))

    forces.append(Friction(const.FRICTION_G, const.MEW, objects=objects))

    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    startTime= time.time()
    tm.StartGame();

def NextRound():
    global objects
    global grayCircle
    global forces
    global RUNNING
    global PAUSED
    global ONETIME
    global TEST
    global tm;
    global currentBallToBeThrown;
    global pallino
    global stage  
    global BALLS_AIMING 
    global placedBallPos    
    objects=[]
    forces = []

    rad=const.SPHERE_RADIUS
    StartPos= GetRandomStartPos()
    grayCircle=Circle(100, color=const.LIGHT_GRAY, width= 0, pos=StartPos, velo=[0,0], mass=math.inf)
    currentBallToBeThrown=Circle(rad, color=const.WHITE, width= 0, pos=StartPos, velo=[0,0], mass=const.BALL_MASS)
    pallino=currentBallToBeThrown
    placedBallPos = pallino.pos
    forces.append(Friction(const.FRICTION_G, const.MEW, objects=objects))

    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    stage=BALLS_AIMING
    tm.StartGame();

StartGame()

score1=0
score2=0
turnMessage="Someone throw the pallino"
RUNNING=True;
SHOW_MESSAGE=True
event1 = pygame.USEREVENT;
FigureOutWhosTurnItIs=False;

titlePos = [screen.get_width()/2 , 10]
score1Pos=  [10, 10]
score2Pos=  [screen.get_width()-20, 10]
CURR_COLOR=P1_COLOR

placedBallPos= pygame.Vector2(100,100)

ball_shoot_force = pygame.math.Vector2(1)
ball_shoot_dir = pygame.Vector2(0)
CHARGE_RATE = 10
STOPWEIGHT= -const.MEW * const.FRICTION_G * deltaTime
rollingBall= None
closestBall_P1= None;
closestBall_P2= None;
pointScore=0
READ_FOR_PLAY_AGAIN=False;
def GetCommandNameHack(command):
    if(command == BALLS_STOPPED):
        return "place the ball in the zone"
    if(command == BALLS_AIMING):
        return "shoot the ball"
    if(command == BALLS_CHARGING):
        return "is charging up"
    if(command == BALLS_ROLLING):
        return "..nice shot!"
    if(command == ROUND_END):
        return "ROUND_END"
    if(command == WAITING):
        return f"scored {pointScore} points!"

while RUNNING :
    mouseCurr=pygame.math.Vector2(pygame.mouse.get_pos())
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
        if e.type ==event1:
            READ_FOR_PLAY_AGAIN=True;
        if (e.type == pygame.KEYUP) or (e.type == pygame.MOUSEBUTTONUP and e.button ==2):
            if READ_FOR_PLAY_AGAIN:
                READ_FOR_PLAY_AGAIN=False;
                NextRound();
        elif e.type == pygame.MOUSEBUTTONUP and e.button ==1 and pygame.display.get_active(): 
                if READ_FOR_PLAY_AGAIN:
                    READ_FOR_PLAY_AGAIN=False;
                    NextRound();
                elif stage == BALLS_STOPPED:
                    #print("check in range of gray circle");
                    if(CheckCollision(mouseCurr, grayCircle.pos, 5, grayCircle.radius)):
                        #print("Clicked in gray circle during ball placement mode")
                        placedBallPos=mouseCurr;
                        currentBallToBeThrown=(InstantiateBall(radius = const.SPHERE_RADIUS, pos=placedBallPos,color= tm.WhosTurnColor()))
                        tm.BallPlaced(currentBallToBeThrown)
                        stage= BALLS_AIMING
                elif stage == BALLS_CHARGING:
                        if(len(objects)>0):
                            FigureOutWhosTurnItIs=True;

                        objects.append(currentBallToBeThrown);#might clear force too soon??
                        currentBallToBeThrown.addForce(ball_shoot_force)
                        rollingBall=currentBallToBeThrown
                        stage= BALLS_ROLLING;

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button ==1 and pygame.display.get_active(): 
                if stage == BALLS_AIMING:
                    #print("Begin AIM ");
                    stage= BALLS_CHARGING
   
               
    
    if stage != WAITING :   
        for o in objects:
            if(o==currentBallToBeThrown):
                currentBallToBeThrown=None; #strange hack to prevent goofy frame 1 changes
            else:
                o.clearForce();




        #collisions
        for o in objects:
            for w in walls :
                #if(rollingBall==o):
                #    print(f"checking collision between rolling ball and {w}")
                c= detectContact(o,w, restitution=0.3)
                if(c.isColliding()):
                    #print(f"We think theres a colliison WALLS" , c.overlap, c.normal)
                    c.resolve();

        for a,b in itertools.combinations(objects, 2):
            if(a!=None and b!=None):
                c= detectContact(a,b,restitution=0.5)
                if(c.isColliding()): #overloaded bool operator for collision
                    #print(f"We think theres a colliisonw balls" , c.overlap, c.normal, a.velo, b.velo)
                    c.resolve();

        for f in forces:
            f.apply();

    
        # HAVE TO CHANGE TO ALL BALLS >.< 
        if(stage == BALLS_ROLLING ):
            BallsRolling=False
            for o in objects:
                #print(f"ball mag= {o.velo.magnitude()} vs {STOPWEIGHT}")
                velo=o.velo.magnitude()
                if(velo > STOPWEIGHT):
                    BallsRolling=True;
                    if(o==rollingBall):
                        rollingBall=None # hack when only 1 ball *starts* moving, something wfirst frame still having mag=0
                elif(velo!=0):
                    o.clearForce()
                    o.velo=pygame.math.Vector2(0)
                    #print("trying to stop a ball")
                elif(o==rollingBall):
                    BallsRolling=True; # hack when only 1 ball *starts* moving, something wfirst frame still having mag=0
            if(BallsRolling==False):
                stage = BALLS_STOPPED
                #FIND CLOSEST BALL FOR EACH TEAM
                #DETERMINE CLOSEST COLOR
                #FIND ALL OTHER BALLS FOR TEAM COLOR CLOSER TO PALLINO THAN CLOSEST BALL ON OTHER TEAM
                # HOLD ON TO THIS # for final scoring if round ends 

                #print("switch to BALLS_STOPPED")

        
            

        for o in objects:
            o.update(deltaTime)



    currCommand=GetCommandNameHack(stage)
    CURR_COLOR= tm.WhosTurnColor()
    turnMessage=(f"{tm.WhosTurnName()} {currCommand}")
    #Figure out text
    text = tileFont.render(f"{turnMessage}",True, CURR_COLOR) #Isn't on screen yet
    titlePos = [screen.get_width()/2 - text.get_width()/2, 10]
    score1Text= tileFont.render(f"{score1}",True, P1_COLOR) #Isn't on screen yet
    score2Text= tileFont.render(f"{score2}",True, P2_COLOR) #Isn't on screen yet
    
    #REDRAW SCREEN
    screen.fill(const.GREEN) #erase screen 
    # Put the image of the text on the screen at a POS
    if stage != BALLS_ROLLING:
        if(SHOW_MESSAGE):
            screen.blit(text, titlePos)
    
    screen.blit(score1Text, score1Pos)
    screen.blit(score2Text, score2Pos)


    #draws all objs 
    grayCircle.draw(screen)
    if(currentBallToBeThrown!=None):
        currentBallToBeThrown.draw(screen)


    #Testing
    for w in walls:
        w.draw(screen) 

    #DRAW CLOSEST BALL HIGHLIGHTS:
    if stage == BALLS_STOPPED or stage == BALLS_AIMING or stage == WAITING:
        if(len(objects) > 2):
            highlightedBalls=[]
            #print("checking to highlight:")
            maxDis1=999999999999
            maxDis2=999999999999
            #FIND CLOSEST BALL FOR EACH TEAM
            for o in objects:
                if(o!=pallino):
                    playerNum= tm.IsPlayersBall(o)
                    dis= (o.pos - pallino.pos).magnitude()
                    if(playerNum==1 and dis <maxDis1):
                        closestBall_P1=o
                        maxDis1=dis
                        #print(f"found a ball for p1 {dis}")
                    if(playerNum==2 and dis <maxDis2):
                        closestBall_P2=o
                        maxDis2=dis
                        #print(f"found a ball for p2 {dis}")

            #Identify the winning Team:
            winningPlayerNum=2
            winningDis=maxDis2
            losingDis= maxDis1;
            if(maxDis1< maxDis2):
                 winningPlayerNum=1
                 winningDis=maxDis1
                 losingDis=maxDis2

            #find other balls closer than the losing players closest ball:
            for o in objects:
                if(o!=pallino):
                    playerNum= tm.IsPlayersBall(o)
                    if(playerNum == winningPlayerNum):
                        dis= (o.pos - pallino.pos).magnitude()
                        #print(f"Find ball for player# {playerNum} , dis = {dis} <? {losingDis} ")
                        if(dis<=losingDis):
                            newBall= InstantiateBall(const.SPHERE_RADIUS +5, o.pos,const.YELLOW)
                            newBall.draw(screen)
                            highlightedBalls.append(newBall);
                            #print(f"draw this ball to highlight for player# {playerNum}")


            # HOLD ON TO THIS # for final scoring if round ends
            pointScore=len(highlightedBalls)


    if stage == BALLS_AIMING :
        #todo figure out projection to limit length of line
        pygame.draw.line(screen, const.BLACK, placedBallPos ,mouseCurr,1)
        ball_shoot_dir= mouseCurr-placedBallPos;
        ball_shoot_force= pygame.math.Vector2(1)#reset charge
        #print(f"LOCKED IN AIM DIR= {ball_shoot_dir} , {ball_shoot_force}")

    if stage == BALLS_CHARGING:
        if(ball_shoot_force.magnitude() < 150000): 
            newForce= pygame.math.Vector2(ball_shoot_dir.x*CHARGE_RATE, ball_shoot_dir.y*CHARGE_RATE)
            #print(f" {ball_shoot_dir}  + {newForce}==> Charing ball force= {ball_shoot_force} ");
            ball_shoot_force+=newForce
        #else:
        #    print(f"Magnitude={ball_shoot_force.magnitude()}")
    
    if(stage == BALLS_STOPPED and FigureOutWhosTurnItIs):
        FigureOutWhosTurnItIs=False;
        TryAdvanceTurn(tm, objects, pallino, closestBall_P1, closestBall_P2);
    #finally draw the balls last:
    for o in objects:
        #print(f"obj is located at: {o.pos}")
        o.draw(screen) 
    
    
    if(tm.IsGameOver() and stage==PLACE_BALL):
        stage=ROUND_END;

    if stage == ROUND_END:
        winningNum=IdentifyWinner(pallino, closestBall_P1, closestBall_P2)
        #print(f"Score earned={pointScore}")
        if(winningNum==0):
            print("TIE!")
        elif(winningNum ==1):
            print("player1 Wins");
            score1+=pointScore
            if(tm.WhosTurnNum() ==2):
                #print("switch turn since p1 isnt turn")
                tm.SwitchTurn();
        else:
            print("player2 Wins");
            score2+=pointScore
            if(tm.WhosTurnNum() ==1):
                tm.SwitchTurn();
                #print("switch turn since p2 isnt turn")

        pygame.time.set_timer(event1, 1000, True) #1000 milisec is 1 sec
        stage = WAITING


    #Update the Screen to show what we drew
    pygame.display.update();
    clock.tick(fps);