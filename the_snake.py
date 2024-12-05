from random import choice, randint

import pygame as pg

# Константы для размеров игрового окна и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Возможные направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ALL_DIRECTION = (UP, DOWN, LEFT, RIGHT)
TURNS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Цветовая палитра:
BOARD_BACKGROUND_COLOR = (128, 128, 128)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (63, 161, 119)

# Скорость игры:
SPEED = 10

# Настройка экрана:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна:
pg.display.set_caption('Snake Game: Press ESC to Quit')

# Таймер для управления FPS:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: tuple = None) -> None:
        """Инициализация объекта."""
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки."""
        raise NotImplementedError(f'Redefine draw in {type(self).__name__}.')

    def draw_cell(self, position, body_color=None, border_color=BORDER_COLOR):
        """Отрисовка одного квадрата."""
        body_color = body_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self, positions_taken: tuple = CENTER, body_color: tuple = APPLE_COLOR) -> None:
        """Инициализация атрибутов."""
        super().__init__(body_color)
        self.randomize_position(positions_taken)

    def randomize_position(self, positions_taken) -> tuple:
        """Генерация случайного положения яблока."""
        while self.position in positions_taken:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self, body_color: tuple = SNAKE_COLOR) -> None:
        """Инициализация змейки."""
        super().__init__(body_color)
        self.reset()

    def move(self) -> None:
        """Перемещение змейки."""
        x_position, y_position = self.get_head_position()
        x_next_position, y_next_position = self.direction
        self.positions.insert(
            0,
            ((x_position + x_next_position * GRID_SIZE) % SCREEN_WIDTH,
             (y_position + y_next_position * GRID_SIZE) % SCREEN_HEIGHT))
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def update_direction(self, next_direction) -> None:
        """Изменение направления движения."""
        self.direction = next_direction

    def get_head_position(self) -> tuple:
        """Получение координат головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Перезапуск змейки."""
        self.last = None
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTION)

    def draw(self) -> None:
        """Отрисовка змейки."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)


def handle_keys(snake) -> None:
    """Обработка ввода пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            snake.update_direction(
                TURNS.get((snake.direction, event.key), snake.direction))


def main():
    """Основной игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
