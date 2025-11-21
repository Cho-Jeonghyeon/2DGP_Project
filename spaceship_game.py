from pico2d import *
import math
import game_framework
from drill import Drill

class SpaceshipGame:
    def __init__(self, planet):
        self.x, self.y = 600, 900
        self.speed = 150
        self.image = load_image('images/spaceship_level_1.png')

        self.dx, self.dy = 0, 0
        self.angle = 0

        self.drill = Drill()
        self.drill_offset = 50

        self.planet = planet

    def update(self):
        # 좌우 이동
        self.x += self.dx * self.speed * game_framework.frame_time
        self.x = clamp(50, self.x, 1150)

        scroll_speed = self.dy * self.speed * game_framework.frame_time
        target_y = 400

        # 타일맵 기반 스크롤
        max_scroll = self.planet.total_height - 1000

        if (self.dy > 0 and self.planet.scroll_y < max_scroll) or \
           (self.dy < 0 and self.planet.scroll_y > 0):

            self.planet.scroll_y += scroll_speed
            self.planet.scroll_y = clamp(0, self.planet.scroll_y, max_scroll)

            lerp = 0.25 * game_framework.frame_time
            self.y = self.y * (1 - lerp) + target_y * lerp

        else:
            if self.dx == 0 and self.dy == 0:
                self.y -= 30 * game_framework.frame_time
                self.y = clamp(70, self.y, 950)
            else:
                self.y += self.dy * self.speed * game_framework.frame_time
                self.y = clamp(70, self.y, 950)

        if self.dx != 0 or self.dy != 0:
            self.angle = math.atan2(self.dy, self.dx)

        self.drill.update()

    def draw(self):
        draw_angle = self.angle - math.pi / 2
        self.image.rotate_draw(draw_angle, self.x, self.y, 70, 70)

        drill_x = self.x + math.cos(self.angle) * self.drill_offset
        drill_y = self.y + math.sin(self.angle) * self.drill_offset

        self.drill.draw(drill_x, drill_y, draw_angle)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT: self.dx = 1
            elif event.key == SDLK_LEFT: self.dx = -1
            elif event.key == SDLK_UP: self.dy = 1
            elif event.key == SDLK_DOWN: self.dy = -1

        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT): self.dx = 0
            if event.key in (SDLK_UP, SDLK_DOWN): self.dy = 0
