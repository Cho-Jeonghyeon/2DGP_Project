from pico2d import *

import game_framework
import game_world
import stage_mode

upgrade = None


def init():
    global upgrade
    global ui_spaceship, ui_heart, ui_atk, ui_def, ui_line
    global ui_inform, ui_info
    upgrade = load_image('images/upgrade_mode.png')
    ui_spaceship = load_image('UI/ui_spaceship.png')
    ui_heart = load_image('UI/ui_heart.png')
    ui_atk = load_image('UI/ui_atk.png')
    ui_def = load_image('UI/ui_def.png')
    ui_line = load_image('UI/ui_line.png')
    ui_inform = load_image('UI/upgrade_inform.png')
    ui_info = load_image('UI/upgrade_info.png')

def finish():
    pass

def update():
    pass

def draw():
    upgrade.draw(600, 500, 1100, 926)    # 중앙에 패널 띄우기

    # =============================
    # 아이콘 좌표 (1000x920 기준)
    # =============================
    ship_x, ship_y = 350, 500
    def_x, def_y = 350, 660
    heart_x, heart_y = 230, 420
    atk_x, atk_y = 470, 420


    # =============================
    # 아이콘 그리기
    # =============================
    ui_spaceship.draw(ship_x, ship_y, 160, 160)
    ui_heart.draw(heart_x, heart_y, 160, 160)
    ui_atk.draw(atk_x, atk_y, 160, 160)
    ui_def.draw(def_x, def_y, 160, 160)
    ui_inform.draw(850, 650, 450, 500)
    ui_info.draw(850, 775, 165, 165)
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

        # elif event.type == SDL_MOUSEMOTION:
        #     mx, my = event.x, 1000 - event.y
        #     # hover 감지
        #     if button.is_clicked(mx, my):
        #         button.is_hover = True
        #     else:
        #         button.is_hover = False
        #
        # elif event.type == SDL_MOUSEBUTTONDOWN:
        #     mx, my = event.x, 1000 - event.y
        #     if button.is_clicked(mx, my):
        #         game_framework.change_mode(stage_mode)

def pause():
    pass
def resume():
    pass

