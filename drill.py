from pico2d import *

class Drill:
    def __init__(self):
        self.image = load_image('images/drill2.png')
        self.frame = 0
        self.level = 0
        self.x, self.y = 400, 300

    def update(self):
        # 프레임 넘기기
        self.frame = (self.frame + 1) % 6

    def draw(self):
        frame_width = 40
        frame_height = 40

        # clip_draw(x, y, w, h, draw_x, draw_y)
        self.image.clip_draw(
            self.frame * frame_width,                 # 현재 프레임의 가로 좌표
            (5 - self.level) * frame_height,          # 세로 좌표 (pico2d는 아래가 0이므로 반대로 계산)
            frame_width, frame_height,                # 한 프레임 크기
            self.x, self.y                            # 그릴 위치
        )