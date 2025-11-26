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

ui_rock1 = None
ui_rock2 = None
ui_rock3 = None
ui_rock_penel = None
ui_font = None
ui_font2 = None

ui_hp_exp = None
ui_level = None

hp_left = None
hp_mid = None
hp_right = None

exp_left = None
exp_mid = None
exp_right = None

def init():
    enter()

def enter():
    global planet, spaceship, background
    global ui_rock1, ui_rock_penel, ui_font, ui_rock2, ui_rock3, ui_font2
    global ui_level, ui_hp_exp
    global hp_left, hp_mid, hp_right
    global exp_left, exp_mid, exp_right

    # 1) 맵 로딩
    map_data = load_map('planet_map_test.txt')

    # 2) Planet 생성
    planet = Planet(map_data)

    # 3) Spaceship 생성
    spaceship = Spaceship(planet)
    background = Background('images/level1_background.png', 60)
    game_world.add_object(background, 0)

    ui_rock1 = load_image('UI/rock_ui2_1.png')
    ui_rock2 = load_image('UI/rock_ui2_2.png')
    ui_rock3 = load_image('UI/rock_ui2_3.png')

    ui_rock_penel = load_image('UI/rock_ui.png')
    ui_font = load_font('fonts/MaplestoryBold.ttf', size=15)
    ui_font2 = load_font('fonts/MaplestoryBold.ttf', size=23)

    ui_hp_exp = load_image('UI/hp_exp_ui.png')
    ui_level = load_image('UI/level_ui.png')

    hp_left = load_image('UI/ui_hp_left.png')
    hp_mid = load_image('UI/ui_hp_mid.png')
    hp_right = load_image('UI/ui_hp_right.png')

    exp_left = load_image('UI/ui_exp_left.png')
    exp_mid = load_image('UI/ui_exp_mid.png')
    exp_right = load_image('UI/ui_exp_right.png')

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
    draw_rock_ui(planet)
    draw_hp_exp_level_ui(spaceship)
    draw_hp_bar(spaceship)
    draw_exp_bar(spaceship)

    update_canvas()


def draw_rock_ui(plant):
    num = plant.rock_count
    base_x = SCREEN_W - 120  # 패널 left
    base_y = SCREEN_H - 200  # 패널 center
    ui_rock_penel.draw(base_x, base_y, 130,120)

    ui_rock_locate_x = base_x + 85
    ui_rock_locate_y = base_y + 40
    slot_gap = 40

    ui_rock_images = [ui_rock1, ui_rock2, ui_rock3]
    for i in range (3):
        img = ui_rock_images[i]
        img.draw(ui_rock_locate_x, ui_rock_locate_y-i*slot_gap, 40,40)

    names = ["Stone", "Iron", "Ruby"]
    for i, name in enumerate(names, start=1):
        ui_font.draw(base_x - 40, ui_rock_locate_y - (i - 1) * slot_gap, f"{name} : {num[i]}",(0,0,0))


def draw_hp_exp_level_ui(spaceship):

    base_x = 520
    base_y = 945

    ui_hp_exp.draw(base_x, base_y,1000,70)
    ui_level.draw(base_x - 450, base_y - 60)

    ui_font2.draw(base_x - 490, base_y - 60, f'LV : {spaceship.level}', (0, 0, 0))


def draw_hp_bar(spaceship):
    # HP 퍼센트
    hp_ratio = spaceship.hp / spaceship.max_hp
    hp_ratio = max(0, min(1, hp_ratio))

    # 바 위치 (상단)
    base_x = 520
    base_y = 961


    full_width = 990   #전체 체력바 길이
    mid_width = int((full_width - hp_left.w - hp_right.w) * hp_ratio)

    # HP 바의 실제 시작점
    left_x  = base_x - full_width // 2
    mid_x   = left_x + hp_left.w
    right_x = mid_x  + mid_width-2

    # 그리기
    hp_left.draw(left_x + hp_left.w//2, base_y)
    hp_mid.draw(mid_x + mid_width//2, base_y, mid_width, hp_mid.h)
    hp_right.draw(right_x + hp_right.w//2, base_y)

    ui_font.draw(520, 960, f'{spaceship.hp}  /  {spaceship.max_hp}', (0,0,0))

def draw_exp_bar(spaceship):

    # exp 퍼센트
    exp_ratio = spaceship.exp / spaceship.max_exp
    exp_ratio = max(0, min(1, exp_ratio))

    # 바 위치 (상단)
    base_x = 520
    base_y = 931

    full_width = 990  # 전체 체력바 길이
    mid_width = int((full_width - exp_left.w - exp_right.w) * exp_ratio)

    # exp 바의 실제 시작점
    left_x = base_x - full_width // 2
    mid_x = left_x + hp_left.w
    right_x = mid_x + mid_width - 2

    # 그리기
    exp_left.draw(left_x + exp_left.w // 2, base_y)
    exp_mid.draw(mid_x + mid_width // 2, base_y, mid_width, exp_mid.h)
    exp_right.draw(right_x + exp_right.w // 2, base_y)

    ui_font.draw(520, 930, f'{spaceship.exp}  /  {spaceship.max_exp}', (0, 0, 0))