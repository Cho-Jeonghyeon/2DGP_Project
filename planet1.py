from pico2d import *

class Planet:
    def __init__(self):
        self.image = load_image('images/planet1.png')
        self.width = self.image.w
        self.height = self.image.h
        self.scroll_y = 0

    def update(self, dy=0):
        self.scroll_y = clamp(0, self.scroll_y + dy, self.height - 1000)

    def draw(self):
        self.image.clip_draw(0, int(self.scroll_y), 1200,1000,600,500)