from pico2d import *

class Background:
    def __init__(self, image_name='background2.png'):
        self.image = load_image(image_name)
        self.x, self.y = 400, 300   # 화면 중앙 고정


    def update(self):
        pass

    def draw(self):
         self.image.draw(self.x, self.y)