# spaceship_game.py
from pico2d import *
import game_framework
import math

from drill import Drill
from planet1 import TILE, SCREEN_W, SCREEN_H

class Spaceship:
    def __init__(self, planet):
        self.planet = planet

        # ===== World 좌표 (절대 위치) =====
        self.world_x = (planet.world_width // 2)
        self.world_y = planet.world_height - 200   # 시작은 맨 위 근처

        # ===== Movement =====
        self.angle = -math.pi / 2           # 처음엔 아래쪽
        self.speed = 250
        self.dx = 0
        self.dy = 0

        # ===== Drill =====
        self.drill_offset = 60
        self.drill = Drill()

        # ===== Camera =====
        self.camera_x = 0
        self.camera_y = self.world_y - SCREEN_H // 2

        self.image = load_image('images/spaceship_level_1.png')

    # ===============================================
    # Input
    # ===============================================
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT: self.dx = +1
            if event.key == SDLK_LEFT:  self.dx = -1
            if event.key == SDLK_UP:    self.dy = +1
            if event.key == SDLK_DOWN:  self.dy = -1

        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT): self.dx = 0
            if event.key in (SDLK_UP, SDLK_DOWN):     self.dy = 0

    # ===============================================
    # Update
    # ===============================================
    def update(self):
        frame_time = game_framework.frame_time

        # ---------------------
        # 1) World 좌표 이동
        # ---------------------
        self.world_x += self.dx * self.speed * frame_time
        self.world_y += self.dy * self.speed * frame_time

        # 가로 world clamp
        self.world_x = clamp(0, self.world_x, self.planet.world_width)

        # ---------------------
        # 2) Drill world 위치
        # ---------------------
        self.angle = math.atan2(self.dy, self.dx) if (self.dx or self.dy) else self.angle

        drill_world_x = self.world_x + math.cos(self.angle) * self.drill_offset
        drill_world_y = self.world_y + math.sin(self.angle) * self.drill_offset

        # ---------------------
        # 3) 타일 파괴 (world 좌표)
        # ---------------------
        hit = self.planet.destroy(drill_world_x, drill_world_y,
                                  damage=self.drill.damage, radius=1)

        # ---------------------
        # 4) bounce(반동)
        # ---------------------
        if hit:
            bounce = 80 * frame_time
            self.world_x -= math.cos(self.angle) * bounce
            self.world_y -= math.sin(self.angle) * bounce

        # ---------------------
        # 5) Camera follow
        # ---------------------
        target_camera_y = self.world_y - SCREEN_H // 2
        self.camera_y = target_camera_y

        # Camera clamp
        max_cam_y = self.planet.world_height - SCREEN_H
        self.camera_y = clamp(0, self.camera_y, max_cam_y)

        # ---------------------
        # 6) Drill update
        # ---------------------
        self.drill.update()

    # ===============================================
    # Draw
    # ===============================================
    def draw(self):
        # ===== world → screen 변환 =====
        screen_x = self.world_x - self.camera_x
        screen_y = self.world_y - self.camera_y

        # world의 top/bottom에서는 screen_y가 고정에서 벗어남
        self.image.rotate_draw(self.angle - math.pi/2,
                               screen_x, screen_y,
                               70, 70)

        # Drill draw
        drill_world_x = self.world_x + math.cos(self.angle) * self.drill_offset
        drill_world_y = self.world_y + math.sin(self.angle) * self.drill_offset

        drill_screen_x = drill_world_x - self.camera_x
        drill_screen_y = drill_world_y - self.camera_y

        self.drill.draw(drill_screen_x, drill_screen_y, self.angle)



# from pico2d import *
# import math
# import game_framework
# from drill import Drill
#
# class SpaceshipGame:
#     def __init__(self, planet):
#         self.x, self.y = 600, 900
#         self.speed = 150
#         self.image = load_image('images/spaceship_level_1.png')
#
#         self.dx, self.dy = 0, 0
#         self.angle = 0
#
#         self.drill = Drill()
#         self.drill_offset = 50
#
#         self.planet = planet
#
#     def update(self):
#         # 좌우 이동
#         self.x += self.dx * self.speed * game_framework.frame_time
#         self.x = clamp(50, self.x, 1150)
#
#         scroll_speed = self.dy * self.speed * game_framework.frame_time
#         target_y = 400
#
#         # 타일맵 기반 스크롤
#         max_scroll = self.planet.total_height - 1000
#
#         # === 타일 파괴 ===
#         drill_x = self.x + math.cos(self.angle) * self.drill_offset
#         drill_y = self.y + math.sin(self.angle) * self.drill_offset
#
#         hit = self.planet.destroy(drill_x, drill_y, radius=1, damage=self.drill.damage)
#         print(hit)
#         if hit:
#             bounce = 30 * game_framework.frame_time
#             self.x -= math.cos(self.angle) * bounce
#             self.y -= math.sin(self.angle) * bounce
#         else:
#
#             if (self.dy > 0 and self.planet.scroll_y < max_scroll) or \
#                (self.dy < 0 and self.planet.scroll_y > 0):
#
#                 self.planet.scroll_y += scroll_speed
#                 self.planet.scroll_y = clamp(0, self.planet.scroll_y, max_scroll)
#
#                 lerp = 0.25 * game_framework.frame_time
#                 self.y = self.y * (1 - lerp) + target_y * lerp
#
#             else:
#                 if self.dx == 0 and self.dy == 0:
#                     fall_speed = 15* game_framework.frame_time
#                     fall_speed2 = 25* game_framework.frame_time
#
#                     self.y -= fall_speed
#                     self.planet.scroll_y -= fall_speed2
#
#                     self.y = clamp(70, self.y, 950)
#                     self.planet.scroll_y = clamp(0, self.planet.scroll_y, max_scroll)
#
#                 else:
#                     self.y += self.dy * self.speed * game_framework.frame_time
#                     self.y = clamp(70, self.y, 950)
#
#             if self.dx != 0 or self.dy != 0:
#                 self.angle = math.atan2(self.dy, self.dx)
#
#         self.drill.update()
#
#     def draw(self):
#         draw_angle = self.angle - math.pi / 2
#         self.image.rotate_draw(draw_angle, self.x, self.y, 70, 70)
#
#         drill_x = self.x + math.cos(self.angle) * self.drill_offset
#         drill_y = self.y + math.sin(self.angle) * self.drill_offset
#
#         self.drill.draw(drill_x, drill_y, draw_angle)
#
#
#     def handle_events(self, event):
#         if event.type == SDL_KEYDOWN:
#             if event.key == SDLK_RIGHT: self.dx = 1
#             elif event.key == SDLK_LEFT: self.dx = -1
#             elif event.key == SDLK_UP: self.dy = 1
#             elif event.key == SDLK_DOWN: self.dy = -1
#
#         elif event.type == SDL_KEYUP:
#             if event.key in (SDLK_RIGHT, SDLK_LEFT): self.dx = 0
#             if event.key in (SDLK_UP, SDLK_DOWN): self.dy = 0
