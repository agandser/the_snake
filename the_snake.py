from random import choice as random_choice

import pygame as pg

# Константы для размеров поля и сетки:
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Направления движения:
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

# Цвет фона - черный:
BG_COLOR = (0, 0, 0)

# Цвет границы ячейки:
GRID_BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_FILL_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_FILL_COLOR = (0, 255, 0)

# Скорость игры:
MOVE_SPEED = 20

# Настройка окна:
game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# Заголовок окна:
pg.display.set_caption('Snake')

# Таймер:
game_clock = pg.time.Clock()


# Определение классов игры.
class GameObject:
    """Родительский класс"""

    def __init__(self) -> None:
        self.position = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.color = None

    def draw(self) -> None:
        """Для переопределения в наследниках"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self) -> None:
        self.position = self.new_position()
        self.color = APPLE_FILL_COLOR

    def new_position(self) -> tuple:
        """Генерация случайной позиции"""
        x_coord = random_choice(range(0, WINDOW_WIDTH, 20))
        y_coord = random_choice(range(0, WINDOW_HEIGHT, 20))
        self.position = (x_coord, y_coord)
        return (x_coord, y_coord)

    def draw(self) -> None:
        """Отображение яблока"""
        rect = pg.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(game_window, self.color, rect)
        pg.draw.rect(game_window, GRID_BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.body = [self.position]
        self.direction = DIR_RIGHT
        self.next_direction = None
        self.color = SNAKE_FILL_COLOR
        self.previous_tail = None

    def update_direction(self) -> None:
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Движение змейки"""
        head = self.get_head()

        new_head = (
            (head[0] + self.direction[0] * CELL_SIZE) % WINDOW_WIDTH,
            (head[1] + self.direction[1] * CELL_SIZE) % WINDOW_HEIGHT
        )
        if new_head in self.body[2:]:
            self.reset()
            return

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.previous_tail = self.body.pop()

    def draw(self) -> None:
        """Рисует змейку"""
        for segment in self.body[:-1]:
            rect = pg.Rect(segment, (CELL_SIZE, CELL_SIZE))
            pg.draw.rect(game_window, self.color, rect)
            pg.draw.rect(game_window, GRID_BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.body[0], (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(game_window, self.color, head_rect)
        pg.draw.rect(game_window, GRID_BORDER_COLOR, head_rect, 1)

        if self.previous_tail:
            tail_rect = pg.Rect(self.previous_tail, (CELL_SIZE, CELL_SIZE))
            pg.draw.rect(game_window, BG_COLOR, tail_rect)

    def get_head(self) -> tuple:
        """Возвращает текущую позицию головы"""
        return self.body[0]

    def reset(self) -> None:
        """Сброс игры"""
        game_window.fill(BG_COLOR)
        self.length = 1
        self.position = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.body = [self.position]
        self.direction = random_choice((DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN))
        self.next_direction = None


def handle_input(snake: GameObject) -> None:
    """Обработка ввода"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DIR_DOWN:
                snake.next_direction = DIR_UP
            elif event.key == pg.K_DOWN and snake.direction != DIR_UP:
                snake.next_direction = DIR_DOWN
            elif event.key == pg.K_LEFT and snake.direction != DIR_RIGHT:
                snake.next_direction = DIR_LEFT
            elif event.key == pg.K_RIGHT and snake.direction != DIR_LEFT:
                snake.next_direction = DIR_RIGHT


def main():
    """Основной цикл игры"""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        game_clock.tick(MOVE_SPEED)

        handle_input(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head() == apple.position:
            snake.length += 1
            apple.new_position()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
