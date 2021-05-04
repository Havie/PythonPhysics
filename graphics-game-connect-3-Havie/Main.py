#import pygame 
from pygame import *
#https://www.pygame.org/docs/ref/display.html
from View.BoardHelpers import *
from Model.TurnManager import *

WHITE= [255,255,255]
BLACK= [0,0,0]
GRAY= [40,40,40]
bgColor = BLACK
cursorColor=WHITE



#create window 
screen = display.set_mode([600,800])
#create a clock
clock = time.Clock() 

#Rect(left, top, width, height)
boardPos= [100,90,screen.get_width() * 0.65,screen.get_height() * 0.85]
GenerateCircles(6,3,boardPos[2], boardPos[3], BLACK ) # will need to be an array of [x,y, COLOR]'s 


init() #pygame function
StartGame() #Start TurnManager


#create font object
tileFont = font.SysFont('Calibri', size=15, bold=True, italic=False)
msgFont = font.SysFont('Calibri', size=25, bold=False, italic=True)


RUNNING=True
GAMES_ACTIVE=True
mouse.set_visible(False)


active = True
SHOW_MESSAGE=False
Custom_msg= ""
PRINTED_SOMETHING=USEREVENT
PLAY_AGAIN=USEREVENT+1
Read_for_playAgain=False;
# Game Loop 
while RUNNING : 
    
    #loop thru all new events
    for e in event.get():
        if e.type == QUIT:
            RUNNING=False
        elif e.type ==KEYUP and e.key==K_ESCAPE:
            time.set_timer(PRINTED_SOMETHING, 1000, True) #1000 milisec is 1 sec, TRUE MEANS ONLY FIRE ONCE!
            SHOW_MESSAGE=True
        elif e.type == PRINTED_SOMETHING:
            SHOW_MESSAGE=False
        elif e.type == PLAY_AGAIN:
           Custom_msg = "Play Again? (Y/N)"
           Read_for_playAgain=True;
        elif e.type == MOUSEBUTTONUP and e.button ==1 and display.get_active() and InBoardRange(e.pos) and GAMES_ACTIVE: 
            colDroppedIn= GetNearestCol(e.pos)
            #print(f"..ColDrop:{colDroppedIn}")
            if(colDroppedIn!= -1):
                GAMES_ACTIVE= (HandleChoice(colDroppedIn) == False)
                colFull = not AddToColumn(colDroppedIn, cursorColor)
                if colFull : 
                    time.set_timer(USEREVENT, 1000, True) #1000 milisec is 1 sec
                    Custom_msg= "Column is Full"
                    SHOW_MESSAGE=True;
                if CheckIfDraw():
                        Custom_msg="Draw!"
                        GAMES_ACTIVE=False;
                if GAMES_ACTIVE ==False:
                    print("Only Fire this Event ONCE")
                    time.set_timer(PLAY_AGAIN, 1000, True) #1000 milisec is 1 sec
                #print(f"Selected Column:{colDroppedIn} , GAMES_ACTIVE={GAMES_ACTIVE}")
        elif e.type == KEYUP :
            if Read_for_playAgain :
                if e.key == K_y or e.key== K_SPACE:
                   GenerateCircles(6,3,boardPos[2], boardPos[3], BLACK )
                   StartGame()
                   GAMES_ACTIVE=True
                   Read_for_playAgain=False
                elif e.key == K_n:
                     RUNNING=False;

        elif e.type == MOUSEMOTION:
            pass
        elif e.type == ACTIVEEVENT:
            active = e.gain



    #graphics
    screen.fill(bgColor)
    #draw board:
    draw.rect(screen, GRAY, boardPos, 0)

    playerNum=PlayerNumber()
    cursorColor= GetPlayerColor(playerNum)



    if(GAMES_ACTIVE==True):
        if(SHOW_MESSAGE):
            text = tileFont.render(f"{Custom_msg}",True, WHITE) #Isn't on screen yet
        else:
            text = tileFont.render(f"Player {playerNum}. Place your piece",True, cursorColor) #Isn't on screen yet
       
    elif(GAMES_ACTIVE==False):
        if(CheckIfDraw() or Read_for_playAgain):
            text = tileFont.render(f"{Custom_msg}",True, WHITE) #Isn't on screen yet
        else:
             text = tileFont.render(f"Winner= Player {playerNum}!",True, cursorColor) #Isn't on screen yet
          
        
   
    textPos = [screen.get_width()/2 - text.get_width()/2, 10]
    # Put the image of the text on the screen at a POS
    screen.blit(text, textPos) 


    #Draw board
    DrawCirclePositions(screen)

    #custom cursor
    draw.circle(screen, cursorColor, mouse.get_pos(), 40) 

    #Actaully draw things / refresh screen 
    display.update()

    #control frame rate
    clock.tick(60) # 60 fps