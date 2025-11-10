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
        self.image = self.image.draw(self.x, self.y)

    def handle_events(self, event):
        pass

    def get_bb(self):
        pass

