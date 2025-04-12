from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math


#Variables:
spaceship_x = 250
spaceship_y = 60
spaceship_width = 20
spaceship_height = 50
spaceship_speed = 10
fireballs = []

falling_circles = []
circle_rad = 20
circle_speed = 0.05

missed_circles = 0
missed_fireballs = 0
score = 0
falling_speed = 5

#Buttons VArs
game_pause = False
game_over = False

#Handling play pause end button using mouse
W_Width, W_Height = 500, 500

