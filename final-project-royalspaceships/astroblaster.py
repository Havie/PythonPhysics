from pygame import *
from pygame.math import Vector2
import math
from circle import Circle
from wall import Wall
from polygon import Polygon
from polygon import UniformPolygon
from contact import contact
from forces import Gravity
import itertools
import random

# Ethan Kapelka
# April 8, 2021

# initialize game
init()

def mag(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# create screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# create constants
GRAY = [200, 200, 200]
BLUE = [40, 20, 200]
RED = [200, 20, 40]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
ORANGE = [255, 165, 0]
YELLOW = [255, 255, 0]

BALL_MASS = 20
BALL_RADIUS = 15
BALL_VELOCITY = [0, -1000]
SHAPE_DENSITY = 0.2
GROUND_HEIGHT = SCREEN_HEIGHT - 100
PLAYER_MOVEMENT_SPEED = 6
PLAYER_BOUNDARY_SIZE = 50
SHOOT_TIME = 120
STAGE_BASE_SCORE = 20

TRIANGLE_OFFSETS = [
    [-50,0], [50,0], [0,-50]
]
EQUILATERAL_TRIANGLE_OFFSETS = [
    [-60, 0], [60, 0], [0, -60]
]
SQUARE_OFFSETS = [
    [0, 0], [0, 70], [70, 70], [70, 0]
]
RHOMBUS_OFFSETS = [
    [-30, 0], [0, 50], [30, 0], [0, -50]
]
TRAPIZOID_OFFSETS = [
    [-80, 0], [80, 0], [60, -40], [-60, -40]
]
LONG_RECTANGLE_OFFSETS = [
    [-50, 0], [50, 0], [50,-50], [-50,-50]
]
GROUND_OFFSETS = [
    [0, GROUND_HEIGHT], [0, GROUND_HEIGHT+50], [SCREEN_WIDTH, GROUND_HEIGHT+50], [SCREEN_WIDTH, GROUND_HEIGHT]
]

# create fonts
title_font = font.SysFont('comicsansms', 20, True, False)

# create variables
objects = []
polygons = []
balls = []

player = UniformPolygon(offsets=TRIANGLE_OFFSETS, pos=[SCREEN_WIDTH/2, GROUND_HEIGHT], color=GRAY, avel=0, normals_length=0)
objects.append(player)

ground = UniformPolygon(offsets=GROUND_OFFSETS, pos=[0,0], color=BLACK, avel=0, normals_length=0)
objects.append(ground)

# SHAPES = []
SHAPE_OFFSETS = [EQUILATERAL_TRIANGLE_OFFSETS, SQUARE_OFFSETS, RHOMBUS_OFFSETS, TRAPIZOID_OFFSETS, LONG_RECTANGLE_OFFSETS]
SHAPE_COLORS = [BLUE, RED, ORANGE, YELLOW, GRAY]
# SHAPES.append(UniformPolygon(offsets=EQUILATERAL_TRIANGLE_OFFSETS, pos=[50, 50], vel=[10, 100], color=BLUE, avel=0, density=0.1, normals_length=0))
# SHAPES.append(UniformPolygon(offsets=SQUARE_OFFSETS, pos=[250, 50], vel=[10, 100], color=RED, avel=0, density=0.1, normals_length=0))
# SHAPES.append(UniformPolygon(offsets=RHOMBUS_OFFSETS, pos=[50, 250], vel=[10, 100], color=ORANGE, avel=0, density=0.1, normals_length=0))
# SHAPES.append(UniformPolygon(offsets=TRAPIZOID_OFFSETS, pos=[250, 250], vel=[10, 100], color=YELLOW, avel=0, density=0.1, normals_length=0))
# SHAPES.append(UniformPolygon(offsets=LONG_RECTANGLE_OFFSETS, pos=[450, 300], vel=[10, 100], color=GRAY, avel=0, density=0.1 , normals_length=0))

# polygon library
def spawnRandomShape():
    global stage
    global objects
    if stage <= 5:
        spawnID = random.randrange(0, stage)
    else:
        spawnID = 4
    newPoly = UniformPolygon(offsets=SHAPE_OFFSETS[spawnID], pos=[random.randrange(50, SCREEN_WIDTH-50), 10], vel=[random.randrange(-20, 20), random.randrange(40, 80)], color=SHAPE_COLORS[spawnID], avel=0, density=SHAPE_DENSITY, normals_length=0)
    objects.append(newPoly)
    polygons.append(newPoly)

# get shape values
def getShapeValue(color):
    for i in range(len(SHAPE_COLORS)):
        if color == SHAPE_COLORS[i]:
            return i+1
    return 0

# set game variables
score = 0
peak_score = 0
stage = 1
highest_stage = 1
lives = 3
is_ready_to_shoot = True
shoot_counter = 0
gameover = False

# create a Clock object to help with timing
fps = 60
dt = 1/fps
clock = time.Clock()

time.set_timer(USEREVENT, 1000)

# start program
running = True
while running:
    # EVENTS
    for e in event.get():
        # click x in corner
        if e.type == QUIT:
            running = False
        # spawn stage shapes
        elif e.type == USEREVENT:
            time.set_timer(USEREVENT, 1000)
            for i in range(stage):
                spawnRandomShape()
                print("spawn random shape")
    
    # move player
    keys = key.get_pressed()
    x_movement = 0
    if keys[K_LEFT]:
        x_movement -= PLAYER_MOVEMENT_SPEED
    if keys[K_RIGHT]:
        x_movement += PLAYER_MOVEMENT_SPEED
    if PLAYER_BOUNDARY_SIZE < player.pos[0]+x_movement < SCREEN_WIDTH-PLAYER_BOUNDARY_SIZE:
        player.pos[0] += x_movement

    # shoot
    if keys[K_SPACE]:
        if is_ready_to_shoot:
            # create new ball
            shootball = Circle(pos=player.pos-[0, 60], vel=BALL_VELOCITY, mass=BALL_MASS, color=WHITE, radius=BALL_RADIUS)
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

    # collisions
    for a, b in itertools.combinations(objects, 2):
        c = contact(a, b)
        if c:
            if (a == ground and b in polygons):
                score -= getShapeValue(b.color)
                objects.remove(b)
                polygons.remove(b)
            elif (a in polygons and b == ground):
                score -= getShapeValue(b.color)
                objects.remove(a)
                polygons.remove(a)
            elif (a == player and b in polygons):
                objects.remove(b)
                polygons.remove(b)
                lives -= 1
            elif (a in polygons and b == player):
                objects.remove(a)
                polygons.remove(a)
                lives -= 1
            elif (a in polygons and b in polygons) or (a in polygons and b in balls) or (a in balls and b in polygons):
                c.resolve()

    # update objects with physics
    for o in objects:
        o.update(dt)

    # check if balls outside room
    for b in balls:
        if b.pos[0] < -b.radius or b.pos[1] < -b.radius or b.pos[0] > SCREEN_WIDTH+b.radius or b.pos[1] > SCREEN_HEIGHT+b.radius:
            balls.remove(b)
            objects.remove(b)

    # check if objects hit ceiling
    for p in polygons:
        lowest_point = -math.inf
        for i in p.points:
            if i[1] > lowest_point:
                lowest_point = i[1]
                if lowest_point > 0:
                    break
        if lowest_point < 0:
            score += getShapeValue(p.color)
            objects.remove(p)
            polygons.remove(p)

    # remove polygons outside sides of room
    for b in polygons:
        if b.pos[0] < -50 or b.pos[0] > SCREEN_WIDTH + 50:
            objects.remove(b)
            polygons.remove(b)

    # check if objects hit sides

    # check if game over
    if gameover == False and lives <= 0:
        gameover = True

    # DRAW
    # draw background
    screen.fill(BLACK)
    
    # draw objects
    for o in objects:
        o.draw(screen)

    # player.draw(screen)

    # draw ground line
    draw.line(screen, [0, 200, 0], [0, GROUND_HEIGHT], [SCREEN_WIDTH, GROUND_HEIGHT], 4)

    # # check for lost ball
    # if playingball != None:
    #     if playingball.pos[1] > SCREEN_HEIGHT:
    #         objects.remove(playingball)
    #         playingball = None
    #         time.set_timer(USEREVENT, 1)

    # on update peak score
    if score > peak_score:
        peak_score = score

    # get stage based on score
    if score < 15:
        stage = 1
    else:
        stage = math.floor(math.log2(score/STAGE_BASE_SCORE)+2)

    if stage > highest_stage:
        highest_stage = stage
        lives += 1

    # draw text
    if gameover:
        text_gameover = title_font.render(f"GAME OVER - Peak Score:{peak_score}", True, WHITE)
        screen.blit(text_gameover, [(SCREEN_WIDTH - text_gameover.get_width())/2, (SCREEN_HEIGHT - text_gameover.get_height())/2])
    
    # draw score
    text_score = title_font.render(f"Score: {score}", True, WHITE)
    screen.blit(text_score, [(SCREEN_WIDTH - text_score.get_width())/2, 0])

    # draw number of lives
    text_lives = title_font.render(f"Lives: {lives}", True, RED)
    screen.blit(text_lives, [(SCREEN_WIDTH - text_lives.get_width())/2, 20])

    # draw stage
    text_stage = title_font.render(f"Stage: {stage}", True, YELLOW)
    screen.blit(text_stage, [(SCREEN_WIDTH - text_stage.get_width())/2, 40])

    # Refresh the screen
    display.update()

    # Limit the framerate
    clock.tick(fps)