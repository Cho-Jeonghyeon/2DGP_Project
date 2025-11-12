from pico2d import *
import game_framework
import game_world
import stage_mode
from background import Background
from stage_button import Button

logo = None
char = None

def init():
    global gamestart, button, logo, char
    gamestart = Background('images/main_background.png')
    button = Button('images/start.png', 600, 180, 300, 80)
    logo = load_image('images/plantcrusher.png')
    char = load_image('images/spaceship_level_3.png')
    game_world.add_object(gamestart, 0)
    game_world.add_object(button, 1)

def finish():
    game_world.clear()


def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    logo.draw(600,800)
    char.draw(600,450, 200,200)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 1000 - event.y
            # hover 감지
            if button.is_clicked(mx, my):
                button.is_hover = True
            else:
                button.is_hover = False

        elif event.type == SDL_MOUSEBUTTONDOWN:
            mx, my = event.x, 1000 - event.y
            if button.is_clicked(mx, my):
                game_framework.change_mode(stage_mode)
def pause():
    pass
def resume():
    pass