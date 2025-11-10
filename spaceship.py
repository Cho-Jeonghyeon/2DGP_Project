from pico2d import *

class Spaceship:
    def __init__(self):
        self.x, self.y = 300,300
        #self.frame = 0
        #self.face_dir = 1
        self.image = load_image('spaceship_level_1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

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