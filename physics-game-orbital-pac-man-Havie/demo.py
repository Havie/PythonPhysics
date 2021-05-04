import pygame
from circle import Circle
from asteroidCreator import AsteroidCreator
from globalFunctions import *

screenBounds=[600,600]
screen = pygame.display.set_mode(screenBounds);

fps = 60
deltaTime= 1/fps
clock = pygame.time.Clock()


sun=  Circle(pos=[300,300] , velo=[0,0], mass=2000, color=[215,215,50] , radius = 30)
ship = Circle(pos=GetPosForValidDistanceFromPos([300,300], 250) , velo=[0,0], mass=250, color=[0,192,255] , radius = 10)
ac = AsteroidCreator(10, [255,255,255], screenBounds)
TESTCIRCLE=  Circle(pos=[125,50] , velo=[0,0], mass=200, color=[255,15,50] , radius = 5)
objects =ac.CreateAsteroids()

RUNNING=True;

while RUNNING :
    #EventLOOP
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            RUNNING=False
    #DO Physics
    ## clear forces on all particles 
    ship.clearForce()
    for o in objects:
        o.clearForce()



    #Move the player circle
    keys= pygame.key.get_pressed()
    if(keys[pygame.K_LEFT]):
        ship.addForce([-1000,0])
    if(keys[pygame.K_RIGHT]):
        ship.addForce([1000,0])
    if(keys[pygame.K_DOWN]):
        ship.addForce([0,1000])
    if(keys[pygame.K_UP]):
        ship.addForce([0,-1000])



    toRemove=[]
    ##Add all the forces on the objects 
    for o in objects:
        #g=GetGravityForce(sun.mass, o.mass,DisX(sun.pos, o.pos), DisY(sun.pos, o.pos))
        #need to make it in the direction of [300,300]...?
        #print(f"the gravity is : {g}")
        #o.addForce(g) # gravity

        if (CheckCollision(o.pos, ship.pos, o.radius, ship.radius)):   ## COLLISION: Check dis between 2 obj is less than sum of 2 radius ? 
           toRemove.append(o);
           print("colliisoon w ship")
           

        #if(o.pos[1] + o.radius > yBoundary):
        #    force = 1000 * (yBoundary - o.pos[1] + o.radius)  #sqrt (k/m) ?? idk 
        #    o.addForce([0, force])

    
    for collidedItem in toRemove:
        objects.remove(collidedItem)
    
    #if (CheckCollision(TESTCIRCLE.pos, ship.pos, TESTCIRCLE.radius, ship.radius)):   ## COLLISION: Check dis between 2 obj is less than sum of 2 radius ? 
    #    print("colliisoon w ship")
     


    ##Update the positions and velocities 
    TESTCIRCLE.update(deltaTime)
    ship.update(deltaTime)
    for o in objects:
        o.update(deltaTime)



    #Draw Stuff
    screen.fill([0,0,0]) #erase screen 
    #pygame.draw.line(screen, [127,128,128], [0, yBoundary], [800,yBoundary])
    TESTCIRCLE.draw(screen);
    sun.draw(screen)
    ship.draw(screen)
    for o in objects:
        o.draw(screen)  #draw all objs 

    #Update the Screen to show what we drew
    pygame.display.update();

    clock.tick(fps);
