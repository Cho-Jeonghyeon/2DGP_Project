from pico2d import *

import game_framework
import game_mode

stage1 = None
background = None

def init():
    global stage1, background
    stage1 = load_image('plant_1.png')
    background = load_image('main_background.png')
def finish():
    global stage1, background
    del stage1, background

def update():
    pass

def draw():
    clear_canvas()
    background.draw(600, 500)
    stage1.draw(200, 200)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_MOUSEBUTTONDOWN:
            game_framework.change_mode(game_mode)

def pause():
    pass
def resume():
    pass