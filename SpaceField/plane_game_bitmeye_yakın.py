# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 13:46:20 2022

@author: goktu
"""

from graphics import Canvas
import time
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PLANE_Y = 80
PLANE_X = 50
BULLET_X = 10
BULLET_Y = 20


velocity_x = 0
velocity_y = -5

list_bullet = []
meteor_list = []



def make_bullet(canvas):
    x = canvas.get_mouse_x()
    y = CANVAS_HEIGHT - (20 + PLANE_Y) - PLANE_Y//2
    # bullet = canvas.create_rectangle(x, y, x + BULLET_X, y + BULLET_Y)
    bullet = canvas.create_image_with_size(x, y, BULLET_X, BULLET_Y, "isin.png")
    return bullet


def make_plane(canvas):
    x1 = CANVAS_WIDTH/2 - PLANE_X/2
    y1 = CANVAS_HEIGHT - (20 + PLANE_Y)
    # plane = canvas.create_rectangle(x1, y1, x1 + PLANE_X, y1 + PLANE_Y)
    plane = canvas.create_image_with_size(x1, y1, PLANE_X, PLANE_Y, "spaceship 4.png")
    # canvas.set_fill_color(plane, "white")
    return plane

def move_plane(canvas, plane):
    canvas.moveto(plane, min(max(canvas.get_mouse_x()-PLANE_X/2,0),CANVAS_WIDTH-PLANE_X), CANVAS_HEIGHT - (20 + PLANE_Y))

def move_bullet(canvas, bullet):
    canvas.move(bullet, velocity_x, velocity_y)

def check_collisions(canvas, bullet, meteor, ucak):
    for bullet in list_bullet:
        bullet_coords = canvas.coords(bullet)
        overlapping = canvas.find_overlapping(bullet_coords[0], bullet_coords[1], bullet_coords[0] + BULLET_X, bullet_coords[1] + BULLET_Y)
        for over in overlapping:
            if over in meteor_list:
                canvas.delete(over)
                meteor_list.remove(over)
                canvas.delete(bullet)
                list_bullet.remove(bullet)
                return 1
            
    plane_coords = canvas.coords(ucak)
    colliding_list_plane = canvas.find_overlapping(plane_coords[0],plane_coords[1],plane_coords[0]+PLANE_X,plane_coords[1]+PLANE_Y)
    
    for collider in colliding_list_plane:
        if collider in meteor_list:
            return False
        
    for meteor in meteor_list:
        top = canvas.get_top_y(meteor)
        if top > CANVAS_HEIGHT:
            return False
    
    
def make_meteor(canvas):
    METEOR_RADIUS = random.randint(50, 100)
    random_x = random.randint(0,CANVAS_WIDTH-METEOR_RADIUS)
    random_y = random.randint(-5000, 0)
    # meteor = canvas.create_oval(random_x, random_y , random_x + METEOR_RADIUS, random_y + METEOR_RADIUS)
    meteor = canvas.create_image_with_size(random_x, random_y, METEOR_RADIUS, METEOR_RADIUS, "meteor.png")
    meteor_list.append(meteor)
    return meteor
    
def move_meteor(canvas, meteor):
    vel_meteor_x = 0
    vel_meteor_y = random.randint(2, 5)
    for meteor in meteor_list:
        canvas.move(meteor, vel_meteor_x, vel_meteor_y)

def make_text(canvas, meteor_counter):
    text = canvas.create_text(55, 10, "Meteor Counter: {}".format(meteor_counter))
    canvas.set_color(text, "blue")
    return text

def play_game(canvas, bullet, ucak, meteor, meteor_counter, meteor_count):
    text = make_text(canvas, meteor_counter)
    for i in range(meteor_count):
        make_meteor(canvas)
    while meteor_count > 0:
        move_meteor(canvas, meteor)
        move_plane(canvas, ucak)
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            list_bullet.append(make_bullet(canvas))
            
        for bullet in list_bullet:
            if canvas.get_top_y(bullet) <= 0:
                canvas.delete(bullet)
                list_bullet.remove(bullet)
                
        for bullet in list_bullet:
            move_bullet(canvas, bullet)
        
        sonuc = check_collisions(canvas, bullet, meteor, ucak)
        
        
        if sonuc == 1:
            meteor_counter += 1
            canvas.delete(text)
            text = make_text(canvas, meteor_counter)
            if meteor_counter > meteor_count:
                win_text = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, "CONGRATULATIONS YOU ELIMINATED ALL OF THE METEORS!!!")
                canvas.set_color(win_text, "green")
                break
            
        if sonuc == False:
            text_go = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, "GAME OVER")
            canvas.set_color(text_go, "red")
            break
        
        
        
        time.sleep(0.001)
        canvas.update()

def check_clicks_coords(canvas):
    rect_size_x = 150
    rect_size_y = 60
    SEP = 10
    x = CANVAS_WIDTH/2 - rect_size_x/2 
    y = CANVAS_HEIGHT/2 - rect_size_y/2
    
    mouse_x = canvas.get_mouse_x()
    mouse_y = canvas.get_mouse_y()
    
    if mouse_x > x and mouse_x < x + rect_size_x:
        if mouse_y > y - rect_size_y - SEP and mouse_y < y - rect_size_y - SEP + rect_size_y:
            meteor_count = 24
            return meteor_count
        elif mouse_y > y and mouse_y < y + rect_size_y:
            meteor_count = 34
            return meteor_count
        elif mouse_y > y + rect_size_y + SEP and mouse_y < y + rect_size_y + SEP + rect_size_y:
            meteor_count = 64
            return meteor_count

    meteor_count = 34
    return meteor_count
    
    
def make_levels(canvas):
    rect_size_x = 150
    rect_size_y = 60
    SEP = 10
    x = CANVAS_WIDTH/2 - rect_size_x/2 
    y = CANVAS_HEIGHT/2 - rect_size_y/2

    easy = canvas.create_rectangle(x, y - rect_size_y - SEP, x + rect_size_x,  y - rect_size_y - SEP + rect_size_y)
    normal = canvas.create_rectangle(x, y, x + rect_size_x, y + rect_size_y)
    hard = canvas.create_rectangle(x, y + rect_size_y + SEP, x + rect_size_x, y + rect_size_y + SEP + rect_size_y)
    
    canvas.set_color(easy, "gray")
    canvas.set_color(normal, "gray")
    canvas.set_color(hard, "gray")
    
    easy_txt = canvas.create_text(x+rect_size_x/2, y - rect_size_y + rect_size_y/2 - SEP, "EASY")
    normal_txt = canvas.create_text(x+rect_size_x/2, y +rect_size_y/2, "NORMAL")
    hard_txt = canvas.create_text(x+rect_size_x/2, y + rect_size_y + SEP + rect_size_y/2, "HARD")

    canvas.set_color(easy_txt, "black")
    canvas.set_color(normal_txt, "black")
    canvas.set_color(hard_txt, "black")
    

    
    
def main ():
    canvas = Canvas(CANVAS_WIDTH,CANVAS_HEIGHT)
    meteor_count = 0
    
    firstbg = canvas.set_canvas_background_color("black")
    make_levels(canvas)
    canvas.wait_for_click()
    meteor_count = check_clicks_coords(canvas)

    canvas.wait_for_click()
    canvas.delete(firstbg)
        
    canvas.create_image_with_size(0,0, CANVAS_WIDTH, CANVAS_HEIGHT, "space 3.jpg")
    ucak = make_plane(canvas)
    bullet = make_bullet(canvas)
    meteor = make_meteor(canvas)
    canvas.delete(bullet)
    meteor_counter = 0
    
    
    text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 , "YOU NEED TO SHOOT ALL OF THE METEORS, DON'T ESPCAPE FROM THEM")
    canvas.set_color(text, "red")
    
    canvas.wait_for_click()
    canvas.delete(text)

    play_game(canvas, bullet, ucak, meteor, meteor_counter, meteor_count)
        
    canvas.mainloop()
    
    
if __name__ == '__main__':
    main()    
    