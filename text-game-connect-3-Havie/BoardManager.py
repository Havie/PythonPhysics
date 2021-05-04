#Functions to print / manage the gameboard
from GenericHelpers import *

#print the board to the console
def PrintBoard( arr, itemsInCols):
    #did not need to clone the array as we arent modifying it
    #rowsClone= arr[0].copy()
    #colsClone= arr[1].copy()
    savedLines= GenerateEmptyLines(arr[0], arr[1])
    finalArr= PlaceItemsInEmptyCols(savedLines,itemsInCols )
    PrintLines(finalArr)
#Places "e" placeholders into our empty spots
def GenerateEmptyLines(rowsClone, colsClone):
    savedLine= []
    for i in range(len(rowsClone)):
        sLine=""
        for j in range(len(colsClone)):
            sLine+=(f"| e ")  # keep on one line
        newLine=F"{rowsClone[i]}{sLine}"
        #print(newLine)
        savedLine.append(newLine)
    sLine="  "
    for k in range(len(colsClone)):
          sLine+=(f" {colsClone[k]}  ")
    #print(sLine)
    savedLine.append(sLine)
    return savedLine
#parses our user-generated itemsInCols and replaced the "e" placeholders
def PlaceItemsInEmptyCols(savedLines, itemsInCols):
        #print((f"# itemsInColsSize={len(itemsInCols)}"))
        addedLinesReversed=[]
        reversedRows=  ReverseAnArr(savedLines)
        for i in range(len(reversedRows)-1):
            sLine= reversedRows[i+1] #Omit the bottom    1   2   3
            numOfEs=range(len(itemsInCols))
            for e in numOfEs: 
                colDataArr= itemsInCols[e]
                #print(f"the colData#{e} size={len(colDataArr)}")
                val=sLine.find("e")
                if(len(colDataArr)>i):
                    colValue=colDataArr[i]
                    sLine= f"{SubString(sLine, 0, val)}{colValue}{SubString(sLine, val+1, len(sLine))}"  #SubString helper method
                else:
                    sLine= sLine[0:val] + " " + sLine[val+1:len(sLine)] #Python way to subString
                #print(sLine)
            addedLinesReversed.append(sLine)
        #Return things in the proper order
        return PutBackInOrder(addedLinesReversed, reversedRows[0])
#reverse the work done by parsing the EmptyLines       
def PutBackInOrder(arrInRev, firstLine):
    inOrder= ReverseAnArr(arrInRev)  
    inOrder.append(firstLine)
    return inOrder; 
#helper to print the lines of any array
def PrintLines(arr):
    for i in range(len(arr)):
        print(arr[i])
#helper to reverse any array
def ReverseAnArr(arr):
    aReversed = []
    for i in range(len(arr)):
        index=(len(arr)-i-1)
        #print(f"..index= {index}")
        item = arr[index]
        #print(f"i={i}--> item= {item}")
        aReversed.append(item)
    return aReversed

