from pico2d import *
import game_framework
from planet1 import *

class SpaceshipGame:
    def __init__(self, planet=None):
        self.x, self.y = 600, 200
        self.image = load_image('images/spaceship_level_1.png')
        self.speed = 400
        self.dy = 0
        self.planet = planet

    def update(self):
        # game_world.update() will call this without arguments
        if self.planet:
            self.planet.update(self.dy * game_framework.frame_time)


    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                self.dy = 200
            elif event.key == SDLK_DOWN:
                self.dy = -200
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_UP, SDLK_DOWN):
                self.dy = 0
