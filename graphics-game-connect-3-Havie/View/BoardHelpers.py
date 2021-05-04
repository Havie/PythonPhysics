from pygame import *
import math
WHITE= [255,255,255]
BLACK= [0,0,0]
GRAY= [40,40,40]
BLUE=  [15,20,200]
RED =  [255,10,10]

circlePositions=[] # I might want this class to hang onto this 
              #xLeft, xRight, yTop, yBot
boardDimensions = [0,0,0,0]
colXCoordinates= []


#prompts user to play again
def PlayAgain():

    validInput=False
    choice=""
    while validInput !=True:
        choice= (input("Play Again? (Y/N)"))
        validInput= True
        if(choice=="Y" or choice=="N"):
            if(choice=="Y"):
                return True
            if(choice=="N"):
                return False
        else:
            validInput= False

def CheckColor(Color1, Color2): # how else to do a comparison on whatever dataType Colors are? array vs array ?
    if(Color1[0]==Color2[0] and Color1[1]==Color2[1] and Color1[2]==Color2[2]):
        return True;
    else:
        return False;

def AddToColumn(colNumber, COLOR):
    
    requiredXCoord= colXCoordinates[colNumber-1]
    for i in range(len(circlePositions)):
       circle= circlePositions[i]
       if(circle[0] == requiredXCoord and CheckColor(circle[2], BLACK)):
          print(f"Sucess!!:{circle} for {requiredXCoord}" )
          circle[2] = COLOR
          return True;

    return False;

def GetNearestCol(clickPos):
    bizarreOffset=30
    inRangeDistance=15
    for i in range(len(colXCoordinates)):
        columnPos= colXCoordinates[i]
        mousePos= clickPos[0] - bizarreOffset
        #print(f"colsXCoordinate={columnPos} , clickPos[x]={clickPos[0]} + offset= {mousePos}")
        if(math.fabs(columnPos - mousePos) < inRangeDistance ):
            #print(f"true(1)={math.fabs(columnPos -mousePos)}")
            return i+1
        elif (math.fabs(mousePos- columnPos)   < inRangeDistance ):
            #print(f"true(2)={math.fabs(mousePos- columnPos)}")
            return i+1
    return -1

def InBoardRange(clickPos):
    bizarreOffset=30 # some kind of screen space math im not understanding, this fixes it 
    #xDis= math.fabs(clickPos[0] - boardDimensions[0])
    #print(f" mousPos={clickPos[0]} , boardX=  {(boardDimensions[0])}, {(boardDimensions[1])} ")
    
    #Horizontal
    if(clickPos[0] < boardDimensions[0] ): # clicked left of board
        return False;
    if(clickPos[0] > boardDimensions[1] + bizarreOffset*2): # clicked right of board 
        return False; 
    #Vertical
    if(clickPos[1] < boardDimensions[2] ): # clicked above board
        return False; 
    if(clickPos[1] > boardDimensions[3] ): # clicked below board
        return False; 



    return True

def GetPlayerColor(playerNum):
    if(playerNum==1):
        return RED
    else : 
        return BLUE

def DrawCirclePositions(screen):
    bizarreOffset=30 # some kind of screen space math im not understanding, this fixes it 
    for i in range(len(circlePositions)):
        arr=circlePositions[i]
        rect = [bizarreOffset+arr[0],bizarreOffset+arr[1]]
        draw.circle(screen, arr[2], rect, 40, 0)

def GenerateCircles(rows, cols, width, height, color):

    xLeft =0
    xRight =0
    yTop =0
    yBot=0
    global circlePositions
    circlePositions=[] # I might want this to hang onto 
    colX= width/cols
    xLeft=colX
    for i in range(cols):
        xPos = colX+ (i*colX)
        colY=height
        heightPerRow= height/rows
        yBot= colY
        for j in range(rows):
            yPos= colY - (j*heightPerRow)
            circlePositions.append(GetColumnArray(xPos, yPos, color))
            yTop=yPos
        xRight=xPos
        global colXCoordinates
        colXCoordinates.append(xPos) #keep track of where our cols are
    
    global boardDimensions
    boardDimensions = [xLeft,xRight,yTop,yBot]
    #return circlePositions

def GetColumnArray(xPos, yPos, color):
    return [int(xPos),int(yPos),color]