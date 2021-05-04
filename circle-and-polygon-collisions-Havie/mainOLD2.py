import pygame
from globalFunctions import *
import constVars as const
import numpy as np
import time
from Gravity import *
from RepulsiveForce import *
from Chain import *
from AirDrag import *
from circle import *

screenBounds=[800,600]
screen = pygame.display.set_mode(screenBounds);

fps = 60
deltaTime= 1/fps
clock = pygame.time.Clock()





global objects
global pairs
global wind
global forces
global RUNNING
global PAUSED
global ONETIME
global TEST

def StartGame():
    global objects
    global pairs
    global wind
    global forces
    global RUNNING
    global PAUSED
    global ONETIME
    global TEST
    objects=[]
    forces = []

    rad=const.SPHERE_RADIUS
    #objects.append(Circle(rad, color=const.DARK_GRAY, width= 0, pos=[400,100], velo=[0,0], mass=math.inf))
    firstBall=Circle(rad, color=const.DARK_GRAY, width= 0, pos=[400,100], velo=[0,0], mass=math.inf)
    objects.append(Circle(rad, color=const.ORANGE,  width=0, pos=[400,200], velo=[0,0], mass=const.REALISTIC_MASS))
    objects.append(Circle(rad, color=const.YELLOW, width= 0, pos=[400,300], velo=[0,0], mass=const.REALISTIC_MASS))
    objects.append(Circle(rad, color=const.GREEN, width= 0, pos=[400,400], velo=[0,0], mass=const.REALISTIC_MASS))
    objects.append(Circle(rad, color=const.PINK, width= 0, pos=[400,500], velo=[0,0], mass=const.REALISTIC_MASS))
                                                                               
    forces.append(Gravity(objects=objects.copy(), acc = [0, 9.8* const.MM_TO_PX]))
    wind = AirDrag(windVel=[0,0], objects=objects.copy())
    forces.append(wind)

    pairs =[]
    firstPair=[firstBall,objects[0]]
    pairs.append(firstPair)
    for i in range(len(objects)):
        if(i < len(objects)-1):
            obj1= objects[i]
            obj2= objects[i+1]
            pairs.append([obj1, obj2])

    
   
    forces.append(Chain(k=const.SPRING_FORCE, naturalLen=const.NATURAL_LENGTH, damp=const.DAMPENING, pair=pairs))

    #Add our Infinite mass circle after Forces:
    objects.append(firstBall)
    forces.append(Repulsion(k=const.SPRING_FORCE, objList=objects.copy(), pair=pairs))

    RUNNING=True;
    PAUSED=False;
    GAMEOVER=False;
    READ_FOR_PLAY_AGAIN=False;
    startTime= time.time()


StartGame()

while RUNNING :
    mousePrev=mouseCurr
    mouseCurr=pygame.math.Vector2(pygame.mouse.get_pos())
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE and not READ_FOR_PLAY_AGAIN:
                 PAUSED= not PAUSED # toggles pause
                 if ONETIME: #Turns off the initial welcome message from occuring again 
                     ONETIME=False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button ==1 and pygame.display.get_active(): 
                print(f"CLIKCD MOUSE@: {mouseLoc}");




    for o in objects:
        o.clearForce()


    for f in forces:
        f.apply();


    for o in objects:
        o.update(deltaTime)

    #detect and resolve contacts:
    #for a, b in iterTools : 
        #contact(a,b).resolve(restituion=1)


    screen.fill(const.LIGHT_BLUE) #erase screen 
    #draw chains behind spheres:
    for a,b in pairs:
        pygame.draw.line(screen, const.BLACK, a.pos , b.pos,1)
    #draws all objs 
    for o in objects:
        o.draw(screen) 



    #Update the Screen to show what we drew
    pygame.display.update();
    clock.tick(fps);
