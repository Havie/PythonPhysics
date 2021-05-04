from BoardManager import *

validInput=False
rows = []
cols = []
itemsInCols=[]
global playerXWinner

#---------------------------------------------------------------------------------------#

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

#prints the gameboard properly to the console
def PrintGameBoard():
    arr = [ReverseAnArr(rows),cols ]
    PrintBoard(arr, itemsInCols)
#Determines values for the board with custom or default dimensions
def RequestUserDimensions(CUSTOMIZE_BOARD_SIZE):
    #Reset our arr's
    global rows 
    global cols 
    rows = []
    cols = []

    if(CUSTOMIZE_BOARD_SIZE==True):
        validInput=False
        while validInput !=True:
            try:
                rowSize= int(input("Enter # of rows"))
                validInput= True
            except ValueError:
                print("invalid input, enter an int")
                validInput=False

        validInput=False
        while validInput !=True:
            try:
                colSize= int(input("Enter # of cols"))
                validInput= True
            except ValueError:
                print("invalid input, enter an int")
                validInput=False
    else:
        rowSize=6
        colSize=3



    for i in range(rowSize):
        rows.append(i+1)

    for i in range(colSize):
        cols.append(i+1)   

    SetUpBoard()
#Sets up the board based on global determined dimensions
def SetUpBoard():
    from ColumnCreator import CreateColumnArray
    global itemsInCols
    itemsInCols=CreateColumnArray(cols) # why is it say this is unused by clearly isnt?
#Helper method which returns the string based on whos turn it is
def GetXorO(isPlayerOne):
    if(isPlayerOne):
        return "X"
    else:
       return "O"
#Gets and validates input from the Player whos turn it is, then adds move to the board
def RequestUserMove(isPlayerOne):
    validInput=False
    colSelection=-1
    XorO=GetXorO(isPlayerOne)
    while validInput !=True:
        try:
            colSelection= int(input(f"Player:[{XorO}] Turn!.. Enter Column to drop in:  "))
            if(colSelection>len(cols) or colSelection <= 0):
                print("....invalid choice")
                validInput=False
            else:
                validInput= True
        except ValueError:
            print("....invalid input, enter an int")
            validInput=False

        #IDK WHY Im off by 1..somewhere? heres a HACK:
        if(colSelection-1 >= len(itemsInCols)):
            validInput=False
        elif(len(itemsInCols[colSelection-1]) >= len(rows)):
            print("....invalid input, columns full")
            validInput=False
    #print(f"colSelction={colSelection-1} and len of itemsInCols={len(itemsInCols)} ")
    itemsInCols[colSelection-1].append(XorO)
#Makes decisions for the AI opponent
def AITurn(isPlayerOne):
    XorO=GetXorO(isPlayerOne)
    aiColChoice=0
    print(f"AI places {XorO} col:{aiColChoice}")
    itemsInCols[aiColChoice].append(XorO)
#Determines is anyone one the game
def IsGameOver():

    if(CheckVerticalWin()):
        return True
    if(CheckHorizontalWin()):
        return True
    if(CheckDiagonalWin()):
        return True
    if(CheckDiagonalWinRev()): #could adapt this to one method but using the try catches will probably break the loop? so meh
        return True
    return False
#checks for 3  X or O in a col
def CheckVerticalWin():
    numX=0
    numO=0
    #go thru the cols
    for i in range(len(itemsInCols)):
        colArr= itemsInCols[i]
        for j in range(len(colArr)):
            if(colArr[j]=="X"):
                numX= numX+1
                numO=0
            elif(colArr[j]=="O"):
                numO= numO+1
                numX=0
        #print(f" col{i+1} => NumX={numX} numO={numO}")
        global playerXWinner #this global nonsense SUCKS
        if(numX==3):
            playerXWinner=True
            return True
        elif(numO==3):
            playerXWinner=False
            return True
        numX=0
        numO=0

    return False
#checks for 3  X or O in a row
def CheckHorizontalWin():
    #go thru the rows
    for i in range(len(rows)):
        ##Get col val at this index
        #print(f"looking at row#{i}")
        tmpRow= []
        #Look at each col with items in it
        for j in range(len(itemsInCols)):
            try:
               # print(itemsInCols[i][j])
                tmpRow.append(itemsInCols[j][i])
            except IndexError:
                pass
                #print(f"error at :[{i}][{j}]")
                tmpRow.append("e") # allows the game to be played with >3 cols and accounts for gaps
        
        if( CheckTMPRow(tmpRow, i)==True):
            return True
        
    return False
#checks for 3  X or O diag 
def CheckDiagonalWin():
    #go thru the rows
    for i in range(len(rows)):
        tmpRow= []
        #Look at each col with items in it
        offset=0
        for j in range(len(itemsInCols)):
           # print(f"#{i}-->{itemsInCols[j]}")
            colArr=itemsInCols[j]
            try:
                #print(f"{itemsInCols[j+1][i]} vs {itemsInCols[j][i+1]}")
                tmpRow.append(colArr[i+offset])
                offset= offset+1
            except IndexError:
                pass
                #print(f"error at :[{i}][{j}]")
        
        if( CheckTMPRow(tmpRow, i)==True):
            return True
        
    return False
#checks for 3  X or O diag reversed
def CheckDiagonalWinRev():
    #go thru the rows
    for i in range(len(rows)):
        tmpRow= []
        #Look at each col with items in it
        offset=2
        for j in range(len(itemsInCols)):
           # print(f"#{i}-->{itemsInCols[j]}")
            colArr=itemsInCols[j]
            try:
                #print(f"{itemsInCols[j+1][i]} vs {itemsInCols[j][i+1]}")
                tmpRow.append(colArr[i+offset])
                offset= offset-1
            except IndexError:
                pass
                #print(f"error at :[{i}][{j}]")
        
        if(CheckTMPRow(tmpRow, i)==True):
            return True
        
    return False
#helper method for the horiz / diag rows to check their tmp constructed arrays 
def CheckTMPRow(arr, index):
    #print(f"(Temp row)#{index} --> {arr}")
    lastWasX=True
    inARow=0
    for i in range(len(arr)):
        #print(f"{arr[i]}")
        #print(f"{arr[i]}", end="  ")  
        if(arr[i]=="X"):
            if(lastWasX == True):
                inARow= inARow+1
            else:
                inARow=1
            lastWasX=True
        elif(arr[i]=="O"):
            if(lastWasX==False):
                inARow= inARow+1
            else:
                inARow=1
            lastWasX=False
        elif(arr[i]=="e"):
            inARow=0
        #print(f"lastWasX={lastWasX}||inARow#={inARow}")
        if(inARow>=3):
            global playerXWinner #this global nonsense SUCKS
            playerXWinner = lastWasX
            return True

    return False
#returns the winning X or O of the game
def GetWinner():
    return GetXorO(playerXWinner)

def IsDraw():
    for i in range(len(itemsInCols)):
        colArr= itemsInCols[i]
        if(len(colArr) < len(rows)):
            return False
    
    return True