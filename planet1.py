from pico2d import *

class Planet:
    TILE = 32
    MAP_W = 40
    MAP_H = 100

    def __init__(self):
        self.tileset = load_image("images/tileset.png")

        self.map = self.load_map("planet_map_test.txt")

        # 타일맵 전체 높이
        self.total_height = self.MAP_H * self.TILE

        # 스크롤 시작
        self.scroll_y = self.total_height - 1000

    def load_map(self, path):
        data = []
        with open(path, "r") as f:
            for line in f:
                row = list(map(int, line.split()))
                data.append(row)
        data.reverse()
        return data

    def draw(self):
        screen_w = 1200
        screen_h = 1000

        start_row = int(self.scroll_y // self.TILE)
        end_row = start_row + (screen_h // self.TILE) + 3

        for r in range(start_row, min(end_row, self.MAP_H)):
            for c in range(self.MAP_W):
                tile = self.map[r][c]
                if tile == 0:
                    continue

                world_x = c * self.TILE
                world_y = r * self.TILE - self.scroll_y

                if world_y < -self.TILE or world_y > screen_h + self.TILE:
                    continue

                sx = (tile % 8) * self.TILE
                sy = (tile // 8) * self.TILE

                self.tileset.clip_draw(
                    sx-self.TILE, sy,
                    self.TILE, self.TILE,
                    world_x + self.TILE // 2,
                    world_y + self.TILE // 2
                )

    def update(self):
        pass

    def destroy(self, world_x, world_y, radius=1):
        tile_c = int(world_x // self.TILE)
        tile_r = int((world_y + self.scroll_y) // self.TILE)

        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                if dx*dx + dy*dy > radius * radius:
                    continue

                r = tile_r + dy
                c = tile_c + dx

                if 0 <= r < self.MAP_H and 0 <= c < self.MAP_W:
                    self.map[r][c] = 0


