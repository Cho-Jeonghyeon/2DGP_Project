# planet1.py
from pico2d import load_image, draw_rectangle
import math

TILE = 32
SCREEN_W = 1200
SCREEN_H = 1000


class Planet:
    def __init__(self, map_data):
        """
        map_data : 2D 리스트 (row x col)
        """
        self.map = map_data
        self.MAP_H = len(map_data)       # rows
        self.MAP_W = len(map_data[0])    # cols

        self.world_height = self.MAP_H * TILE
        self.world_width  = self.MAP_W * TILE

        # 타일 이미지 로드 (0은 비어있음)
        self.tile_images = {
            1: load_image('images/1.png'),
            2: load_image('images/2.png'),
            3: load_image('images/3.png'),
            4: load_image('images/4.png')
        }

        # 각 타일 HP
        self.tile_hp = [
            [self.get_initial_hp(tile) for tile in row]
            for row in self.map
        ]

    def get_initial_hp(self, tile):
        if tile == 1: return 20     # dirt
        if tile == 2: return 40     # stone
        if tile == 3: return 60     # iron
        if tile == 4: return 100    # cobalt
        return 0

    # ============================================
    # destroy : world 좌표 기준 파괴
    # ============================================
    def destroy(self, world_x, world_y, damage=1, radius=1):
        """
        world_x, world_y : 타일 파괴 기준이 되는 '월드 좌표'
        damage : 드릴 데미지
        radius : 원형 범위 파괴
        """
        tile_c = int(world_x // TILE)
        tile_r = int(world_y // TILE)

        hit = False

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):

                # 원형 범위 체크
                if dx*dx + dy*dy > radius * radius:
                    continue

                r = tile_r + dy
                c = tile_c + dx

                if 0 <= r < self.MAP_H and 0 <= c < self.MAP_W:
                    tile = self.map[r][c]
                    if tile != 0:
                        # HP 감소
                        self.tile_hp[r][c] -= damage
                        hit = True

                        # HP가 0 이하이면 제거
                        if self.tile_hp[r][c] <= 0:
                            self.map[r][c] = 0
        return hit

    # ============================================
    # draw : world → screen 변환해서 그리기
    # ============================================
    def draw(self, camera_x, camera_y):
        """
        camera_x, camera_y : world 기준 카메라 좌표
        화면에는 0~SCREEN 좌표로 그리기
        """

        # 화면에 보이는 타일 범위 계산
        start_col = max(0, int(camera_x // TILE))
        end_col   = min(self.MAP_W, int((camera_x + SCREEN_W) // TILE) + 1)

        start_row = max(0, int(camera_y // TILE))
        end_row   = min(self.MAP_H, int((camera_y + SCREEN_H) // TILE) + 1)

        for r in range(start_row, end_row):
            for c in range(start_col, end_col):

                tile = self.map[r][c]
                if tile == 0:
                    continue

                img = self.tile_images.get(tile, None)
                if img is None:
                    continue

                world_x = c * TILE
                world_y = r * TILE

                # world → screen 변환
                screen_x = world_x - camera_x
                screen_y = world_y - camera_y

                img.draw(screen_x + TILE//2, screen_y + TILE//2, TILE, TILE)



# from operator import truediv
#
# from pico2d import *
#
# class Planet:
#     TILE = 32
#     MAP_W = 40
#     MAP_H = 100
#
#     def __init__(self):
#         self.tileset = load_image("images/tileset.png")
#
#         self.map = self.load_map("planet_map_test.txt")
#
#         # 타일맵 전체 높이
#         self.total_height = self.MAP_H * self.TILE
#
#         # 스크롤 시작
#         self.scroll_y = self.total_height - 1000
#
#         self.tile_hp = [
#             [self.mineral_hp(tile) for tile in row]
#             for row in self.map
#         ]
#
#     def load_map(self, path):
#         data = []
#         with open(path, "r") as f:
#             for line in f:
#                 row = list(map(int, line.split()))
#                 data.append(row)
#         data.reverse()
#         return data
#
#     def draw(self):
#         screen_w = 1200
#         screen_h = 1000
#
#         start_row = int(self.scroll_y // self.TILE)
#         end_row = start_row + (screen_h // self.TILE) + 3
#
#         for r in range(start_row, min(end_row, self.MAP_H)):
#             for c in range(self.MAP_W):
#                 tile = self.map[r][c]
#                 if tile == 0:
#                     continue
#
#                 world_x = c * self.TILE
#                 world_y = r * self.TILE - self.scroll_y
#
#                 if world_y < -self.TILE or world_y > screen_h + self.TILE:
#                     continue
#
#                 sx = (tile % 8) * self.TILE
#                 sy = (tile // 8) * self.TILE
#
#                 self.tileset.clip_draw(
#                     sx-self.TILE, sy,
#                     self.TILE, self.TILE,
#                     world_x + self.TILE // 2,
#                     world_y + self.TILE // 2
#                 )
#
#     def update(self):
#         pass
#
#     def destroy(self, world_x, world_y, radius=1, damage=1):
#         hit = False
#         tile_c = int(world_x // self.TILE)
#         tile_r = int((world_y + self.scroll_y) // self.TILE)
#
#         for dy in range(-radius, radius+1):
#             for dx in range(-radius, radius+1):
#                 if dx*dx + dy*dy > radius * radius:
#                     continue
#
#                 r = tile_r + dy
#                 c = tile_c + dx
#
#                 if 0 <= r < self.MAP_H and 0 <= c < self.MAP_W:
#                     if self.map[r][c] ==0:
#                         continue
#                     self.tile_hp[r][c] -= damage
#                     hit = True
#                     if self.tile_hp[r][c] <=0:
#                         self.map[r][c] =0
#                         self.tile_hp[r][c] = 0
#         return hit
#
#
#
#     def mineral_hp(self, tile):
#         if tile ==1:
#             return 1
#         if tile ==2:
#             return 2
#         if tile ==3:
#             return 3
#         if tile ==4:
#             return 4
#         return 0
