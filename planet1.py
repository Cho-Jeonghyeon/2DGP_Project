from pico2d import *

class Planet:
    TILE = 32  # 타일 크기
    MAP_W = 200  # 가로 타일 수
    MAP_H = 600  # 세로 타일 수

    def __init__(self):
        # 타일셋 로드
        self.tileset = load_image("images/tileset.png")

        # 맵 로드
        self.map = self.load_map("planet_map.txt")

        # 스크롤 시작 지점 (테라리아 최고 핵심)
        self.scroll_y = 0  # 0 = 맨 위

    def update(self, dy=0):
        self.scroll_y = clamp(0, self.scroll_y + dy, self.height - 1000)

    def draw(self):
        self.image.clip_draw(0, int(self.scroll_y), 1200, 1000, 600, 500)

    def load_map(self, path):
        data = []
        with open(path, "r") as f:
            for line in f:
                row = list(map(int, line.split()))
                data.append(row)
        return data
