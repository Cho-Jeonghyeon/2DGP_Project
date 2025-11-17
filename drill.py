from pico2d import *
import math
import game_framework

class Drill:
    def __init__(self):
        self.image = load_image('images/drill_level1.png')

        # 스프라이트 시트 정보
        self.frame = 0
        self.total_frames = 5     # 총 프레임 수
        self.frame_width = 22 #self.image.w // self.total_frames  #
        self.frame_height = self.image.h  # = 13
        self.drill_size = 35      # 화면에 그릴 크기 (확대용)

    def update(self):
        # 회전 애니메이션 프레임 업데이트
        self.frame = (self.frame + 12 * game_framework.frame_time) % self.total_frames

    def draw(self, x, y, angle):
        frame_index = int(self.frame)

        # 이미지가 "왼쪽"을 바라보므로, draw_angle은 우주선 각도 + 90도 보정
        draw_angle = angle - math.pi / 2

        self.image.clip_composite_draw(
            frame_index * self.frame_width,  # x좌표 (왼쪽부터 프레임 자르기)
            0,                               # y좌표 (1행이라 0)
            self.frame_width, self.frame_height,
            draw_angle,                      # 회전각도 (라디안)
            '',                              # 플립 없음
            x, y,                            # 드릴 중심 좌표
            self.drill_size, self.drill_size # 출력 크기
        )