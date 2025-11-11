from pico2d import *
import game_framework
import game_world
import stage_mode
from background import Background
from stage_button import Button


def init():
    global gamestart, button
    gamestart = Background('images/game_start.png')
    button = Button('images/start.png', 600, 180, 300, 80)

    game_world.add_object(gamestart, 0)
    game_world.add_object(button, 1)

def finish():
    game_world.clear()


def update():
    pass

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
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mx, my = event.x, 1000 - event.y
            if button.is_clicked(mx, my):
                print("게임 시작 버튼 클릭됨!")
                game_framework.change_mode(stage_mode)

def pause():
    pass
def resume():
    pass