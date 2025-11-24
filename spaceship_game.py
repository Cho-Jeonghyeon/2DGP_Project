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

        self.hp = 400
        self.max_hp = 400

    def get_bb(self):
        screen_x = self.world_x - self.camera_x
        screen_y = self.world_y - self.camera_y
        return screen_x-30, screen_y-30, screen_x+30, screen_y+30

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

    # def check_collision_with_tiles(self):
    #     # 우주선 bounding box (screen 기준)
    #     left, bottom, right, top = self.get_bb()
    #
    #     # 우주선 bounding box → world 좌표로 바꾸기
    #     world_left = left + self.camera_x
    #     world_bottom = bottom + self.camera_y
    #     world_right = right + self.camera_x
    #     world_top = top + self.camera_y
    #
    #     # 우주선이 걸쳐 있는 타일 범위
    #     tile_left = int(world_left // TILE)
    #     tile_right = int(world_right // TILE)
    #     tile_bottom = int(world_bottom // TILE)
    #     tile_top = int(world_top // TILE)
    #
    #     damage_sum = 0
    #
    #     for r in range(tile_bottom, tile_top + 1):
    #         for c in range(tile_left, tile_right + 1):
    #             if 0 <= r < self.planet.MAP_H and 0 <= c < self.planet.MAP_W:
    #                 tile = self.planet.map[r][c]
    #                 if tile != 0:  # 타일이 존재함
    #                     # 데미지 누적
    #                     damage_sum += self.planet.tile_damage[r][c]
    #
    #     return damage_sum

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
        hit, tile_damage = self.planet.destroy(drill_world_x, drill_world_y,
                                  damage=self.drill.damage, radius=1)


        # ---------------------
        # 4) bounce(반동)
        # ---------------------
        if hit:
            self.hp -= tile_damage
            print(self.hp)
            # bounce = 1500 * frame_time
            # self.world_x -= math.cos(self.angle) * bounce
            # self.world_y -= math.sin(self.angle) * bounce
            self.drill.hit_timer = 0.08
            bounce = 600 * frame_time + 20
            self.world_x -= math.cos(self.angle) * bounce
            self.world_y -= math.sin(self.angle) * bounce


        # if hit:
        #     bounce = 1500 * frame_time
        #     self.world_x -= math.cos(self.angle) * bounce
        #     self.world_y -= math.sin(self.angle) * bounce
        #     return


        # ---------------------
        # 5) Camera follow
        # ---------------------
        target_camera_y = self.world_y - SCREEN_H // 2
        lerp = 8 * frame_time  # 따라오는 속도(6~12 추천)
        self.camera_y = self.camera_y * (1 - lerp) + target_camera_y * lerp

        # target_camera_y = self.world_y - SCREEN_H // 2
        # self.camera_y = target_camera_y

        # Camera clamp
        max_cam_y = self.planet.world_height - SCREEN_H
        self.camera_y = clamp(0, self.camera_y, max_cam_y)

        # idle 중력 처리
        if self.dx == 0 and self.dy == 0 and not hit:
            fall_speed = 120 * frame_time
            self.world_y -= fall_speed
            if self.world_y < 0:
                self.world_y = 0

        # ---------------------
        # 6) Drill update
        # ---------------------
        self.drill.update()

    # # ===============================================
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

        # ★ 추가 오프셋 (왼쪽 -3, 아래 -3)
        off_x = -7
        off_y = 3

        # ★ 회전 보정
        rot_off_x = off_x * math.cos(self.angle) - off_y * math.sin(self.angle)
        rot_off_y = off_x * math.sin(self.angle) + off_y * math.cos(self.angle)

        drill_world_x += rot_off_x
        drill_world_y += rot_off_y

        drill_screen_x = drill_world_x - self.camera_x
        drill_screen_y = drill_world_y - self.camera_y

        self.drill.draw(drill_screen_x, drill_screen_y, self.angle- math.pi/2)
        draw_rectangle(*self.get_bb())

