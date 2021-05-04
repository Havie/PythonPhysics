import pygame
    
def CheckCollision(pos1, pos2, radius1, radius2):
    ##  dis between 2 obj is less than sum of 2 radius ? 
    #print(f"pos1={pos1} pos2={pos2} -> [dis= {Distance(pos1, pos2)}  , rad={radius1+ radius2} ] result= {Distance(pos1, pos2) < radius1+ radius2}")
    dis = pygame.math.Vector2.magnitude(pos1 - pos2)
    return dis < radius1+ radius2