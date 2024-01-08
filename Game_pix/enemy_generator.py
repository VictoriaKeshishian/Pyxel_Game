
import random
from enemy import Enemy

def generate_unique_enemy(existing_enemies, window_width):
    new_enemy = Enemy(0)
    pos_x = random.choice(range(0, window_width - new_enemy.size_x))
    pos_y = new_enemy.spawn_y

    # Проверка на пересечение с другими врагами
    while any(
            enemy.pos.x < pos_x + new_enemy.size_x and
            enemy.pos.x + enemy.size_x > pos_x and
            enemy.pos.y < pos_y + new_enemy.size_y and
            enemy.pos.y + enemy.size_y > pos_y
            for enemy in existing_enemies
    ):
        pos_x = random.choice(range(0, window_width - new_enemy.size_x))

    new_enemy.pos.x = pos_x
    new_enemy.pos.y = pos_y
    return new_enemy