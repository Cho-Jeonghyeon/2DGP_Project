from pico2d import *

import game_framework
import game_mode

image = None

def init():
    global image
    image = load_image('plant1.png')

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(200, 200)
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