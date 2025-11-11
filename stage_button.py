from pico2d import *


class StageButton:
    def __init__(self, path, x, y, w, h, stage):
        self.image = load_image(path)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.stage_mode = stage
    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def is_clicked(self, mx, my):
        return (self.x - self.w / 2 <= mx <= self.x + self.w / 2) and (self.y - self.h / 2 <= my <= self.y + self.h / 2)


class Button:
    def __init__(self, image_path, x, y, w, h):
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.w, self.h = w, h

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def is_clicked(self, mx, my):
        return (self.x - self.w/2 <= mx <= self.x + self.w/2) and \
               (self.y - self.h/2 <= my <= self.y + self.h/2)