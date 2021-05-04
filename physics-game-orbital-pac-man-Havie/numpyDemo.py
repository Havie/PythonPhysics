import numpy as np   #should be part of anaconda 
import math
pos = [300,400] #not a numpy array, its just a list

pos+= [10,10] #does not make it [310,410]

print(pos)


pos=  np.array([300,400])
pos+= [10,10] #now works as [310,410]

a= np.array([3,5])
b= np.array([-1,2])

print(f" {a} + {b} = {a+b}");

print(a.shape)


def Magnitude(vector):
    return np.linalg.norm(vector)

def Mag(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])

#maginitude:
print(f"magnitude= |{a}| = {Magnitude(a)}  vs {Mag(a)}")


d= np.zeros([2,3], float)
print(d.shape)
