from pico2d import *
import game_framework
import gameover_mode
import item_mode
from spaceship import Spaceship

background_level_1 = None
spaceship = None

def init():
    global background_level_1, spaceship
    background_level_1 = load_image('background2.png')
    spaceship = Spaceship()

def finish():
    global background_level_1, spaceship
    del background_level_1, spaceship

def update():
    pass

def draw():
    clear_canvas()
    background_level_1.draw(400, 300)
    spaceship.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(gameover_mode)

def pause():
    pass
def resume():
    pass