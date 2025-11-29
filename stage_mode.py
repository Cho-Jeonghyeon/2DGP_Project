from pico2d import *

import game_framework
import game_mode_1
import game_mode_2
import game_mode_3
import game_world
import upgrade_mode
from stage_button import *
from background import Background
from spaceship import Spaceship

background = None
spaceship = None
stage_x = None
stage_y = None

def init():
    global  background, spaceship
    global stage_x, stage_y
    background = Background('images/main_background.png', speed=60)
    stage1 = Plant('images/ice_plant.png', 200, 800, 300, 300, game_mode_1)
    stage2 = Plant('images/lava_plant.png', 600, 800, 300, 300, game_mode_2)
    stage3 = Plant('images/gas_plant.png', 1000, 800, 300, 300, game_mode_3)

    upgrade = UpgradeButton('images/upgrade.png', 425, 100, 250, 100, upgrade_mode)
    equipment = UpgradeButton('images/equip.png', 775, 100, 250, 100, upgrade_mode)
    if stage_x is None and stage_y is None:
        stage_x , stage_y= 600,400
    spaceship = Spaceship(stage_x,stage_y)

    game_world.add_object(background, 0)
    game_world.add_objects([stage1, stage2, stage3, upgrade, equipment], 1)
    game_world.add_objects([spaceship], 2)

def finish():
    game_world.clear()

def update():
    global stage_x, stage_y
    game_world.update()

    for obj in game_world.world[1]:
        if isinstance(obj, Plant):
            obj.is_glow = False

    for obj in game_world.world[1]:
        if isinstance(obj, Plant):
            if collide(spaceship, obj):
                game_framework.change_mode(obj.stage_mode)
            elif collide2(spaceship, obj):
                obj.is_glow = True
        elif isinstance(obj, UpgradeButton):
            if collide(spaceship, obj):
                stage_x = spaceship.x
                stage_y = spaceship.y
                game_framework.push_mode(obj.stage_mode)

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
        spaceship.handle_events(event)

def pause():
    pass
def resume():
    pass

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide2(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb2()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True