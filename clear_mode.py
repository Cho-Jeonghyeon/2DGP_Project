from pico2d import *

import game_data
import stage_mode
from planet1 import Planet
import game_framework
import game_world

show_step = 0         # 0 → 아무것도 안보임
show_timer = 0        # 시간 누적값
blink_timer = 0

def init():
    global clear, font, font2, rock1, rock2, rock3, rock4
    clear = load_image('UI/clear_ui.png')
    font = load_font('fonts/MaplestoryBold.ttf', 60)
    font2 = load_font('fonts/MaplestoryLight.ttf', 30)
    rock1 = load_image('images/1.png')
    rock2 = load_image('images/2.png')
    rock3 = load_image('images/3.png')
    rock4 = load_image('images/4.png')

def finish():
    pass

def update():
    global show_timer, show_step, blink_timer
    show_timer += game_framework.frame_time
    blink_timer += game_framework.frame_time

    # 0.5초마다 하나씩 증가
    if show_timer > 0.5 and show_step < 4.5:
        show_step += 1
        show_timer = 0

def draw():

    clear.draw(600, 500, 600,600)

    font.draw(460, 550, '획득한 자원', (255, 255, 255))

    # rock1
    if show_step >= 1:
        rock1.draw(450, 450, 40,40)
        font2.draw(425, 400, f"{game_data.rock_break_count[1] + 100}", (255,255,255))

    # rock2
    if show_step >= 2:
        rock2.draw(550, 450, 40,40)
        font2.draw(525, 400, f"{game_data.rock_break_count[2] + 100}", (255,255,255))

    # rock3
    if show_step >= 3:
        rock3.draw(650, 450, 40,40)
        font2.draw(625, 400, f"{game_data.rock_break_count[3] + 100}", (255,255,255))

    # rock4
    if show_step >= 4:
        rock4.draw(750, 450, 40,40)
        font2.draw(730, 400, f"{game_data.rock_break_count[4]}", (255,255,255))

    if show_step >= 4.5:
        if (blink_timer % 1.0) < 0.5:
            font2.draw(500, 300, 'Press SPACE', (255, 255, 255))

    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            game_framework.pop_mode()  # SPACE 눌러 나가기
            stage_mode.stage_x, stage_mode.stage_y = None, None
            game_framework.change_mode(stage_mode)
        elif e.type == SDL_QUIT:
            game_framework.quit()


def pause():
    pass

def resume():
    pass

