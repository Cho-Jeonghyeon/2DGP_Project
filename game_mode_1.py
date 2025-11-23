# game_mode_1.py

from pico2d import *
import game_framework
import game_world

from planet1 import Planet
from spaceship_game import Spaceship
from background import Background

# ======================================
# 맵 로딩 함수
# ======================================
def load_map(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            row = list(map(int, line.split()))
            data.append(row)
    data.reverse()
    return data


# ======================================
# GAME MODE 1
# ======================================
planet = None
spaceship = None
background = None

def init():
    enter()

def enter():
    global planet, spaceship, background

    # 1) 맵 로딩
    map_data = load_map('planet_map_test.txt')

    # 2) Planet 생성
    planet = Planet(map_data)

    # 3) Spaceship 생성
    spaceship = Spaceship(planet)
    background = Background('images/level1_background.png', 60)
    game_world.add_object(background, 0)

def finish():
    game_world.clear()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        else:
            spaceship.handle_event(event)


def update():
    game_world.update()
    spaceship.update()


def draw():
    clear_canvas()
    game_world.render()
    # 먼저 Planet을 camera 기준으로 그린다
    planet.draw(spaceship.camera_x, spaceship.camera_y)

    # 그 뒤 Spaceship을 화면(screen) 기준으로 그린다
    spaceship.draw()

    update_canvas()




# from pico2d import *
# import game_framework
# import gameover_mode
# from spaceship_game import *
# import game_world
# from background import Background
# from planet1 import Planet
#
# planet = None
# background = None
# spaceship = None
#
# def init():
#     global background, spaceship, planet
#
#     background = Background('images/level1_background.png')
#
#     planet = Planet()
#     spaceship = SpaceshipGame(planet)
#
#     game_world.add_object(background, 0)
#     game_world.add_object(planet, 1)
#     game_world.add_object(spaceship, 1)
#
# def finish():
#     game_world.clear()
#
# def update():
#     spaceship.update()
#     game_world.update()
#
# def draw():
#     clear_canvas()
#     game_world.render()
#     update_canvas()
#
# def handle_events():
#     events = get_events()
#     for event in events:
#         if event.type == SDL_QUIT:
#             game_framework.quit()
#         elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
#             game_framework.change_mode(gameover_mode)
#         else:
#             spaceship.handle_events(event)
#
# def pause():
#     pass
#
# def resume():
#     pass
