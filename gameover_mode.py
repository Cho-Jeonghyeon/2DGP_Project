from pico2d import *
import game_framework
import game_world
import stage_mode
from background import Background


def init():
    global background
    background = Background('images/gameover.png')
    game_world.add_object(background, 0)

def finish():
    game_world.clear()

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(stage_mode)

def pause():
    pass
def resume():
    pass