from pico2d import *

import game_framework
import game_mode_1
import game_mode_2
import game_mode_3
import game_world
from stage_button import StageButton
from background import Background

background = None

def init():
    global  background

    background = Background('main_background.png')
    stage1 = StageButton('plant_1.png', 200, 200, 200, 200, game_mode_1)
    stage2 = StageButton('plant_2.png', 400, 200, 200, 200, game_mode_2)
    stage3 = StageButton('plant_3.png', 600, 200, 200, 200, game_mode_3)

    game_world.add_object(background, 0)
    game_world.add_objects([stage1, stage2, stage3], 1)

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
        if event.type == SDL_MOUSEBUTTONDOWN:
            mx, my = event.x, 1000 - event.y  # 좌표 변환

            print(f"Mouse click: ({mx}, {my})")  #  클릭 좌표 디버깅

            for obj in game_world.world[1]:  # 버튼 레이어
                if isinstance(obj, StageButton) and obj.is_clicked(mx, my):
                    print(f" {obj.stage_mode}")  #  연결된 모드 확인
                    game_framework.change_mode(obj.stage_mode)

def pause():
    pass
def resume():
    pass