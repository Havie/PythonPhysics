import math 

print("hello world")

a=5
b=6

# this is a^2 
print("This is a^2=" , a**2)

print (math.sqrt(b))

# type clear in terminal to clear it 



# cntrol + / to comment and uncomment 

# name = input("Wat is ur name?")

# name = name.lower()

# if name == "me": 
#     print("i miss curly braces and (), this is 4 spaces or TAB to indent")
# elif name == "nobody" or name =="":
#     print("fuck you ghost")
# elif name.lower() in ("jesus" or "allah" or "god" ):
#     print("Hello mah lord")
# else :
#     print(f"HI {name.lower()} !!!!!")


stuff = [12, "Dave", math.sqrt]

print(stuff[1], "Favorite # is ", stuff[-1](9)) # Can count backwards for indicies in python


more_stuff = stuff # pointer to same place in memory , a ref

more_stuff.append("frisbee")
print (stuff, "vs", more_stuff)

#instead we should do copy

copied_stuff = more_stuff.copy()
copied_stuff.append("JESUS TAKE THE WHEEL")

print(copied_stuff)



for item in stuff: 
    print(item)

for i in range(2,9): # (inclusive, exclusive)
    print(f"i={i}", end="  ")  # keep the shit on one line


#APPENDED FROM GITHUBDESKTOP

print("Good bye")