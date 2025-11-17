from pico2d import *
import math
import game_framework
from drill import Drill

class SpaceshipGame:
    def __init__(self, planet):
        self.x, self.y = 600, 400  # 화면 중앙 고정
        self.speed = 300
        self.image = load_image('images/spaceship_level_1.png')

        # 방향 벡터
        self.dx, self.dy = 0, 0
        self.angle = 0  # 기본 방향: 오른쪽

        # 드릴 장착
        self.drill = Drill()
        self.drill_offset = 50
        self.planet = planet  # 행성 참조

    def update(self):
        # 좌우 이동 (x는 실제 이동)
        self.x += self.dx * self.speed * game_framework.frame_time
        self.x = clamp(50, self.x, 1150)

        # === 상하 이동 (스크롤 + 끝에서는 실제 이동) ===
        scroll_speed = self.dy * self.speed * game_framework.frame_time

        # 위로 이동 (행성 아래쪽이 올라오게)
        if self.dy > 0 and self.planet.scroll_y < self.planet.height - 1000:
            self.planet.scroll_y += scroll_speed
            self.y = 400
        # 아래로 이동 (행성 윗부분으로 돌아가게)
        elif self.dy < 0 and self.planet.scroll_y > 0:
            self.planet.scroll_y += scroll_speed
            self.y = 400
        # 더 이상 스크롤 불가능할 때만 우주선 실제 이동
        else:
            # 맨 위나 맨 아래라면 우주선을 실제로 움직임
            self.y += self.dy * self.speed * game_framework.frame_time
            self.y = clamp(100, self.y, 1000)

        # 방향 회전 계산
        if self.dx != 0 or self.dy != 0:
            self.angle = math.atan2(self.dy, self.dx)

        # 드릴 회전 애니메이션
        self.drill.update()

    def draw(self):
        # 이미지 기본 방향이 아래쪽이면 90도 보정
        draw_angle = self.angle - math.pi / 2

        # 우주선
        self.image.rotate_draw(draw_angle, self.x, self.y, 70, 70)

        # 드릴 위치 계산
        drill_x = self.x + math.cos(self.angle) * self.drill_offset
        drill_y = self.y + math.sin(self.angle) * self.drill_offset

        # 드릴 회전
        self.drill.draw(drill_x, drill_y, draw_angle)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dx = 1
            elif event.key == SDLK_LEFT:
                self.dx = -1
            elif event.key == SDLK_UP:
                self.dy = 1
            elif event.key == SDLK_DOWN:
                self.dy = -1

        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT):
                self.dx = 0
            elif event.key in (SDLK_UP, SDLK_DOWN):
                self.dy = 0
