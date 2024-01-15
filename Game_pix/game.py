import pyxel
from imageposition import Imageposition
from hero import Hero
from shot import Shot
from enemy import Enemy
from enemy2 import Enemy2
from enemy3 import Enemy3
from enemy_generator import generate_unique_enemy
import random



class Game:

    def __init__(self):
        self.IMG_ID0 = 0
        self.WINDOW_H = 120
        self.WINDOW_W = 160
        self.game_over_flag = False
        self.menu_option = 0
        self.game_over_color = 8
        self.text_visible = False
        self.text_display_time = 1  # количество кадров (фреймов), в течение которых будет отображаться текст
        self.current_text_frame = 0
        self.score = 0

        pyxel.init(self.WINDOW_W, self.WINDOW_H)
        pyxel.load("my.pyxres")

        self.hero = Hero(self.IMG_ID0)
        self.hero.pos.x = 80
        self.hero.pos.y = 110
        self.Shots = []
        self.Enemies = []
        self.count_died_enemies = 0



        while True:
            if pyxel.btnp(pyxel.KEY_Q):
                break

            if not self.game_over_flag:
                self.update()
            self.draw()
            pyxel.flip()




    def update(self):

        pyxel.text(10, 10, f"Score: {self.score}", 10)

        # Обработка выхода из игры при нажатии Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Обновление позиции героя при нажатии клавиш W, A, S, D
        if self.hero.pos.y - 1 > 0 and pyxel.btn(pyxel.KEY_W):
            self.hero.update(self.hero.pos.x, self.hero.pos.y - 1)
        if self.hero.pos.x - 1 > 0 and pyxel.btn(pyxel.KEY_A):
            self.hero.update(self.hero.pos.x - 1, self.hero.pos.y)
            self.hero.get_image = self.hero.get_image_left
        if self.hero.pos.y + 9 < self.WINDOW_H and pyxel.btn(pyxel.KEY_S):
            self.hero.update(self.hero.pos.x, self.hero.pos.y + 1)
        if self.hero.pos.x + 9 < self.WINDOW_W and pyxel.btn(pyxel.KEY_D):
            self.hero.update(self.hero.pos.x + 1, self.hero.pos.y)
            self.hero.get_image = self.hero.get_image_right

        # Обработка выстрела при нажатии пробела
        shot_count = len(self.Shots)
        enemies_count = len(self.Enemies)
        if pyxel.btnp(pyxel.KEY_SPACE) and shot_count < 100:
            new_shot = Shot()
            new_shot.update(
                self.hero.pos.x + self.hero.size_x / 2,
                self.hero.pos.y - new_shot.size - 2
            )
            self.Shots.append(new_shot)

        for enemy in self.Enemies:
            if isinstance(enemy, Enemy):
                if enemy.pos.y < self.WINDOW_H - enemy.size_y:
                    enemy.pos.y += enemy.speed_y
                enemy.update(enemy.pos.x, enemy.pos.y + enemy.speed_y)
            elif isinstance(enemy, Enemy2):
                if enemy.pos.y < self.WINDOW_H - enemy.size_y:
                    enemy.pos.y += enemy.speed_y
                enemy.update(enemy.pos.x, enemy.pos.y)
            elif isinstance(enemy, Enemy3):
                if enemy.pos.y < self.WINDOW_H - enemy.size_y:
                    enemy.pos.y += enemy.speed_y
                enemy.update(enemy.pos.x, enemy.pos.y)

            # Проверка столкновения с другими врагами
            for other_enemy in self.Enemies:
                if enemy != other_enemy and self.check_collision(enemy, other_enemy):
                    # Если есть столкновение, измените координаты текущего врага
                    enemy.pos.x -= 0.1
                    enemy.pos.y -= 0.1

        for i in range(len(self.Shots) - 1, -1, -1):
            if self.Shots[i].pos.y > 0:
                self.Shots[i].update(
                    self.Shots[i].pos.x,
                    self.Shots[i].pos.y - self.Shots[i].speed
                )
                try:
                    if self.kill_enemy(i):
                        self.count_died_enemies += 1
                        break
                except IndexError:
                    pass
            else:
                # Используем метод pop для удаления снарядов
                self.Shots.pop(i)
                break


        # Создание нового врага при необходимости
        if enemies_count < 5:
            new_enemy = Enemy(self.IMG_ID0)
            pos_x = random.choice(range(0, self.WINDOW_W - new_enemy.size_x))

            # Используйте значение spawn_y при создании нового врага
            pos_y = new_enemy.spawn_y

            # Проверка на пересечение с другими врагами
            while any(
                    enemy.pos.x < pos_x < enemy.pos.x + enemy.size_x and
                    enemy.pos.y < pos_y < enemy.pos.y + enemy.size_y
                    for enemy in self.Enemies
            ):
                pos_x = random.choice(range(0, self.WINDOW_W - new_enemy.size_x))

                # Используйте значение spawn_y при создании нового врага
                pos_y = new_enemy.spawn_y

            new_enemy.pos.x = pos_x
            new_enemy.pos.y = pos_y
            self.Enemies.append(new_enemy)

        # Проверка на столкновение героя с врагом или достижение врагом конца экрана
        for enemy in self.Enemies:
            if self.check_collision(self.hero, enemy):
                # Если есть касание, завершаем игру (проигрыш)
                self.game_over()

            # Проверка достижения врагом конца экрана
            if enemy.pos.y + enemy.size_y >= self.WINDOW_H:
                # Если враг достиг конца экрана, завершаем игру (проигрыш)
                self.game_over()


    def kill_enemy(self, shot_index):
        for enemy_index in range(len(self.Enemies) - 1, -1, -1):
            enemy = self.Enemies[enemy_index]
            if (self.Shots[shot_index].pos.x >= enemy.pos.x and
                    self.Shots[shot_index].pos.x <= enemy.pos.x + enemy.size_x and
                    self.Shots[shot_index].pos.y >= enemy.pos.y and
                    self.Shots[shot_index].pos.y <= enemy.pos.y + enemy.size_y):
                # Используем метод pop для удаления врагов
                self.Shots.pop(shot_index)
                self.Enemies.pop(enemy_index)

                self.count_died_enemies += 1
                self.score += 1
                # Создание нового врага Enemy2 после убийства 5 врагов
                if self.count_died_enemies % 5 == 0:
                    self.count_died_enemies = 0
                    new_enemy2 = Enemy2(self.IMG_ID0, self.WINDOW_W, self.WINDOW_H)
                    pos_x = random.choice(range(0, self.WINDOW_W - new_enemy2.size_x))
                    pos_y = new_enemy2.spawn_y
                    new_enemy2.update(pos_x, pos_y)
                    self.Enemies.append(new_enemy2)

                if self.count_died_enemies % 10 == 0:
                    new_enemy3 = Enemy3(self.IMG_ID0, self.WINDOW_W, self.WINDOW_H)
                    pos_x = random.choice(range(0, self.WINDOW_W - new_enemy3.size_x))
                    pos_y = new_enemy3.spawn_y
                    new_enemy3.update(pos_x, pos_y)
                    self.Enemies.append(new_enemy3)

                return True
        return False

    def check_collision(self, obj1, obj2):
        # Проверка пересечения координат двух объектов
        return (
                obj1.pos.x < obj2.pos.x + obj2.size_x and
                obj1.pos.x + obj1.size_x > obj2.pos.x and
                obj1.pos.y < obj2.pos.y + obj2.size_y and
                obj1.pos.y + obj1.size_y > obj2.pos.y
        )

    def game_over(self):
        # Дополнительные действия при завершении игры (например, вывод GAME OVER и остановка игры)
        # pyxel.text(self.WINDOW_W // 2 - 30, self.WINDOW_H // 2, "GAME OVER", 8)
        # pyxel.quit()
        self.game_over_flag = True

    def draw(self):
        pyxel.cls(0)

        pyxel.text(10, 10, f"Score: {self.score}", 10)

        if not self.game_over_flag:

            pyxel.blt(self.hero.pos.x, self.hero.pos.y,
                      self.hero.img_hero,
                      self.hero.get_image.pos.x,
                      self.hero.get_image.pos.y,
                      self.hero.size_x, self.hero.size_y)

            for enemy in self.Enemies:

                if isinstance(enemy, Enemy):
                    pyxel.blt(
                        enemy.pos.x,
                        enemy.pos.y,
                        enemy.img_hero,
                        enemy.get_image.pos.x,
                        enemy.get_image.pos.y,
                        enemy.size_x,
                        enemy.size_y,
                        enemy.color_tr
                    )
                elif isinstance(enemy, Enemy2):
                    pyxel.blt(
                        enemy.pos.x,
                        enemy.pos.y,
                        enemy.img_hero,
                        enemy.get_image.pos.x,
                        enemy.get_image.pos.y,
                        enemy.size_x,
                        enemy.size_y,
                        enemy.color_tr,
                    )
                elif isinstance(enemy, Enemy3):
                    pyxel.blt(
                        enemy.pos.x,
                        enemy.pos.y,
                        enemy.img_hero,
                        enemy.get_image.pos.x,
                        enemy.get_image.pos.y,
                        enemy.size_x,
                        enemy.size_y,
                        enemy.color_tr,
                    )

            for shot in self.Shots:
                pyxel.circ(shot.pos.x, shot.pos.y, shot.size, shot.color)

        else:
            # Выводим сообщение Game Over и меню
            pyxel.text(self.WINDOW_W // 2 - 30, self.WINDOW_H // 2 - 10, "GAME OVER", self.game_over_color)
            pyxel.text(self.WINDOW_W // 2 - 40, self.WINDOW_H // 2 + 10, "1: Start", 7)
            pyxel.text(self.WINDOW_W // 2 - 40, self.WINDOW_H // 2 + 20, "2: Exit", 7)

            # Обработка выбора опции меню
            if pyxel.btnp(pyxel.KEY_1):
                self.reset_game()
            elif pyxel.btnp(pyxel.KEY_2):
                pyxel.quit()

            self.game_over_color = (self.game_over_color + 1) % 16


    def reset_game(self):
        # Сброс параметров игры для нового запуска
        self.game_over_flag = False
        self.menu_option = 0
        self.hero.pos.x = 80
        self.hero.pos.y = 110
        self.Shots = []
        self.Enemies = []
        self.count_died_enemies = 0
        self.game_over_color = 8
        self.create_new_enemies()
        self.score = 0

    def create_new_enemies(self):
        for _ in range(5):
            new_enemy = generate_unique_enemy(self.Enemies, self.WINDOW_W)
            self.Enemies.append(new_enemy)


Game() 