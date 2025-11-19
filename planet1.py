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

    def load_map(self, path):
        data = []
        with open(path, "r") as f:
            for line in f:
                row = list(map(int, line.split()))
                data.append(row)
        return data

    def update(self, dy=0):
        self.scroll_y = clamp(0, self.scroll_y + dy, self.MAP_H * self.TILE - 1000)

    def draw(self):
        screen_w = 1200
        screen_h = 1000

        start_row = int(self.scroll_y // self.TILE)
        end_row = start_row + (screen_h // self.TILE) + 2

        for r in range(start_row, min(end_row, self.MAP_H)):
            for c in range(self.MAP_W):
                tile = self.map[r][c]
                if tile == 0:
                    continue

                world_x = c * self.TILE
                world_y = r * self.TILE - self.scroll_y

                if world_y + self.TILE < 0 or world_y > screen_h:
                    continue

                sx = (tile % 8) * self.TILE
                sy = (tile // 8) * self.TILE

                self.tileset.clip_draw(sx, sy, self.TILE, self.TILE,world_x + self.TILE//2,world_y + self.TILE//2,)

    def destroy_at(self, world_x, world_y, radius=2):
        tile_c = int(world_x // self.TILE)
        tile_r = int((world_y + self.scroll_y) // self.TILE)

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    r = tile_r + dy
                    c = tile_c + dx

                    if 0 <= r < self.MAP_H and 0 <= c < self.MAP_W:
                        self.map[r][c] = 0  # 타일 삭제
