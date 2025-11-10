from pico2d import *
from state_machine import StateMachine

def right_down(event):
    return event[0] == SDL_KEYDOWN and event[0] == SDLK_RIGHT

def right_up(event):
    return event[0] == SDL_KEYUP and event[0] == SDLK_RIGHT

def left_up(event):
    return event[0] == SDL_KEYUP and event[0] == SDLK_LEFT

def left_down(event):
    return event[0] == SDL_KEYDOWN and event[0] == SDLK_LEFT

def down_down(event):
    return event[0] == SDL_KEYDOWN and event[0] == SDLK_DOWN

def down_up(event):
    return event[0] == SDL_KEYUP and event[0] == SDLK_DOWN

def up_down(event):
    return event[0] == SDL_KEYDOWN and event[0] == SDLK_UP

def up_up(event):
    return event[0] == SDL_KEYUP and event[0] == SDLK_UP


class Spaceship:
    def __init__(self):
        self.x, self.y = 300,300
        self.frame = 0
        self.dir_x = 1 #오른쪽
        self.dir_y = 1 #위쪽
        self.speed = 5
        self.image = load_image('spaceship_level_1.png')
        self.IDLE, self.MOVE = Idle(self), Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.MOVE: {right_up: self.IDLE, left_up: self.IDLE, up_up: self.IDLE, down_up: self.IDLE},
                self.IDLE: {right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_events(self, event):
        pass

    def get_bb(self):
        pass

class Idle:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    def enter(self):
        self.spaceship.dir_x = 0
        self.spaceship.dir_y = 0

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Move:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    def enter(self, event):

        if right_down(event):
            self.spaceship.dir_x += 1
        if left_down(event):
            self.spaceship.dir_x -= 1
        if up_down(event):
            self.spaceship.dir_y += 1
        if down_down(event):
            self.spaceship.dir_y -= 1

        if right_up(event):
            self.spaceship.dir_x -= 1
        if left_up(event):
            self.spaceship.dir_x += 1
        if up_up(event):
            self.spaceship.dir_y -= 1
        if down_up(event):
            self.spaceship.dir_y += 1


    def exit(self, event):
        pass

    def do(self):
        self.spaceship.x += self.spaceship.dir_x * self.spaceship.speed
        self.spaceship.y += self.spaceship.dir_y * self.spaceship.speed

    def draw(self):
        pass