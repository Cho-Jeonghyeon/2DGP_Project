from pico2d import *

class Background:
    def __init__(self, path):
        self.image = load_image(path)
        self.x, self.y = 600, 500   # 화면 중앙 고정


    def update(self):
        pass

    def draw(self):
         self.image.draw(self.x, self.y)