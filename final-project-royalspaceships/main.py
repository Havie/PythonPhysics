from pygame import *
from pygame.math import Vector2
import math
from circle import Circle
from wall import Wall
from polygon import Polygon
from polygon import UniformPolygon
from contact import contact
from forces import Gravitation
import itertools
import random

# Ethan Kapelka

# initialize game
init()

def mag(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# create screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# create constants
DARK_GREEN = [1,50,32]
LIGHT_GRAY =[95,95,95]
GRAY = [200, 200, 200]
COLOR_MAGNET = [200, 200, 60]
BLUE = [40, 20, 200]
RED = [200, 20, 40]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
ORANGE = [200, 100, 0]
YELLOW = [255, 255, 0]
PURPLE = [66,20,82]

BALL_MASS = 20
BALL_RADIUS = 10
BALL_VELOCITY = [0, -1000]
SHAPE_DENSITY = 0.2
GROUND_HEIGHT = SCREEN_HEIGHT - 100
PLAYER_MOVEMENT_SPEED = 6
PLAYER_BOUNDARY_SIZE = 50
SHOOT_TIME = 120
SHAPE_SPAWN_TIME = 3000
COIN_RADIUS = 10
COIN_MASS = 15
G = 1800000
MAGNET_STRENGTH = 3

TRIANGLE_OFFSETS = [
    [-25,0], [25,0], [0,-25]
]
EQUILATERAL_TRIANGLE_OFFSETS = [
    [-30, 0], [30, 0], [0, -30]
]
SQUARE_OFFSETS = [
    [0, 0], [0, 40], [40, 40], [40, 0]
]
RHOMBUS_OFFSETS = [
    [-15, 0], [0, 25], [15, 0], [0, -25]
]
TRAPIZOID_OFFSETS = [
    [-40, 0], [40, 0], [30, -20], [-30, -20]
]
LONG_RECTANGLE_OFFSETS = [
    [-25, 0], [25, 0], [25,-25], [-25,-25]
]
GROUND_OFFSETS = [
    [0, GROUND_HEIGHT], [0, GROUND_HEIGHT+150], [SCREEN_WIDTH, GROUND_HEIGHT+150], [SCREEN_WIDTH, GROUND_HEIGHT]
]

# create fonts
title_font = font.SysFont('comicsansms', 20, True, False)

# create variables
global objects
global polygons
global balls
global coins
global broken_pieces
global ground_pieces
global damage_pieces
global player
global ground
global ledge

# set game variables
global score
global peak_score
global lives
global is_ready_to_shoot
global shoot_counter
global is_magnetizing
global gameover
global is_win
global waiting_to_start

def init_game():
    global objects
    global polygons
    global balls
    global coins
    global broken_pieces
    global damage_pieces
    global ground_pieces
    global player
    global ground
    global score
    global peak_score
    global lives
    global is_ready_to_shoot
    global shoot_counter
    global is_magnetizing
    global gameover
    global is_win
    global waiting_to_start
    global ledge
    
    objects = []
    polygons = []
    balls = []
    coins = []
    broken_pieces = []
    ground_pieces=[]
    damage_pieces=[]

    player = UniformPolygon(offsets=TRIANGLE_OFFSETS, pos=[SCREEN_WIDTH/2, GROUND_HEIGHT], color=ORANGE, avel=0, normals_length=0)
    objects.append(player)

    ground = UniformPolygon(offsets=GROUND_OFFSETS, pos=[0,0], color=DARK_GREEN, avel=0, normals_length=0)
    objects.append(ground)

    score = 0
    peak_score = 0
    lives = 3
    is_ready_to_shoot = True
    shoot_counter = 0
    is_magnetizing = False
    gameover = False
    is_win = False
    
init_game()

SHAPE_OFFSETS = [EQUILATERAL_TRIANGLE_OFFSETS, SQUARE_OFFSETS, RHOMBUS_OFFSETS, TRAPIZOID_OFFSETS, LONG_RECTANGLE_OFFSETS]
SHAPE_COLORS = [BLUE, WHITE, DARK_GREEN, PURPLE, GRAY]

# magnet_force = Gravitation(objects=coins, G=2)

# polygon library
def spawnRandomShape():
    global objects
    global polygons
    spawnID = random.randrange(0, 5)
    newPoly = UniformPolygon(offsets=SHAPE_OFFSETS[spawnID], pos=[random.randrange(50, SCREEN_WIDTH-50), 10], vel=[random.randrange(-20, 20), random.randrange(40, 80)], color=SHAPE_COLORS[spawnID], avel=0, density=SHAPE_DENSITY, normals_length=0)
    objects.append(newPoly)
    polygons.append(newPoly)

# get shape values
def getShapeValue(color):
    for i in range(len(SHAPE_COLORS)):
        if color == SHAPE_COLORS[i]:
            return i+1
    return 0

# break shape
def breakShape(shape):
    if shape != None:
        offsets = shape.offsets # shape.world(shape.offsets)
        for i in range(len(offsets)):
            break_velocity = random.randrange(25, 50)
            break_rotational_velocity = random.randrange(-5, 5)
            newOffsets = []
            newOffsets.append(offsets[i])
            midpoint2 = (offsets[i] + offsets[(i+1)%len(offsets)]) / 2
            newOffsets.append(midpoint2)
            midpoint1 = (offsets[i] + offsets[i-1]) / 2
            newOffsets.append(midpoint1)
            slope = midpoint1 - midpoint2
            tangent = slope.rotate(-90)
            tangent_direction = tangent.normalize()

            # newOffsets = shape.local(shape.newOffsets)
            newPoly = UniformPolygon(offsets=newOffsets, pos=shape.pos, vel=shape.vel + tangent_direction * break_velocity, color=LIGHT_GRAY, avel=break_rotational_velocity, density=0.1, normals_length=0)
            broken_pieces.append(newPoly)
            objects.append(newPoly)
        newCoin = Circle(pos=shape.pos, vel=shape.vel, mass=COIN_MASS, color=YELLOW, radius=COIN_RADIUS)
        coins.append(newCoin)
        objects.append(newCoin)
        polygons.remove(shape)
        objects.remove(shape)

def calculate_universal_gravitation(m, pos1, pos2):
    global G
    r = pos1 - pos2
    return ((-G * MAGNET_STRENGTH * m) / (mag(r)**3)) * r

def getOutsideRoom(obj):
    return obj.pos[0] < -50 or obj.pos[0] > SCREEN_WIDTH + 50 or obj.pos[1] < -50 or obj.pos[1] > SCREEN_HEIGHT + 50


# create a Clock object to help with timing
fps = 60
dt = 1/fps
clock = time.Clock()
currTime=0
currRemovalTimeDmg=0
currRemovalTimeGround =0
maxTimeRemoveDmg = 0.8 # time we show red dmg piece for
maxTimeRemoveGround= 3 # time items remain in the ground
# start program
running = True
waiting_to_start = True
while running:
    # EVENTS
    for e in event.get():
        # click x in corner
        if e.type == QUIT:
            running = False
        # spawn shapes
        elif e.type == USEREVENT:
            time.set_timer(USEREVENT, SHAPE_SPAWN_TIME)
            spawnRandomShape()
    
    
    keys = key.get_pressed()
    # play again button
    if gameover: 
        if keys[K_RETURN]:
            init_game()
    elif not gameover:
        # Keyboard presses:
        # magnetize button
        if keys[K_DOWN]:
            is_magnetizing = True
            player.color = COLOR_MAGNET
        elif is_magnetizing:
            is_magnetizing = False
            player.color = ORANGE

        if is_magnetizing == False:
            # move player
            x_movement = 0
            if keys[K_LEFT]:
                x_movement -= PLAYER_MOVEMENT_SPEED
            if keys[K_RIGHT]:
                x_movement += PLAYER_MOVEMENT_SPEED
            if PLAYER_BOUNDARY_SIZE < player.pos[0]+x_movement < SCREEN_WIDTH-PLAYER_BOUNDARY_SIZE:
                player.pos[0] += x_movement
            # shoot
            if keys[K_SPACE]:
                if waiting_to_start:
                    waiting_to_start = False
                    # set spawn shape timer
                    time.set_timer(USEREVENT, SHAPE_SPAWN_TIME)
                elif is_ready_to_shoot:
                    # create new ball
                    shootball = Circle(pos=player.pos-[0, 60], vel=BALL_VELOCITY, mass=BALL_MASS, color=ORANGE, radius=BALL_RADIUS)
                    objects.append(shootball)
                    balls.append(shootball)
                    is_ready_to_shoot = False
                    shoot_counter = 0

        
        # shoot counter:
        if is_ready_to_shoot == False and shoot_counter < 12:
            shoot_counter += 1
        if shoot_counter >= 12:
            shoot_counter = 0
            is_ready_to_shoot = True

        # PHYSICS
        # clear forces
        for o in objects:
            o.clear_force()

        # coin magnetize
        if is_magnetizing:
            for c in coins:
                c.add_force(calculate_universal_gravitation(c.mass, c.pos, player.pos))

        # collisions
        for a, b in itertools.combinations(objects, 2):
            c = contact(a, b)
            if c:
                # polygons + ground
                if (a == ground and b in polygons):
                    if gameover == False:
                        score -= 1
                    breakShape(b)
                elif (a in polygons and b == ground):
                    if gameover == False:
                        score -= 1
                    breakShape(a)
                # broken_pieces + ground
                if (a == ground and b in broken_pieces):
                    objects.remove(b)
                    broken_pieces.remove(b)
                    ground_pieces.append(b)
                elif (a in broken_pieces and b == ground):
                    objects.remove(a)
                    broken_pieces.remove(a)
                    ground_pieces.append(a)
                # coins + ground
                if (a == ground and b in coins):
                    objects.remove(b)
                    coins.remove(b)
                elif (a in coins and b == ground):
                    objects.remove(a)
                    coins.remove(a)
                # player + polygons
                elif (a == player and b in polygons):
                    objects.remove(b)
                    polygons.remove(b)
                    b.color=RED
                    damage_pieces.append(b)
                    if gameover == False:
                        lives -= 1
                elif (a in polygons and b == player):
                    objects.remove(a)
                    polygons.remove(a)
                    a.color=RED
                    damage_pieces.append(a)
                    if gameover == False:
                        lives -= 1
                # player + pieces
                elif (a == player and b in broken_pieces):
                    objects.remove(b)
                    broken_pieces.remove(b)
                    b.color=RED
                    damage_pieces.append(b)
                    if gameover == False:
                        lives -= 1
                elif (a in broken_pieces and b == player):
                    objects.remove(a)
                    a.color=red
                    broken_pieces.remove(a)
                    damage_pieces.append(a)
                    if gameover == False:
                        lives -= 1
                # player + coins
                elif (a == player and b in coins):
                    objects.remove(b)
                    coins.remove(b)
                    if gameover == False:
                        score += 1
                elif (a in coins and b == player):
                    objects.remove(a)
                    coins.remove(a)
                    if gameover == False:
                        score += 1
                # polygons + bullets
                elif (a in polygons and b in balls) or (a in balls and b in polygons):
                    if a in polygons:
                        balls.remove(b)
                        objects.remove(b)
                        breakShape(a)
                    elif b in polygons:
                        balls.remove(a)
                        objects.remove(a)
                        breakShape(b)

        # update objects with physics
        for o in objects:
            o.update(dt)

        # check if balls outside room
        for b in balls:
            if b.pos[0] < -b.radius or b.pos[1] < -b.radius or b.pos[0] > SCREEN_WIDTH+b.radius or b.pos[1] > SCREEN_HEIGHT+b.radius:
                balls.remove(b)
                objects.remove(b)


        # remove polygons outside room
        for b in polygons:
            if getOutsideRoom(b):
                objects.remove(b)
                polygons.remove(b)
        
        # remove broken_pieces outside room
        for b in broken_pieces:
            if getOutsideRoom(b):
                objects.remove(b)
                broken_pieces.remove(b)

        # check if game over
        if gameover == False and lives <= 0:
            gameover = True
            is_win = False

        # check if win
        if gameover == False and score >= 10:
            gameover = True
            is_win = True

        # DRAW
        # draw background
        screen.fill(BLACK)
        
        # draw objects
        for o in objects:
            o.draw(screen)
        for gp in ground_pieces:
            gp.draw(screen)
        for dp in damage_pieces:
            dp.draw(screen)
        # draw ground line
        draw.line(screen, [0, 200, 0], [0, GROUND_HEIGHT], [SCREEN_WIDTH, GROUND_HEIGHT], 4)

        # on update peak score
        if score > peak_score:
            peak_score = score

        currRemovalTimeDmg +=dt
        if(currRemovalTimeDmg > maxTimeRemoveDmg):
            currRemovalTimeDmg = 0
            if(len(damage_pieces) > 0):
                damage_pieces.remove(damage_pieces[0])

        currRemovalTimeGround+=dt
        if(currRemovalTimeGround > maxTimeRemoveGround):
            currRemovalTimeGround=0
            if(len(ground_pieces) > 0):
                ground_pieces.remove(ground_pieces[0])

    # # get stage based on score
    # if score < 15:
    #     stage = 1
    # else:
    #     stage = math.floor(math.log2(score/STAGE_BASE_SCORE)+2)

    # if stage > highest_stage:
    #     highest_stage = stage
    #     lives += 1

    # draw gameover text
    if gameover:
        if is_win:
            text_gameover = title_font.render(f"YOU WIN - Lives Remaining:{lives}", True, WHITE)
        else:
            text_gameover = title_font.render(f"GAME OVER - Peak Score:{peak_score}", True, WHITE)
        screen.blit(text_gameover, [(SCREEN_WIDTH - text_gameover.get_width())/2, (SCREEN_HEIGHT - text_gameover.get_height())/2])
        # draw play again text
        playagain_text = title_font.render("Press Enter to play again", True, WHITE)
        screen.blit(playagain_text, [(SCREEN_WIDTH - playagain_text.get_width()) / 2, (SCREEN_HEIGHT - playagain_text.get_height()) / 2 + 32])
    
    # draw instructions text
    if waiting_to_start:
        instruction_text = title_font.render("Instructions", True, WHITE)
        instruction_text1 = title_font.render("Use the arrow keys to move left and right", True, WHITE)
        instruction_text2 = title_font.render("Press spacebar to shoot bullets", True, WHITE)
        instruction_text3 = title_font.render("Press down arrow key to use coin magnet", True, WHITE)
        instruction_text4 = title_font.render("Collect 10 coins without dying to win", True, WHITE)
        instruction_text5 = title_font.render("Press Spacebar to Start", True, WHITE)
        screen.blit(instruction_text, [(SCREEN_WIDTH - instruction_text.get_width()) / 2, (SCREEN_HEIGHT - instruction_text.get_height()) / 2])
        screen.blit(instruction_text1, [(SCREEN_WIDTH - instruction_text1.get_width()) / 2, (SCREEN_HEIGHT - instruction_text1.get_height()) / 2 + 16])
        screen.blit(instruction_text2, [(SCREEN_WIDTH - instruction_text2.get_width()) / 2, (SCREEN_HEIGHT - instruction_text2.get_height()) / 2 + 32])
        screen.blit(instruction_text3, [(SCREEN_WIDTH - instruction_text3.get_width()) / 2, (SCREEN_HEIGHT - instruction_text3.get_height()) / 2 + 48])
        screen.blit(instruction_text4, [(SCREEN_WIDTH - instruction_text4.get_width()) / 2, (SCREEN_HEIGHT - instruction_text4.get_height()) / 2 + 64])
        screen.blit(instruction_text5, [(SCREEN_WIDTH - instruction_text5.get_width()) / 2, (SCREEN_HEIGHT - instruction_text5.get_height()) / 2 + 160])

    # draw score
    text_score = title_font.render(f"Score: {score}", True, YELLOW)
    screen.blit(text_score, [(SCREEN_WIDTH - text_score.get_width())/2, 0])

    # draw number of lives
    text_lives = title_font.render(f"Lives: {lives}", True, RED)
    screen.blit(text_lives, [(SCREEN_WIDTH - text_lives.get_width())/2, 20])

    # # draw stage
    # text_stage = title_font.render(f"Stage: {stage}", True, YELLOW)
    # screen.blit(text_stage, [(SCREEN_WIDTH - text_stage.get_width())/2, 40])

    # Refresh the screen
    display.update()

    # Limit the framerate
    clock.tick(fps)