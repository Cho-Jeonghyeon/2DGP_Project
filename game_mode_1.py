from pico2d import *
import game_framework
import gameover_mode
from spaceship_game import *
import game_world
from background import Background
from planet1 import Planet

planet = None
background = None
spaceship = None

def init():
    global background, spaceship, planet

    background = Background('images/level1_background.png')

    planet = Planet()
    spaceship = SpaceshipGame(planet)

    game_world.add_object(background, 0)
    game_world.add_object(planet, 1)
    game_world.add_object(spaceship, 1)

def finish():
    game_world.clear()

def update():
    spaceship.update()
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(gameover_mode)
        else:
            spaceship.handle_events(event)

def pause():
    pass

def resume():
    pass
