from pico2d import *

import game_framework
import game_world


def init():
    global clear
    clear = load_image('UI/clear_ui.png')

def finish():
    pass

def update():

    pass

def draw():

    clear.draw(600, 500, 600,600)  # 정중앙
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            game_framework.pop_mode()  # SPACE 눌러 나가기
        elif e.type == SDL_QUIT:
            game_framework.quit()


def pause():
    pass

def resume():
    pass

