from pico2d import *

import game_framework


class Plant:
    def __init__(self, image_path, x, y, w, h, stage_mode, frame_count=20, fps=7):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.stage_mode = stage_mode
        self.is_glow = False

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
        if self.is_glow:
            alpha = (math.sin(get_time() * 6) + 1) / 2
            self.image.opacify(0.7 + 0.3 * alpha)
        else:
            self.image.opacify(1.0)
        # 현재 프레임 잘라서 그리기
        frame_index = int(self.frame)
        sx = frame_index * self.frame_width
        self.image.clip_draw(sx, 0, self.frame_width, self.frame_height, self.x, self.y, self.w, self.h)

        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return [self.x-145, self.y-145, self.x+145, self.y+145]
    def get_bb2(self):
        return [self.x-230, self.y-230, self.x+230, self.y+230]


class StartButton:
    def __init__(self, image_path, x, y, w, h):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.base_w, self.base_h = w, h  # 기본 크기
        self.w, self.h = w, h
        self.is_hover = False  # 마우스가 위에 있을 때 True
        self.scale_speed = 5.0  # 크기 전환 속도 (값 높을수록 즉각적)


    def draw(self):
        alpha = (math.sin(get_time() * 3) + 1) / 2  # 0~1 사이 변화
        self.image.opacify(0.5 + 0.5 * alpha)  # 밝기 깜빡임
        self.image.draw(self.x, self.y, self.w, self.h)

    def update(self):
        target_scale = 1.2 if self.is_hover else 1.0  # hover 시 20% 확대
        self.w += (self.base_w * target_scale - self.w) * game_framework.frame_time * self.scale_speed
        self.h += (self.base_h * target_scale - self.h) * game_framework.frame_time * self.scale_speed

    def is_clicked(self, mx, my):
        return (self.x - self.w/2 <= mx <= self.x + self.w/2) and \
               (self.y - self.h/2 <= my <= self.y + self.h/2)


class UpgradeButton:
    def __init__(self, image_path, x, y, w, h, upgrade_mode):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.base_w, self.base_h = w, h
        self.w, self.h = w, h
        self.is_hover = False  # 마우스가 위에 있을 때 True
        self.scale_speed = 5.0  # 크기 전환 속도 (값 높을수록 즉각적)
        self.stage_mode = upgrade_mode

    def draw(self):
        alpha = (math.sin(get_time() * 3) + 1) / 2  # 0~1 사이 변화
        self.image.opacify(0.5 + 0.5 * alpha)  # 밝기 깜빡임
        self.image.draw(self.x, self.y, self.w, self.h)
        #draw_rectangle(*self.get_bb())

    def update(self):
        target_scale = 1.2 if self.is_hover else 1.0  # hover 시 20% 확대
        self.w += (self.base_w * target_scale - self.w) * game_framework.frame_time * self.scale_speed
        self.h += (self.base_h * target_scale - self.h) * game_framework.frame_time * self.scale_speed


    def get_bb(self):
        return [self.x - 125, self.y - 50, self.x + 125, self.y + 50]