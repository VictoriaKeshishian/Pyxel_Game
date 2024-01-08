# import pyxel
# from game import Game


class Menu:

    def __init__(self):
        self.choice = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.choice = 1
        elif pyxel.btnp(pyxel.KEY_UP):
            self.choice = 0

        if pyxel.btnp(pyxel.KEY_ENTER):
            if self.choice == 0:
                # Запуск игры
                pyxel.quit()
                game = Game()
        else:
                # Выход
                pyxel.quit()

    def draw(self):
        pyxel.text(55, 41, "GAME MENU", pyxel.frame_count % 16)
        if self.choice == 0:
            pyxel.text(48, 50, "Start game", 7)
        else:
            pyxel.text(48, 50, "Start game", 1)

        if self.choice == 1:
            pyxel.text(48, 60, "Quit", 7)
        else:
            pyxel.text(48, 60, "Quit", 1)
