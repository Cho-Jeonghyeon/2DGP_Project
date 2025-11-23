from pico2d import *
import math

import game_framework


class Drill:
    def __init__(self):
        self.image = load_image('images/drill_level1.png')
        self.frame = 0
        self.frame_speed = 20  # 회전 애니메이션 속도
        self.damage = 10

        self.total_frames = 5
        self.frame_width = 22
        self.frame_height = self.image.h
        self.drill_size = 50
        self.hit_timer = 0.0

    def update(self):
        # 단순 회전 애니메이션
        frame_time = game_framework.frame_time
        self.frame = (self.frame + 12 * game_framework.frame_time) % self.total_frames
        if self.hit_timer > 0:
            self.hit_timer -= frame_time
            if self.hit_timer < 0:
                self.hit_timer = 0

    def draw(self, screen_x, screen_y, angle):
        frame_index = int(self.frame)
        draw_angle = angle - math.pi / 2

        shake_x, shake_y = 0, 0
        scale = 1.0

        if self.hit_timer > 0:
            # 흔들림
            shake_x = (math.sin(self.hit_timer * 50) * 3)  # 좌우 작은 진동
            shake_y = (math.cos(self.hit_timer * 40) * 3)

            # size 커졌다가 줄어드는 효과
          #  scale = 1.15 - (0.15 * (1 - self.hit_timer / 0.08))
            scale = 1.25 - (0.25 * (1 - self.hit_timer / 0.08))

            # 최종 출력 크기
        final_size = self.drill_size * scale

        # 드릴 그리기
        self.image.clip_composite_draw(
            frame_index * self.frame_width, 0,
            self.frame_width, self.frame_height,
            draw_angle, '',
            screen_x + shake_x, screen_y + shake_y,
            final_size, final_size
        )

        # self.image.clip_composite_draw(
        # frame_index * self.frame_width, 0, self.frame_width, self.frame_height, draw_angle,'', screen_x, screen_y, self.drill_size, self.drill_size)



# from pico2d import *
# import math
# import game_framework
#
# class Drill:
#     def __init__(self):
#         self.image = load_image('images/drill_level1.png')
#
#         self.frame = 0
#         self.total_frames = 5
#         self.frame_width = 22
#         self.frame_height = self.image.h
#         self.drill_size = 50
#
#         self.level = 1
#         self.damage = 1
#
#     def update(self):
#         self.frame = (self.frame + 12 * game_framework.frame_time) % self.total_frames
#
#     def draw(self, x, y, angle):
#         frame_index = int(self.frame)
#         draw_angle = angle - math.pi / 2
#
#         self.image.clip_composite_draw(
#             frame_index * self.frame_width,
#             0,
#             self.frame_width, self.frame_height,
#             draw_angle,
#             '',
#             x, y,
#             self.drill_size, self.drill_size
#         )
#