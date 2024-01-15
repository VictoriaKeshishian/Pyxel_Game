import random
from position import Position
from imageposition import Imageposition

class Enemy3:

    def __init__(self, img_id, window_width, window_height):
        self.pos = Position(0, 0)
        self.img_hero = img_id
        self.size_x = 7
        self.size_y = 8
        self.speed_y = 0.2
        self.speed_x = 0.2
        self.color_tr = 0
        self.get_image_right = Imageposition(40, 0)
        self.get_image = self.get_image_right
        self.spawn_y = -10
        self.WINDOW_W = window_width
        self.WINDOW_H = window_height
        self.dir_x = -5  # Начальное направление по X

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y

        # Проверка достижения края экрана по X
        if self.pos.x <= 0 or self.pos.x + self.size_x >= self.WINDOW_W:
            self.dir_x *= -1  # Изменение направления по X при достижении края экрана

        # Обновление координат
        self.pos.x += self.dir_x * self.speed_x
        self.pos.y += self.speed_y  # Движение по оси Y

        # Ограничим движение врага, чтобы он не выходил за границы экрана
        self.pos.x = max(0, min(self.pos.x, self.WINDOW_W - self.size_x))
        self.pos.y = max(0, min(self.pos.y, self.WINDOW_H - self.size_y))
