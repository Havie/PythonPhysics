from GameLoop import*

GAMES_RUNNING=True
PLAYER_ONES_TURN=True
PLAY_AGAINST_AI=False
CUSTOMIZE_BOARD_SIZE=True

#---------------------------------------------------------------------------------------#

#----------------------GAME LOOP---------------------------------------------------------#

def StartGame():
    #Creates the gameboard to specifications:
    RequestUserDimensions(CUSTOMIZE_BOARD_SIZE)
    global GAMES_RUNNING # WHYY
    GAMES_RUNNING = True
    GameLoop()

def GameLoop():

    #Random chance for who goes first:
    from random import randrange
    rand= randrange(0,2)  # (inclusive, exclusive)?
    PLAYER_ONES_TURN = rand == 0
    global GAMES_RUNNING #WWHHAT?
    isDraw=False
    #Main Game Loop:
    while GAMES_RUNNING !=False : 
        if(PLAYER_ONES_TURN):
            RequestUserMove(PLAYER_ONES_TURN)
            PLAYER_ONES_TURN=False
        else:
            if(PLAY_AGAINST_AI==True):
                AITurn(PLAYER_ONES_TURN)
            else:
                RequestUserMove(PLAYER_ONES_TURN) 
            PLAYER_ONES_TURN=True

        PrintGameBoard()
        GAMES_RUNNING= (IsGameOver() ==False)
        if(GAMES_RUNNING==True):
            if(IsDraw()==True):
                GAMES_RUNNING=False
                isDraw=True
                Draw()

    if(isDraw==False):
        Winner()
    ReplayGame()

def Draw():
    print(f"-------------GAME------------------")
    print(f"-------------OVER------------------")
    print(f"           --DRAW--                ")
    print(f"-----------------------------------")
    print(f"-----------------------------------")

def Winner(): 
    print(f"-------------GAME------------------")
    print(f"-------------OVER------------------")
    print(f"The Winner was Player: {GetWinner()}")
    print(f"-----------------------------------")
    print(f"-----------------------------------")

def ReplayGame():


    if(PlayAgain()):
       StartGame()

#---------------------------------------------------------------------------------------#


StartGame()
