from pico2d import *

import game_framework


class Background:
    def __init__(self, image_path, speed=100):
        self.image = load_image(image_path)
        self.width = self.image.w
        self.height = self.image.h
        self.x1 = 0
        self.x2 = self.width
        self.y = 500  # 화면 중앙 기준 (캔버스 높이에 맞게 조정)
        self.speed = speed

    def update(self):
        # 왼쪽으로 이동
        self.x1 -= self.speed * game_framework.frame_time
        self.x2 -= self.speed * game_framework.frame_time

        # 한쪽 이미지가 완전히 화면 왼쪽을 벗어나면 다시 오른쪽으로 이동
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self):
        # 두 이미지를 이어붙여서 그림
        self.image.draw(self.x1 + self.width // 2, self.y)
        self.image.draw(self.x2 + self.width // 2, self.y)