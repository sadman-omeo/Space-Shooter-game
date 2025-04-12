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
  


def draw_mpl_line(x1, y1, x2, y2, color = (1.0, 1.0, 1.0)):
    
    dx = x2 - x1
    dy = y2 - y1
    zone = FindZone(dx, dy)
    x1, y1 = convert_to_zone_0(x1, y1, zone)
    x2, y2 = convert_to_zone_0(x2, y2, zone)
    if x1 > x2: 
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy - dx)
    
    glPointSize(2)
    glColor3fv(color)
    glBegin(GL_POINTS)
    x, y = x1, y1
    while x <= x2:
        # Convert back to original zone
        x_plot, y_plot = convert_to_others(x, y, zone)
        glVertex2f(x_plot, y_plot)

        if d <= 0:
            d += dE
        else:
            d += dNE
            y += 1
        x += 1

    glEnd()
            

def draw_circle_points(x_c, y_c, x, y, color):
    
    glColor3fv(color)
    glBegin(GL_POINTS)
    glVertex2f(x_c + x, y_c + y)
    glVertex2f(x_c + x, y_c - y)
    glVertex2f(x_c - x, y_c + y)
    glVertex2f(x_c - x, y_c - y)
    glVertex2f(x_c + y, y_c + x)
    glVertex2f(x_c + y, y_c - x)
    glVertex2f(x_c - y, y_c + x)
    glVertex2f(x_c - y, y_c - x)
    glEnd()
    
    

def draw_mpc_circle(x_c, y_c, r, color):
    x = 0
    y = r
    d = 1 - r
    color = color
    draw_circle_points(x_c,  y_c, x, y, color)
    while x < y:
        if d < 0:
            d = d + 2*x + 3
            x += 1
        else:
            d = d + 2*x - 2*y + 5
            x += 1
            y -= 1
        draw_circle_points(x_c, y_c, x, y, color)  


def draw_restart_button():
    color = (0, 0, 1)
    draw_mpl_line(10, 470, 30, 470, color)
    draw_mpl_line(10, 470, 20, 480, color)
    draw_mpl_line(10, 470, 20, 460, color)  

def draw_play_pause_button():
    color = (1, 1, 0)
    draw_mpl_line(245, 480, 245, 460, color)
    draw_mpl_line(245, 480, 255, 470, color)
    draw_mpl_line(245, 460, 255, 470, color)
    
def draw_exit_button():
    color = (1, 0, 0)
    draw_mpl_line(470, 480, 490, 460, color)
    draw_mpl_line(470, 460, 490, 480, color)
    
def draw_buttons():
    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()


def showScreen():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_spaceship(spaceship_x, spaceship_y, spaceship_width, spaceship_height)
    draw_falling_circle()
    
    draw_buttons()
    glutSwapBuffers()
    

def has_collided(box1, box2):
    return (
        box1['x'] < box2['x'] + box2['width'] and
        box1['x'] + box1['width'] > box2['x'] and
        box1['y'] < box2['y'] + box2['height'] and
        box1['y'] + box1['height'] > box2['y']
    )


def animate():
    
    global fireballs
    global falling_circles
    global falling_speed
    global score
    global missed_circles
    global circle_rad
    global missed_fireballs
    global game_pause
  
    
    if game_pause == True:
        return
    
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    #Spaceship and falling circle colide
    spaceship_box = {'x': spaceship_x - spaceship_width // 2, 'y': spaceship_y - spaceship_height // 2 - 20, 'width': spaceship_width, 'height': spaceship_height}
    
    for fc in falling_circles[:]:
           falling_circle_box = {'x': fc.x - fc.rad, 'y': fc.y - fc.rad, 'width': fc.rad * 2, 'height': fc.rad * 2}
           if has_collided(spaceship_box, falling_circle_box):
               print(f'Game Over! Final Score: {score}')
               game_over = True
               glutLeaveMainLoop()
               return
    
    # Draw the circle at the updated position
    
    
    for fr in fireballs:
        fr['y'] += fr['speed']
        draw_mpc_circle(fr['x'], fr['y'], fr['rad'], (1, 0.5, 0))
        
        #AABB for fireballs
        fireball_box = {'x' : fr['x'] - fr['rad'], 'y' : fr['y'] - fr['rad'], 'width' : fr['rad'] * 2, 'height': fr['rad'] * 2}
        if fr['y'] > 500:
            fireballs.remove(fr)
            missed_fireballs += 1
            print(f"missed fireballs: {missed_fireballs}")
            
            if missed_fireballs >= 3:
                print(f'Game Over! Final Score: {score}')
                glutLeaveMainLoop()
                break
    
    
    if len(falling_circles) < 5:
        if random.random() < 0.05:  # Adjust spawn rate (1% chance per frame)
            spawn_falling_circle()
            
    for fc in falling_circles[:]: #fc = falling circle
        fc.move()
        fc.update_rad()
        
        #AABB for falling circle
        circle_box = {'x' : fc.x - fc.rad, 'y' : fc.y - fc.rad, 'width' : fc.rad * 2, 'height' : fc.rad * 2}
        
        
        #Remove the circles if it goes off the screen
        if fc.y <= 0:
            falling_circles.remove(fc)
            missed_circles += 1
            print(f"Missed circles : {missed_circles}")
            if missed_circles >= 3:
                print(f"Game Over! Final Score : {score}")
                glutLeaveMainLoop()
                return
        
        #Check if collision with fireball:
        for fr in fireballs[:]:
            fireball_box = {'x' : fr['x'] - fr['rad'], 'y' : fr['y'] - fr['rad'], 'width' : fr['rad'] * 2, 'height': fr['rad'] * 2}
            
            if has_collided(circle_box, fireball_box):
                falling_circles.remove(fc)
                fireballs.remove(fr)
                if fc.special == True:
                    score += 2
                    print('Bonus Earned')
                else:
                    score += 1
                print(f"Score: {score} !!!")
                return 
                   
         
      
    
    glutSwapBuffers()
    glutPostRedisplay()
    
    


