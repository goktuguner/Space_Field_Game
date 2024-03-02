# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 13:46:20 2022

@author: group_16
        Goktug Uner
        Alp Bugra Ariduman
        Seyhmuz Aydin
        Abdullah Cagri Camas
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


velocity_x_bullet = 0
velocity_y_bullet = -12.5
prize_num = 5

list_bullet = []
meteor_list = []
prize_list = []  


def make_bullet(canvas):
    x = canvas.get_mouse_x() - BULLET_X//2
    y = CANVAS_HEIGHT - (15 + PLANE_Y) - PLANE_Y//2
    bullet = canvas.create_image_with_size(x, y, BULLET_X, BULLET_Y, "isin.png")
    return bullet


def make_plane(canvas):
    x1 = CANVAS_WIDTH/2 - PLANE_X/2
    y1 = CANVAS_HEIGHT - (20 + PLANE_Y)
    plane = canvas.create_image_with_size(x1, y1, PLANE_X, PLANE_Y, "spaceship 4.png")
    return plane

def move_plane(canvas, plane):
    canvas.moveto(plane, min(max(canvas.get_mouse_x()-PLANE_X/2,0),CANVAS_WIDTH-PLANE_X), CANVAS_HEIGHT - (20 + PLANE_Y))

def move_bullet(canvas, bullet):
    canvas.move(bullet, velocity_x_bullet, velocity_y_bullet)

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
        elif collider in prize_list:
            canvas.delete(collider)
            prize_list.remove(collider)
            return 2
            
    for meteor in meteor_list:
        top = canvas.get_top_y(meteor)
        if top > CANVAS_HEIGHT:
            return False
    
    
def make_meteor(canvas):
    METEOR_RADIUS = random.randint(60, 100)
    random_x = random.randint(0,CANVAS_WIDTH-METEOR_RADIUS)
    random_y = random.randint(-5000, -METEOR_RADIUS)
    meteor = canvas.create_image_with_size(random_x, random_y, METEOR_RADIUS, METEOR_RADIUS, "meteor.png")
    meteor_list.append(meteor)
    return meteor
    
def move_meteor(canvas, meteor):
    vel_meteor_x = 0
    vel_meteor_y = random.randint(3,4)
    for meteor in meteor_list:
        canvas.move(meteor, vel_meteor_x, vel_meteor_y)
        
def make_text(canvas, meteor_counter):
    text = canvas.create_text(77,28,f"Meteor\nCounter: {meteor_counter}") 
    canvas.set_color(text, "yellow")
    canvas.set_font(text, "Courier", 16)
    return text

def make_prize_text(canvas, prize_counter):
    prize_text = canvas.create_text(700,28,f"Prize\nCounter: {prize_counter}/{prize_num}") 
    canvas.set_color(prize_text, "yellow")
    canvas.set_font(prize_text, "Courier", 16)
    return prize_text

def play_game(canvas, bullet, ucak, meteor, meteor_counter, meteor_count):
    prize_counter = 0
    text = make_text(canvas, meteor_counter)
    prize_text = make_prize_text(canvas, prize_counter)
    for i in range(meteor_count):
        make_meteor(canvas)
    for a in range(prize_num):
        make_prize(canvas)    
    while True:
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
        
        for prize in prize_list:
            move_prize(canvas, prize)
                
        sonuc = check_collisions(canvas, bullet, meteor, ucak)
                
        
        if sonuc == 1:
            meteor_counter += 1
            canvas.delete(text)
            text = make_text(canvas, meteor_counter)    
            if meteor_counter > meteor_count:
                win_text = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, f"                  WELL DONE !!!\nALL METEORS HAS BEEN CLEARED \n\n                  SUCCESS: %{int(100*(prize_counter/(prize_num)))}")
                canvas.set_font(win_text, "Rockwell Extra Bold", 20)
                canvas.set_color(win_text, "purple")
                canvas.delete(prize_text)
                canvas.delete(text)
                canvas.delete(ucak)
                for bullet in list_bullet:
                    canvas.delete(bullet)
                    list_bullet.remove(bullet)
                canvas.delete(bullet)
                canvas.wait_for_click()
                time.sleep(1)
                break
        
        if sonuc == 2:
            prize_counter += 1
            canvas.delete(prize_text)
            prize_text = make_prize_text(canvas, prize_counter)
            
        
        if sonuc == False:
            text_finish = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, "GAME OVER !!!")
            canvas.set_font(text_finish, "Adobe Caslon Pro Bold", 35)
            canvas.set_color(text_finish, "red")
            canvas.wait_for_click()
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

    meteor_count = 1
    return meteor_count
    
    
def make_levels(canvas):
    rect_size_x = 150
    rect_size_y = 60
    SEP = 10
    x = CANVAS_WIDTH/2 - rect_size_x/2 
    y = CANVAS_HEIGHT/2 - rect_size_y/2

    canvas.create_image_with_size(x, y - rect_size_y - SEP, rect_size_x ,rect_size_y,"button2.png")
    canvas.create_image_with_size(x, y, rect_size_x ,rect_size_y,"button2.png")
    canvas.create_image_with_size(x, y + rect_size_y + SEP, rect_size_x ,rect_size_y,"button2.png")
    
    easy_txt = canvas.create_text(x+rect_size_x/2, y - rect_size_y + rect_size_y/2 - SEP, "EASY")
    normal_txt = canvas.create_text(x+rect_size_x/2, y +rect_size_y/2, "NORMAL")
    hard_txt = canvas.create_text(x+rect_size_x/2, y + rect_size_y + SEP + rect_size_y/2, "HARD")
    
    canvas.set_font(easy_txt, "Eras Bold ITC", 11)
    canvas.set_font(normal_txt, "Eras Bold ITC", 11)
    canvas.set_font(hard_txt, "Eras Bold ITC", 11)
    
    canvas.set_color(easy_txt, "orange")
    canvas.set_color(normal_txt, "orange")
    canvas.set_color(hard_txt, "orange")
    
  
def make_prize(canvas):
    prize = 0
    PRIZE_RADIUS = random.randint(50, 100)
    random_x = random.randint(0,CANVAS_WIDTH-PRIZE_RADIUS)
    random_y = random.randint(-4800, -PRIZE_RADIUS)
    prize = canvas.create_image_with_size(random_x, random_y, PRIZE_RADIUS, PRIZE_RADIUS, "fuel2.png")
    prize_list.append(prize)
    return prize
    
def move_prize(canvas,prize):
    velocity_x_prize= 0
    velocity_y_prize= random.randint(4,7)
    canvas.move(prize,velocity_x_prize,velocity_y_prize)

def delete_all(canvas):
    canvas.delete("all")
    meteor_list.clear()
    list_bullet.clear()
    prize_list.clear()
    
def try_again_page(canvas):
    RECT_X = 400
    RECT_Y = 150
    x = CANVAS_WIDTH/2 - RECT_X/2
    y = CANVAS_HEIGHT/2 - RECT_Y/2
    canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "fbg3.jpg")
    canvas.create_image_with_size(x, y, RECT_X, RECT_Y,"button2.png")
    try_again_text = canvas.create_text(x + RECT_X/2, y + RECT_Y/2, "TRY AGAIN")
    canvas.set_font(try_again_text, "Eras Bold ITC", 20)
    canvas.set_color(try_again_text, "orange")

def check_try_again_page(canvas):
    RECT_X = 400
    RECT_Y = 150
    x = CANVAS_WIDTH/2 - RECT_X/2
    y = CANVAS_HEIGHT/2 - RECT_Y/2
    mouse_x = canvas.get_mouse_x()
    mouse_y = canvas.get_mouse_y()
    
    if mouse_x > x and mouse_x < x + RECT_X:
        if mouse_y > y and mouse_y < y + RECT_Y:
            return 1
        
    return 0


def main ():
    canvas = Canvas(CANVAS_WIDTH,CANVAS_HEIGHT)
    while True:
        meteor_count = 0
        meteor_counter = 0
        firstbg = canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "fbg3.jpg")
        nameofgame = canvas.create_image_with_size(CANVAS_WIDTH/2-(CANVAS_HEIGHT/2),50,CANVAS_HEIGHT,120,"sf.png")
        make_levels(canvas)
        canvas.wait_for_click()
        meteor_count = check_clicks_coords(canvas)
        while meteor_count == 1:
            canvas.wait_for_click()
            meteor_count = check_clicks_coords(canvas)

        
        canvas.delete(nameofgame)
        canvas.delete(firstbg)
        
        canvas.create_image_with_size(0,0, CANVAS_WIDTH, CANVAS_HEIGHT, "space 3.jpg")
        ucak = make_plane(canvas)
        bullet = make_bullet(canvas)
        meteor = make_meteor(canvas)
        prize = make_prize(canvas)
        
        canvas.delete(bullet)
        canvas.delete(prize)
    
        text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 , "YOU NEED TO SHOOT ALL OF THE METEORS\n             DON'T ESPCAPE FROM THEM\n      AND TRY TO TAKE ALL OF THE FUELS")
    
        canvas.set_font(text, "Stencil", 20)
        canvas.set_color(text, "red")
        canvas.wait_for_click()
        canvas.delete(text)
        
        play_game(canvas, bullet, ucak, meteor, meteor_counter, meteor_count)
        
        delete_all(canvas)
        try_again_page(canvas)
        canvas.wait_for_click()
        sonuc = check_try_again_page(canvas)
        while sonuc != 1:
            canvas.wait_for_click()
            sonuc = check_try_again_page(canvas)
        
    
    canvas.mainloop()
    
    
if __name__ == '__main__':
    main()    
    