from pico2d import *
from state_machine import StateMachine

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
    def __init__(self):
        self.x, self.y = 300,300
        self.frame = 0

        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False
        self.dir_x = 0
        self.dir_y = 0

        self.speed = 2
        self.image = load_image('images/spaceship_level_1.png')
        self.IDLE, self.MOVE = Idle(self), Move(self)
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
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_events(self, event):
        # 키 플래그를 직접 갱신하여 MOVE 상태에서도 즉시 반영되도록 함
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT: self.key_right = True
            if event.key == SDLK_LEFT:  self.key_left = True
            if event.key == SDLK_UP:    self.key_up = True
            if event.key == SDLK_DOWN:  self.key_down = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT: self.key_right = False
            if event.key == SDLK_LEFT:  self.key_left = False
            if event.key == SDLK_UP:    self.key_up = False
            if event.key == SDLK_DOWN:  self.key_down = False

        # 상태 전환 처리: IDLE->MOVE, MOVE->IDLE를 직접 제어
        cur = self.state_machine.cur_state
        any_key = (self.key_right or self.key_left or self.key_up or self.key_down)
        if any_key and cur is self.IDLE:
            self.state_machine.cur_state = self.MOVE
            self.MOVE.enter(event)
        elif not any_key and cur is self.MOVE:
            self.state_machine.cur_state = self.IDLE
            self.IDLE.enter()

    def get_bb(self):
        return self.x-50, self.y-45, self.x+50, self.y+45

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
        self.spaceship.image.draw(self.spaceship.x, self.spaceship.y)

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

        # 모든 키가 안 눌려있으면 Idle로 전환
        if not (self.spaceship.key_right or self.spaceship.key_left or
                self.spaceship.key_up or self.spaceship.key_down):
            self.spaceship.state_machine.cur_state = self.spaceship.IDLE
            self.spaceship.IDLE.enter()

    def draw(self):
        self.spaceship.image.draw(self.spaceship.x, self.spaceship.y)
