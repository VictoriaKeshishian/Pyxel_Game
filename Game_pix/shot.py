
from position import Position

class Shot:

    def __init__(self):

        self.pos = Position(0, 0)
        self.size = 1
        self.speed = 3
        self.color = 6

    def update(self, x, y):

        self.pos.x = x
        self.pos.y = y