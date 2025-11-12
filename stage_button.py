from pico2d import *

import game_framework


class Plant:
    def __init__(self, image_path, x, y, w, h, stage_mode, frame_count=20, fps=7):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.stage_mode = stage_mode

        # 애니메이션 관련
        self.frame = 0
        self.frame_count = frame_count   # 한 줄에 몇 프레임이 있는지 (20)
        self.frame_width = self.image.w // frame_count
        self.frame_height = self.image.h
        self.fps = fps
        self.time_acc = 0.0

    def update(self):
        # 프레임 업데이트
        self.time_acc += get_time() * 0  # <- 필요없지만 구조상 유지
        self.frame = (self.frame + self.fps * game_framework.frame_time) % self.frame_count

    def draw(self):
        # 현재 프레임 잘라서 그리기
        frame_index = int(self.frame)
        sx = frame_index * self.frame_width
        self.image.clip_draw(sx, 0, self.frame_width, self.frame_height, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return [self.x-145, self.y-145, self.x+145, self.y+145]

class Button:
    def __init__(self, image_path, x, y, w, h):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.w, self.h = w, h

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def is_clicked(self, mx, my):
        return (self.x - self.w/2 <= mx <= self.x + self.w/2) and \
               (self.y - self.h/2 <= my <= self.y + self.h/2)