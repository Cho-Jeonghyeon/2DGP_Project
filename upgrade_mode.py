from pico2d import *

import game_framework
import game_world
import stage_mode

upgrade = None

def init():
    global upgrade
    global ui_spaceship, ui_heart, ui_atk, ui_def, ui_line

    upgrade = load_image('images/upgrade_mode.png')
    ui_spaceship = load_image('UI/ui_spaceship.png')
    ui_heart = load_image('UI/ui_heart.png')
    ui_atk = load_image('UI/ui_atk.png')
    ui_def = load_image('UI/ui_def.png')
    ui_line = load_image('UI/ui_line.png')

def finish():
    pass

def update():
    pass

def draw():

    upgrade.draw(600, 500)      # 배경 그리기
    # ui_spaceship.draw(450, 600)
    # ui_heart.draw(350, 480)
    # ui_atk.draw(550, 480)
    # ui_def.draw(450, 360)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(stage_mode)

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

