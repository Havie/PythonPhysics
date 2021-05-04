from .GameLoop import *

GAMES_RUNNING=True
PLAYER_ONES_TURN=True



def StartGame():
    global PLAYER_ONES_TURN
    PLAYER_ONES_TURN=True

    RequestUserDimensions(False)


def HandleChoice(colToDropIn):
    global PLAYER_ONES_TURN
    
    AppendChoiceToCol(PLAYER_ONES_TURN, colToDropIn)
    GAMES_RUNNING = IsGameOver() == False
    if GAMES_RUNNING == True: 
        PLAYER_ONES_TURN=  not PLAYER_ONES_TURN
    PrintGameBoard()
    return not GAMES_RUNNING

def CheckIfDraw():
    return IsDraw()

def PlayerNumber():
    if(PLAYER_ONES_TURN):
        return 1
    else:
        return 2