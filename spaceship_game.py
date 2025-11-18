from pico2d import *
import math
import game_framework
from drill import Drill

class SpaceshipGame:
    def __init__(self, planet):
        self.x, self.y = 600, 900  # 화면 중앙 고정
        self.speed = 150
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
        target_y = 400

        # 행성 스크롤 구간
        if (self.dy > 0 and self.planet.scroll_y < self.planet.height - 1000) or \
                (self.dy < 0 and self.planet.scroll_y > 0):

            # 행성 스크롤 이동
            self.planet.scroll_y += scroll_speed

            # --- 일정 속도 보간
            lerp_speed = 0.5 * game_framework.frame_time  # 값 낮을수록 더 부드럽고 느림
            self.y = self.y * (1 - lerp_speed) + target_y * lerp_speed

        else:

            if self.dx == 0 and self.dy == 0:
                self.y -= 30 * game_framework.frame_time
                self.y = clamp(70, self.y, 950)
            else:
                # 맨 위나 맨 아래라면 우주선을 실제로 움직임
                self.y += self.dy * self.speed * game_framework.frame_time
                self.y = clamp(70, self.y, 950)

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
