from pico2d import *

import game_data
from state_machine import StateMachine
import math
import game_framework
from drill import Drill

# 이벤트 검사: raw SDL 이벤트 사용으로 수정
def right_down(event):
    return event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT

def right_up(event):
    return event.type == SDL_KEYUP and event.key == SDLK_RIGHT

def left_down(event):
    return event.type == SDL_KEYDOWN and event.key == SDLK_LEFT

def left_up(event):
    return event.type == SDL_KEYUP and event.key == SDLK_LEFT

def up_down(event):
    return event.type == SDL_KEYDOWN and event.key == SDLK_UP

def up_up(event):
    return event.type == SDL_KEYUP and event.key == SDLK_UP

def down_down(event):
    return event.type == SDL_KEYDOWN and event.key == SDLK_DOWN

def down_up(event):
    return event.type == SDL_KEYUP and event.key == SDLK_DOWN


class Spaceship:
    def __init__(self,x,y):
        self.x, self.y = x,y
        self.frame = 0
        self.dx, self.dy = 0, 0

        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False
        self.dir_x = 0
        self.dir_y = 0

        self.speed = 300
        self.image = load_image('images/spaceship_level_1.png')
        self.image2 = load_image('images/spaceship_level_2.png')
        self.image3 = load_image('images/spaceship_level_3.png')

        self.IDLE, self.MOVE = Idle(self), Move(self)
        # 회전 각도 (라디안)
        self.angle = math.radians(0)  # 기본적으로 위쪽 바라봄

        # 드릴 장착
        self.drill = Drill()
        self.drill_offset = 50  # 드릴이 우주선 중심에서 떨어진 거리

        # 전이 테이블은 최소화: 초기 상태에서 enter 호출만 필요
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.MOVE, left_down: self.MOVE,
                            up_down: self.MOVE, down_down: self.MOVE},
                self.MOVE: {}
            }
        )

    def update(self):
        # 이동
        self.x += self.dx * self.speed * game_framework.frame_time
        self.y += self.dy * self.speed * game_framework.frame_time

        # 화면 경계 제한
        self.x = clamp(40, self.x, 1160)
        self.y = clamp(40, self.y, 960)

        # 방향각 업데이트 (움직일 때만)
        if self.dx != 0 or self.dy != 0:
            self.angle = math.atan2(self.dy, self.dx)

        # 드릴 애니메이션 업데이트
        self.drill.update()

    def draw(self):
        # 이미지가 '아래쪽'을 보고 있으므로 -90도 보정
        draw_angle = self.angle - math.pi / 2

        # 우주선 회전해서 그림
        if game_data.ship_lv == 1:
            self.image.rotate_draw(draw_angle, self.x, self.y, 70, 70)
        elif game_data.ship_lv == 2:
            self.image2.rotate_draw(draw_angle, self.x, self.y, 70, 70)
        elif game_data.ship_lv == 3:
            self.image3.rotate_draw(draw_angle, self.x, self.y, 70, 70)

        # 드릴 위치 계산 (보정된 각도 기준)
        drill_x = self.x + math.cos(self.angle) * self.drill_offset
        drill_y = self.y + math.sin(self.angle) * self.drill_offset

        # 드릴 방향도 동일하게 회전
        self.drill.draw(drill_x, drill_y, draw_angle)

        #draw_rectangle(*self.get_bb())

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
            if event.key == SDLK_RIGHT and self.dx > 0:
                self.dx = 0
            elif event.key == SDLK_LEFT and self.dx < 0:
                self.dx = 0
            elif event.key == SDLK_UP and self.dy > 0:
                self.dy = 0
            elif event.key == SDLK_DOWN and self.dy < 0:
                self.dy = 0

    def get_bb(self):
        return self.x-50, self.y-45, self.x+50, self.y+45

    def get_bb_drill(self):
        drill_x = self.x + math.cos(self.angle) * self.drill_offset
        drill_y = self.y + math.sin(self.angle) * self.drill_offset
        return drill_x - 10, drill_y - 10, drill_x + 10, drill_y + 10

class Idle:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    # enter는 event 없이 호출될 수 있으므로 기본값으로 None 허용
    def enter(self, event=None):
        self.spaceship.dir_x = 0
        self.spaceship.dir_y = 0
        self.spaceship.key_right = False
        self.spaceship.key_left = False
        self.spaceship.key_up = False
        self.spaceship.key_down = False

    def exit(self, event=None):
        pass

    def do(self):
        # 정지 상태에서는 프레임 고정
        self.spaceship.frame = 0

    def draw(self):
        # 이미지 그리기
        draw_rectangle(*self.get_bb())
        self.spaceship.image.draw(self.spaceship.x, self.spaceship.y,80,80)

class Move:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    # enter는 이벤트를 선택적으로 받아 키 상태를 갱신 (여기서는 필요 없음)
    def enter(self, event=None):
        # event가 있으면 키 상태를 갱신하도록 처리(안정성)
        if event is None:
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT: self.spaceship.key_right = True
            if event.key == SDLK_LEFT:  self.spaceship.key_left = True
            if event.key == SDLK_UP:    self.spaceship.key_up = True
            if event.key == SDLK_DOWN:  self.spaceship.key_down = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT: self.spaceship.key_right = False
            if event.key == SDLK_LEFT:  self.spaceship.key_left = False
            if event.key == SDLK_UP:    self.spaceship.key_up = False
            if event.key == SDLK_DOWN:  self.spaceship.key_down = False

    def exit(self, event=None):
        pass

    def do(self):
        dx, dy = 0, 0

        if self.spaceship.key_right: dx += 1
        if self.spaceship.key_left:  dx -= 1
        if self.spaceship.key_up:    dy += 1
        if self.spaceship.key_down:  dy -= 1

        # 대각선 보정
        if dx != 0 and dy != 0:
            factor = 0.70710678
            dx *= factor
            dy *= factor

        self.spaceship.x += dx * self.spaceship.speed
        self.spaceship.y += dy * self.spaceship.speed

        self.spaceship.x = clamp(40, self.spaceship.x, 1160)  # 왼쪽/오른쪽 벽
        self.spaceship.y = clamp(40, self.spaceship.y, 960)  # 아래/위 벽

        # 모든 키가 안 눌려있으면 Idle로 전환
        if not (self.spaceship.key_right or self.spaceship.key_left or
                self.spaceship.key_up or self.spaceship.key_down):
            self.spaceship.state_machine.cur_state = self.spaceship.IDLE
            self.spaceship.IDLE.enter()

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.spaceship.image.draw(self.spaceship.x, self.spaceship.y,80,80)
