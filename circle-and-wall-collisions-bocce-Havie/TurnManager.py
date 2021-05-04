#from .GameLoop import *



class TurnManager:
    def __init__(self, P1Color=[0,0,0], P2Color=[110,110,110] ):
        self.p1Color=P1Color;
        self.p2Color =P2Color;

    def StartGame(self):
        self.p1Balls=[]
        self.p2Balls=[]
        self.PLAYER_ONES_TURN = True;


    def BallPlaced(self, ball):

        GAMES_RUNNING = not self.IsGameOver() 

        if GAMES_RUNNING == True: 
            self.IncreaseBallCount(ball);

    def SwitchTurn(self):

     self.PLAYER_ONES_TURN=  not self.PLAYER_ONES_TURN


    def IncreaseBallCount(self, ball):
        if(self.PLAYER_ONES_TURN):
            self.p1Balls.append(ball)
        else:
            self.p2Balls.append(ball)
        #print(f"Increased ball count = {self.p1Balls}, {self.p2Balls}")


    def IsPlayersBall(self, ball):
        for o in self.p1Balls:
            if(o==ball):
                return 1;
        for o in self.p2Balls:
            if(o==ball):
                return 2;
        return False; #IDK

    def IsGameOver(self):
        return  len(self.p1Balls) == 4 and  len(self.p2Balls) ==4 ;

    def CheckIfDraw(self):
        return IsDraw()

    def PlayerNumber(self):
        if(self.PLAYER_ONES_TURN):
            return 1
        else:
            return 2


    def WhosTurnColor(self):
        if(self.PLAYER_ONES_TURN):
            return  self.p1Color
        else:
            return  self.p2Color

    def WhosTurnName(self):
        if( self.PLAYER_ONES_TURN):
            return "Player1"
        else :
            return "Player2"

    def WhosTurnNum(self):
        if(self.PLAYER_ONES_TURN):
            return 1
        else :
            return 2


    def IsNextPlayerOutOfBalls(self):
        if(self.PLAYER_ONES_TURN):
            return len(self.p2Balls) == 4
        else:
            return len(self.p1Balls) == 4

    def IsCurrPlayerOutOfBalls(self):
        if(self.PLAYER_ONES_TURN):
            return len(self.p1Balls) == 4
        else:
            return len(self.p2Balls) == 4

