from pico2d import *
from state_machine import StateMachine


class Spaceship:
    def __init__(self):
        self.x, self.y = 300,300
        #self.frame = 0
        #self.face_dir = 1
        self.image = load_image('spaceship_level_1.png')
        self.IDLE, self.MOVE = Idle(self), Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.MOVE: {right_up: self.IDLE},
                self.IDLE: {right_down: self.MOVE}
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
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Move:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass