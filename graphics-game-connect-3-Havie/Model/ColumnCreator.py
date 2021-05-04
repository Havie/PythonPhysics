#Creates a MultiDimensional Array
def CreateColumnArray(array):
    arrMajor= []
    for i in range(len(array)):
        arrMajor.append(CreateAnArray())
    return arrMajor

#helper method to create an empty arr
def CreateAnArray():
    arr=[]
    return arr 