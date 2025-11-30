from pico2d import *

import game_framework
import game_world
import stage_mode
from game_mode_1 import ui_font

upgrade = None
SIZE = 30
selected = None

def init():
    global upgrade
    global ui_spaceship, ui_heart, ui_atk, ui_def
    global ui_inform, ui_info, ui_font
    upgrade = load_image('images/upgrade_mode.png')

    ui_spaceship = load_image('UI/ui_spaceship.png')
    ui_heart = load_image('UI/ui_heart.png')
    ui_atk = load_image('UI/ui_atk.png')
    ui_def = load_image('UI/ui_def.png')

    ui_inform = load_image('UI/upgrade_inform.png')
    ui_info = load_image('UI/upgrade_info.png')
    global SIZE
    ui_font = load_font('fonts/MaplestoryBold.ttf', SIZE)

def clicked(px, py, cx, cy, w, h):
    return (cx - w/2 < px < cx + w/2) and (cy - h/2 < py < cy + h/2)

def finish():
    pass

def update():
    pass

# 아이콘 위치
ship_pos = (350, 500)
def_pos  = (350, 660)
heart_pos = (230, 420)
atk_pos = (470, 420)
UI_SIZE = 160

def draw():

    upgrade.draw(600, 500, 1100, 926)    # 중앙에 패널 띄우기

    # --- 왼쪽 스킬 아이콘 ---
    ui_spaceship.draw(*ship_pos, UI_SIZE, UI_SIZE)
    ui_heart.draw(*heart_pos, UI_SIZE, UI_SIZE)
    ui_atk.draw(*atk_pos, UI_SIZE, UI_SIZE)
    ui_def.draw(*def_pos, UI_SIZE, UI_SIZE)

    # --- 오른쪽 패널 ---
    ui_inform.draw(850, 650, 450, 500)
    ui_info.draw(850, 775, 175, 175)

    if selected == 'atk':

        ui_atk.draw(850, 775, 160, 160)
        ui_font.draw(760, 650, '< 공격력 증가 >', (180, 255, 255))
        ui_font.draw(795, 600, '0   ->   5', (180, 255, 255))
        ui_font.draw(795, 550, '12   /   50', (180, 255, 255))

    elif selected == 'heart':

        ui_heart.draw(850, 775, 160, 160)
        ui_font.draw(775, 650, '< 체력 증가 >', (180, 255, 255))
        ui_font.draw(795, 600, '0   ->   5', (180, 255, 255))
        ui_font.draw(795, 550, '12   /   50', (180, 255, 255))

    elif selected == 'def':

        ui_def.draw(850, 775, 160, 160)
        ui_font.draw(760, 650, '< 방어력 증가 >', (180, 255, 255))
        ui_font.draw(795, 600, '0   ->   5', (180, 255, 255))
        ui_font.draw(795, 550, '12   /   50', (180, 255, 255))

    elif selected == 'ship':

        ui_spaceship.draw(850, 775, 160, 160)
        ui_font.draw(760, 650, '< 우주선 강화 >', (180, 255, 255))
        ui_font.draw(795, 600, '0   ->   5', (180, 255, 255))
        ui_font.draw(795, 550, '12   /   50', (180, 255, 255))


    # ui_font.draw(780, 660, f'공격력  증가', (180, 255, 255))
    # ui_font.draw(795, 660-SIZE-20, f'0  ->  5', (180, 255, 255))
    # ui_font.draw(795, 660-SIZE*2-40, f'12  /  50', (180, 255, 255))

    update_canvas()


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if stage_mode.spaceship and stage_mode.stage_x!= None:
                #print("디버깅")
                ship = stage_mode.spaceship
                ship.x = stage_mode.stage_x
                ship.y = stage_mode.stage_y

                ship.dx = 0
                ship.dy = 0

                ship.y += 40  # 충돌 방지 offset
                ship.key_left = ship.key_right = False
                ship.key_up = ship.key_down = False
                game_framework.pop_mode()

        elif event.type == SDL_MOUSEBUTTONDOWN:
            global selected
            mx, my = event.x, 1000 - event.y

            if clicked(mx, my, *atk_pos, UI_SIZE, UI_SIZE):
                selected = 'atk'
            elif clicked(mx, my, *heart_pos, UI_SIZE, UI_SIZE):
                selected = 'heart'
            elif clicked(mx, my, *def_pos, UI_SIZE, UI_SIZE):
                selected = 'def'
            elif clicked(mx, my, *ship_pos, UI_SIZE, UI_SIZE):
                selected = 'ship'


def pause():
    pass
def resume():
    pass

