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
            [self.get_tile_hp(tile) for tile in row]
            for row in self.map
        ]

        self.rock_count = {1:0,2:0,3:0,4:0}

        self.tile_damage = [
            [self.get_tile_damage(tile) for tile in row]
            for row in self.map
        ]

        self.tile_exp = [
            [self.get_tile_exp(tile) for tile in row]
            for row in self.map
        ]


    def get_tile_hp(self, tile):
        if tile == 1: return 10     # dirt
        if tile == 2: return 20     # stone
        if tile == 3: return 30     # iron
        if tile == 4: return 40    # cobalt
        return 0

    def get_tile_damage(self, tile):
        if tile == 1: return 1
        if tile == 2: return 2
        if tile == 3: return 3
        if tile == 4: return 3
        return 0

    def get_tile_exp(self, tile):
        if tile == 1: return 5
        if tile == 2: return 10
        if tile == 3: return 15
        if tile == 4: return 15
        return 0

    # ============================================
    # destroy : world 좌표 기준 파괴
    # ============================================
    def destroy(self, world_x, world_y, damage, radius=1):
        """
        world_x, world_y : 타일 파괴 기준이 되는 '월드 좌표'
        damage : 드릴 데미지
        radius : 원형 범위 파괴
        """
        tile_c = int(world_x // TILE)
        tile_r = int(world_y // TILE)

        hit = False
        tile_damagetoship = 0
        exp_to_ship = 0
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
                        # 광물 HP 감소
                        self.tile_hp[r][c] -= damage
                        # 우주선 HP 감소

                        hit = True

                        tile_damagetoship = self.tile_damage[r][c]
                        # HP가 0 이하이면 제거
                        if self.tile_hp[r][c] <= 0:
                            exp_to_ship = self.tile_exp[r][c]
                            self.rock_count[tile] += 1
                            print(self.rock_count)
                            self.map[r][c] = 0
                            self.tile_hp[r][c] = 0
                            self.tile_damage[r][c] = 0

        return hit, tile_damagetoship, exp_to_ship

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
