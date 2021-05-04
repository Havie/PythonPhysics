#function ex


from math import sqrt 
import math
def magnitude(x,y):
    return sqrt(x**2 + y**2)

# a=3
# b=4

# print(f"the magnitude of {a}, {b} is: {magnitude(a,b):.3f} " )
# print(f"the magnitude of {a}, {b} is: {magnitude(a,b):10.3f} " )


# x,y = input("Enter the x and y coordinate x,y:").split(",")
# print(f"x:{x} , y:{y}")
# print(f"the magnitude of {x}, {y} is: {magnitude(float(x),float(y)):.3f} " )

money=0

def Add_Money(added):
    global money
    money += added

added = None  # None is like null

while added !=0:
    print(f"your accnt is ${money}")
    try:
        added = float(input("Hot much to add?"))
    except ValueError: 
        print("Invalid Input")
        #added=0
        continue
    if added == math.inf:
        print("Cant have infinite money")
        added =0
    if added is not None: #if u make this a while true, this is how u break out
        break
    Add_Money(added)


