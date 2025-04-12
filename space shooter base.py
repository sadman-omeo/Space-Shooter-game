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



class FallingCircle:
    def __init__(self, x, y, special = False, color = (1, 0, 0)):
        self.x = x
        self.y = y
        self.rad = circle_rad
        self.special = special
        
    def move(self):
        self.y -= circle_speed
    
    def update_rad(self):
        if self.special == True:
            self.rad = circle_rad + (circle_rad / 4) * (1 + math.sin(time.time() * 2))
            


def spawn_falling_circle():
    x = random.randint(15, 485)
    special = random.random() < 0.15
    new_circle = FallingCircle(x, 500, special)
    min_dist = circle_rad * 2
    
    for c in falling_circles:
        dist = ((new_circle.x - c.x) ** 2 + (new_circle.y - c.y) ** 2) ** 0.5
        if dist < min_dist + 10:
            return
    falling_circles.append(new_circle)


def move_falling_circle():
    for c in falling_circles:
        c.move()
        if c.y < 0:
            falling_circles.remove(c)
  
def draw_falling_circle():
    for c in falling_circles:
        if c.special == True:
            draw_mpc_circle(c.x, c.y, c.rad, (0, 1, 0))
        else:
            draw_mpc_circle(c.x, c.y, c.rad, (1, 0, 0))
        
        

#Render the spaceship
def draw_spaceship(x, y, width, height):
    colorb = (0, 0, 1)
    colorg = (0, 1, 0)
    colorr = (1, 0, 0)
    draw_mpl_line(x, y, x - width // 2, y - height // 3, colorb)
    draw_mpl_line(x, y, x + width // 2, y - height // 3, colorb)
    draw_mpl_line(x - width // 2, y - height // 3,x + width // 2, y - height // 3, colorb)
    draw_mpl_line(x - width // 2, y - height // 3, x - width // 2, y - 40, colorb)
    draw_mpl_line(x + width // 2, y - height // 3, x + width // 2, y - 40,colorb )
    draw_mpl_line(x - width // 2, y - 40 ,  x + width // 2, y - 40, colorb)
    draw_mpl_line(x - width // 2, y - height // 2 + 3, x - width // 2 - 8, y - height // 2 - 8,colorb)
    draw_mpl_line(x - width // 2, y - height // 2 - 5, x - width // 2 - 8, y - height // 2 - 8,colorb)
    draw_mpl_line(x + width // 2, y - height // 2 + 3, x + width // 2 + 8, y - height // 2 - 8,colorb)
    draw_mpl_line(x + width // 2, y - height // 2 - 5, x + width // 2 + 8, y - height // 2 - 8,colorb)
    
    draw_mpl_line(x - width // 2 + 2, y - 40, x - width // 2 + 2, y - 50, colorr)
    draw_mpl_line(x, y - 40, x, y - 50, colorr)
    draw_mpl_line(x + width // 2 - 2, y - 40, x + width // 2 - 2, y - 50, colorr)
    
    draw_mpc_circle(x, y, 3, (1, 0, 0))


#Point Draw
def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #point location
    glEnd()


#OpenGL must func
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def FindZone(dx, dy):
    if abs(dx) > abs(dy): 
        if dx > 0 and dy >= 0:
            return 0  
        elif dx < 0 and dy >= 0:
            return 3  
        elif dx < 0 and dy < 0:
            return 4  
        else:
            return 7  
    else:  
        if dx >= 0 and dy > 0:
            return 1  
        elif dx < 0 and dy > 0:
            return 2  
        elif dx < 0 and dy < 0:
            return 5  
        else:
            return 6  
         


def convert_to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return -y, x
    if zone == 7:
        return x, -y
 
               
def convert_to_others(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y
  
