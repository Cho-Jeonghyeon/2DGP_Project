# drill.py
from pico2d import load_image

class Drill:
    def __init__(self):
        self.image = load_image('images/drill_level1.png')
        self.frame = 0
        self.frame_speed = 20  # 회전 애니메이션 속도
        self.damage = 10

    def update(self):
        # 단순 회전 애니메이션
        self.frame = (self.frame + self.frame_speed * 0.016) % 360

    def draw(self, screen_x, screen_y, angle):
        """
        screen_x, screen_y : 화면에 그릴 위치
        angle : 회전 각도
        """
        # drill은 spaceship이 world→screen 계산해서 넘겨 줌
        self.image.rotate_draw(angle - 3.14/2, screen_x, screen_y, 40, 40)




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
#         # # ===== 타일 파괴 추가 =====
#         # try:
#         #     from game_mode_1 import planet
#         #     planet.destroy(x, y, radius=1)
#         # except:
#         #     pass
