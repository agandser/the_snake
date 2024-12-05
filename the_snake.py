from random import choice as random_choice

import pygame as pg

# Константы для размеров поля и сетки:
WIN_WIDTH, WIN_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_W = WIN_WIDTH // CELL_SIZE
GRID_H = WIN_HEIGHT // CELL_SIZE

# Направления движения:
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

# Цвет фона - черный:
BG_COLOR = (0, 0, 0)

# Цвет границы ячейки:
CELL_BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
FRUIT_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_BODY_COLOR = (0, 255, 0)

# Скорость движения змейки:
GAME_SPEED = 20

# Настройка игрового окна:
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Snake Game')

# Настройка времени:
timer = pg.time.Clock()


# Тут опишите все классы игры.
class BaseObject:
    """Базовый класс для наследования"""

    def __init__(self) -> None:
        self.coord = ((WIN_WIDTH // 2), (WIN_HEIGHT // 2))
        self.color = None

    def render(self) -> None:
        """Метод для переопределения у потомков"""
        pass


class Fruit(BaseObject):
    """Фрукт"""

    def __init__(self) -> None:
        self.coord = self.new_position()
        self.color = FRUIT_COLOR

    def new_position(self) -> tuple:
        """Возвращает координаты фрукта"""
        x = random_choice(range(0, WIN_WIDTH, 20))
        y = random_choice(range(0, WIN_HEIGHT, 20))
        self.coord = (x, y)
        return (x, y)

    def render(self) -> None:
        """Рисует фрукт"""
        rect = pg.Rect(self.coord, (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(window, self.color, rect)
        pg.draw.rect(window, CELL_BORDER_COLOR, rect, 1)


class Snake(BaseObject):
    """Змейка"""

    def __init__(self) -> None:
        super().__init__()
        self.size = 1
        self.segments = [self.coord]
        self.direction = DIR_RIGHT
        self.next_dir = None
        self.color = SNAKE_BODY_COLOR
        self.prev_tail = None

    def change_direction(self) -> None:
        """Меняет направление"""
        if self.next_dir:
            self.direction = self.next_dir
            self.next_dir = None

    def move_forward(self) -> None:
        """Движение змейки"""
        head = self.get_head()

        new_head = (
            (head[0] + self.direction[0] * 20) % WIN_WIDTH,
            (head[1] + self.direction[1] * 20) % WIN_HEIGHT)
        if new_head in self.segments[2:]:
            self.reset()
            return

        self.segments.insert(0, new_head)
        if len(self.segments) > self.size:
            self.prev_tail = self.segments.pop()

    def render(self) -> None:
        """Рисует змейку"""
        for segment in self.segments[:-1]:
            rect = (pg.Rect(segment, (CELL_SIZE, CELL_SIZE)))
            pg.draw.rect(window, self.color, rect)
            pg.draw.rect(window, CELL_BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.segments[0], (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(window, self.color, head_rect)
        pg.draw.rect(window, CELL_BORDER_COLOR, head_rect, 1)

        if self.prev_tail:
            tail_rect = pg.Rect(self.prev_tail, (CELL_SIZE, CELL_SIZE))
            pg.draw.rect(window, BG_COLOR, tail_rect)

    def get_head(self) -> tuple:
        """Возвращает координаты головы"""
        return self.segments[0]

    def reset(self) -> None:
        """Сбрасывает игру"""
        window.fill(BG_COLOR)
        self.size = 1
        self.coord = ((WIN_WIDTH // 2), (WIN_HEIGHT // 2))
        self.segments = [self.coord]
        self.direction = random_choice((DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN))
        self.next_dir = None
        self.color = SNAKE_BODY_COLOR


def process_keys(player: BaseObject) -> None:
    """Обрабатывает нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and player.direction != DIR_DOWN:
                player.next_dir = DIR_UP
            elif event.key == pg.K_DOWN and player.direction != DIR_UP:
                player.next_dir = DIR_DOWN
            elif event.key == pg.K_LEFT and player.direction != DIR_RIGHT:
                player.next_dir = DIR_LEFT
            elif event.key == pg.K_RIGHT and player.direction != DIR_LEFT:
                player.next_dir = DIR_RIGHT


def main_game():
    """Запуск игры"""
    pg.init()
    snake = Snake()
    fruit = Fruit()

    while True:
        timer.tick(GAME_SPEED)

        process_keys(snake)
        snake.change_direction()
        snake.move_forward()
        if snake.get_head() == fruit.coord:
            snake.size += 1
            fruit.new_position()
        snake.render()
        fruit.render()
        pg.display.update()


if __name__ == '__main__':
    main_game()
