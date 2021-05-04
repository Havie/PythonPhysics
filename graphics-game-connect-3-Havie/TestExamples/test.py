#import pygame 
from pygame import *
#https://www.pygame.org/docs/ref/display.html


WHITE= [255,255,255]
BLACK= [0,0,0]
GREENISH=  [155,200,100]
REDISH =  [255,10,80]
bgColor = GREENISH

init() #pygame function


#create window 
screen = display.set_mode([800,600])

#create a clock
clock = time.Clock() 
#create font object
tileFont = font.SysFont('Calibri', size=35, bold=True, italic=False)
msgFont = font.SysFont('Calibri', size=25, bold=False, italic=True)
#Screen.get_width() is also a thing 

# Render the text. "True" means anti-aliased text.
# Note: This line creates an image of the letters,
# but does not put it on the screen yet.
#text = font.render("My text",True,BLACK)

RUNNING=True
mouse.set_visible(False)
textPos = [400, 300]
circlePos = [400, 300]
active = True
SHOW_MESSAGE=False
# Game Loop 
while RUNNING : 
    #loop thru all new events
    for e in event.get():
        if e.type == QUIT:
            RUNNING=False
        elif e.type ==KEYUP and e.key==K_ESCAPE:
            time.set_timer(USEREVENT, 1000) #1000 milisec is 1 sec
            SHOW_MESSAGE=True
        elif e.type == USEREVENT:
            SHOW_MESSAGE=False
        elif e.type == MOUSEBUTTONUP and e.button ==1 and display.get_active(): 
            circlePos=e.pos #move the circle to where we click
        elif e.type == KEYUP :
            if e.key == K_SPACE:
                if bgColor == GREENISH:
                    bgColor = WHITE
                elif bgColor == WHITE:
                    bgColor = GREENISH
        elif e.type == MOUSEMOTION:
            pass
        elif e.type == ACTIVEEVENT:
            active = e.gain


    keys = key.get_pressed() # an arr or dict of somekind of all keys
    moveDis=2
    if keys[K_UP]:
        textPos[1] -= moveDis  #goes up
    if keys[K_DOWN]:
        textPos[1] += moveDis  #goes down
    if keys[K_LEFT]:
        textPos[0] -= moveDis  #goes left
    if keys[K_RIGHT]:
        textPos[0] += moveDis  #goes right



    #graphics
    screen.fill(bgColor)
    draw.circle(screen, REDISH, circlePos, 150, 0)
    text = tileFont.render("My text",True,BLACK) #Isn't on screen yet

    # Put the image of the text on the screen at a POS
    screen.blit(text, textPos) #[circlePos[0] - text.get_width()/2,circlePos[1] - text.get_height()/2]
    if SHOW_MESSAGE:
        text =  msgFont.render("Click the X in the Corner to close.", True, BLACK)
        screen.blit(text, [0,0]) 
    #custom cursor
    draw.circle(screen, [0,255,0], mouse.get_pos(), 20) 

    #Actaully draw things / refresh screen 
    display.update()

    #control frame rate
    clock.tick(60) # 60 fps
