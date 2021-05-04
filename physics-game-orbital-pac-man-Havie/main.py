import pygame
from circle import Circle
from asteroidCreator import AsteroidCreator
from globalFunctions import *
import numpy as np
import time
import constVars as const


screenBounds=[600,600]
screen = pygame.display.set_mode(screenBounds);

fps = 60
deltaTime= 1/fps
clock = pygame.time.Clock()
global startTime
startTime= time.time()
elapsedTime =0

pygame.init()
pygame.font.init()
msgFont = pygame.font.SysFont('Calibri', size=25, bold=False, italic=True)
textPos=[300,300]

sun = Circle(pos=[300,300] , velo=[0,0], mass=const.SUN_MASS, color=[215,215,50] , radius = 30)
shipStartPos= GetPosForValidDistanceFromPos(sun.pos, 250)
shipStartingVelo= GetStartingVelo(shipStartPos, sun.pos)
thruster= Circle(pos=[300,300] , velo=[0,0], mass=const.SUN_MASS, color=[215,215,50] , radius = 5)
global ship
global ac
global objects
global exObjects
global RUNNING
global PAUSED
global ONETIME
global GAMEOVER
global PLAYERWON
global PLAY_AGAIN
global READ_FOR_PLAY_AGAIN
global TEST

#Starts the game from scratch
def StartGame():

    global ship
    global ac
    global objects
    global exObjects
    global RUNNING
    global GAMEOVER
    global PLAYERWON
    global PLAY_AGAIN
    global READ_FOR_PLAY_AGAIN
    global startTime
    #print(f"ShipStartingVelo={shipStartingVelo}")
    ship = Circle(pos= shipStartPos, velo=shipStartingVelo, mass=1, color=[0,192,255] , radius = 10)
    ship.startPos= shipStartPos
    ship.startVelo = shipStartingVelo
    ac = AsteroidCreator(10, [255,255,255],1,5, screenBounds)
    objects = ac.CreateAsteroids()
    objects.append(ship)
    exAx=AsteroidCreator(5, [100,120,120],1,10, screenBounds)
    exObjects = exAx.CreateAsteroids()
    RUNNING=True;
    GAMEOVER=False;
    PLAYERWON=False;
    READ_FOR_PLAY_AGAIN=False;
    startTime= time.time()


StartGame()
PLAY_AGAIN= pygame.USEREVENT
PAUSED=True;
ONETIME=True;
TEST=False
SHOWTHRUST=False

while RUNNING :
    #EventLOOP
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE and not READ_FOR_PLAY_AGAIN:
                 PAUSED= not PAUSED # toggles pause
                 if ONETIME: #Turns off the initial welcome message from occuring again 
                     ONETIME=False
            if READ_FOR_PLAY_AGAIN:
                if e.key ==  pygame.K_y or e.key==  pygame.K_SPACE:
                    #print("restart")
                    StartGame() #Restarts the game 
                elif e.key ==  pygame.K_n or e.key == pygame.K_ESCAPE:
                     RUNNING=False;

        elif e.type == PLAY_AGAIN: #prompts user to play again 
           READ_FOR_PLAY_AGAIN=True;
           #print(f"SET READ_FOR_PLAY_AGAIN {READ_FOR_PLAY_AGAIN}")

    #displays the Paused message
    if PAUSED:
        text = msgFont.render("Paused", True, [15,255,0]) #Isn't on screen yet
        textPos=[300,10]

    #Displays the starting message 
    if ONETIME:
        text = msgFont.render("Press Space to Start", True, [255,0,0]) #Isn't on screen yet


    if not PAUSED :
        
        skipPhysics= not pygame.key.get_focused()

        if skipPhysics:
            continue

        #DO Physics
        ## clear forces on all particles 
        for o in objects:
            o.clearForce()

        for o in exObjects:
            o.clearForce()

        if (not GAMEOVER):
            #Move the player circle
            keys= pygame.key.get_pressed()

            shipDir= np.array([0,0])
            acc= 20;
            #TODO:thrust on the ship that provides an acceleration of 20 pix/s/s.  make it 20 if ship mass is 1
            #normalize the direction vectors then * 20 
            if(keys[pygame.K_LEFT]):
                shipDir += np.array([-1, 0])
            if(keys[pygame.K_RIGHT]):
                shipDir += np.array([1, 0])
            if(keys[pygame.K_DOWN]):
                shipDir += np.array([0, 1])
            if(keys[pygame.K_UP]):
                shipDir += np.array([0, -1])


        #normalize
        if(shipDir[0]!=0 or shipDir[1] !=0):
            thruster.pos = ship.pos - Normalize(shipDir) * ship.radius
            SHOWTHRUST=True;
            ship.addForce(Normalize(shipDir)*acc)
            #print(f"NormalizedDir={Normalize(shipDir)}")
        else : 
            SHOWTHRUST=False

        toRemove=[]
        ##Add all the forces on the objects 
        for o in objects:
            #g=GetGravityForce(sun.mass, o.mass,DisX(sun.pos, o.pos), DisY(sun.pos, o.pos), Distance(sun.pos, o.pos))
            g= GetGravityForceNew(sun, o )
            #print(f"the gravity is : {g}")
            o.addForce(g) # gravity

            if o!= ship and (CheckCollision(o.pos, ship.pos, o.radius, ship.radius)):   # COLLISION: Check dis between 2 obj is less than sum of 2 radius
               toRemove.append(o);
               #print("collison w ship")
            if o == ship and (CheckCollision(o.pos, sun.pos, o.radius, sun.radius)):
                GAMEOVER=True;
                PLAYERWON=False;
                pygame.time.set_timer(PLAY_AGAIN, 1000, True) #begin play again prompt in  1 sec
                toRemove.append(o);
                #print("collison w sun")
            if o == ship:
               for ex in exObjects: # EXTRA CREDIT objects
                    g= GetGravityForceNew(sun, ex )
                    ex.addForce(g) # gravity
                    if (CheckCollision(ex.pos, ship.pos, ex.radius, ship.radius)):
                        GAMEOVER=True;
                        PLAYERWON=False;
                        pygame.time.set_timer(PLAY_AGAIN, 1000, True) #begin play again prompt in  1 sec
                        toRemove.append(o);

     
        #Remove any items we no longer need to process 
        for collidedItem in toRemove:
            #print("removed ship")
            objects.remove(collidedItem)

        #Player collected all the asteroids 
        if(len(objects) == 1) and objects[0] == ship :
            GAMEOVER =True;
            PLAYERWON = True;
            pygame.time.set_timer(PLAY_AGAIN, 1000, True) #1000 milisec is 1 sec

        ##Update the positions and velocities 
        for o in objects:
            o.update(deltaTime)
        for o in exObjects:
            o.update(deltaTime)


        #Begin to ReDraw this frame
        screen.fill([0,0,0]) #erase screen 
        
        sun.draw(screen)


        #draws all objs 
        for o in objects:
            o.draw(screen)  
        for o in exObjects:
            o.draw(screen)  
        
        #Display the green navigation line if player off screen:
        if(ship.pos[0] > 600 or ship.pos[0] < 0 or ship.pos[1] > 600 or ship.pos[1] < 0):
            pygame.draw.line(screen, [0,255,0], sun.pos,ship.pos,1)
    
        if SHOWTHRUST :
            thruster.draw(screen)

        #Displays the game timer to screen
        if not GAMEOVER:
            elapsedTime= "{:.2f}".format(time.time() - startTime)
        text =  msgFont.render(elapsedTime, True, [255,0,0]) #Isn't on screen yet
        textPos=[10,10]
        screen.blit(text, textPos) #puts it on the screen 

        # A debug hack to draw the starting velocity to screen:
        if(TEST):
            for o in objects:
                pygame.draw.circle(screen, [155,155,155], [int(o.startPos[0]), int(o.startPos[1])], 1, 0);
                pygame.draw.line(screen, [0,255,0], (o.startPos),(o.startPos + o.startVelo),1)
            PAUSED=True
            TEST=False

    if GAMEOVER:
        if PLAYERWON:
            endText = msgFont.render("Player Won!", True, [12,250,0]) #Isn't on screen yet
        else:
            endText = msgFont.render("Player Lost!", True, [222,50,0]) #Isn't on screen yet
        screen.blit(endText, [200,0]) #puts it on the screen 


    if READ_FOR_PLAY_AGAIN:
        endText = msgFont.render("Play Again? (Y/N)", True, [12,50,250]) #Isn't on screen yet
        screen.blit(endText, [200,30]) #puts it on the screen 



    #Update the Screen to show what we drew
    screen.blit(text, textPos) #puts text on the screen 
    pygame.display.update();
    clock.tick(fps);
