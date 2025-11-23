# game_mode_1.py

from pico2d import *
import game_framework
import game_world

from planet1 import *
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
ui_rock = None
ui_rock_penel = None
ui_font = None

def init():
    enter()

def enter():
    global planet, spaceship, background, ui_rock, ui_rock_penel, ui_font

    # 1) 맵 로딩
    map_data = load_map('planet_map_test.txt')

    # 2) Planet 생성
    planet = Planet(map_data)

    # 3) Spaceship 생성
    spaceship = Spaceship(planet)
    background = Background('images/level1_background.png', 60)
    game_world.add_object(background, 0)

    ui_rock = load_image('images/rock_ui2_1.png')
    ui_rock_penel = load_image('images/rock_ui.png')
    ui_font = load_font('fonts/MaplestoryBold.ttf', 18)

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
    draw_ui(planet)
    update_canvas()


def draw_ui(plant):
    num = plant.rock_count
    base_x = SCREEN_W - 170  # 패널 left
    base_y = SCREEN_H - 250  # 패널 center
    ui_rock_penel.draw(base_x, base_y, 250,160)

    ui_rock_locate_x = base_x + 140
    ui_rock_locate_y = base_y + 60
    slot_gap = 40

    for i in range (4):
        ui_rock.draw(ui_rock_locate_x, ui_rock_locate_y-i*slot_gap, 40,40)

    names = ["Stone", "Iron", "Ruby", "Crystal"]
    for i, name in enumerate(names, start=1):
        ui_font.draw(base_x - 80, ui_rock_locate_y - (i - 1) * slot_gap, f"{name} : {num[i]}",(0,0,0))
