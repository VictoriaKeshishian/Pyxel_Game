from imageposition import Imageposition
from position import Position
import pyxel


class Hero:


    def __init__(self, image_id):

        self.pos = Position(0, 0)
        self.img_hero = image_id
        self.size_x = 7
        self.size_y = 8
        self.get_image_left = Imageposition(9, 0)
        self.get_image_right = Imageposition(0, 0)
        self.get_image = self.get_image_right

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y
