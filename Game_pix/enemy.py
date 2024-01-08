from position import Position
from imageposition import Imageposition
class Enemy:

    def __init__(self, img_id):

        self.pos = Position(0, 0)
        self.img_hero = img_id
        self.size_x = 7
        self.size_y = 8
        self.speed_y = 0.1
        self.color_tr = 0
        self.get_image_right = Imageposition(16, 0)
        self.get_image = self.get_image_right
        self.spawn_y = -10


    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y