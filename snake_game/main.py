from collections import deque
from copy import copy
from dataclasses import dataclass, field
from math import ceil
from random import randint
from time import time
import pygame
from vector import Vector2D

RESOLUTION = (600, 600)

BOARD_SIZE = (50, 50)

ON_BACKGROUND = (55, 149, 61)
FOOD_COLOR = (215, 38, 61)
BACKGROUND_COLOR = (11, 10, 7)


def create_random_vector2D() -> Vector2D:
    return Vector2D(randint(0, 49), randint(0, 49))


@dataclass(slots=True)
class Snake:
    body: deque[Vector2D] = field(default_factory=lambda: deque([Vector2D(0, 0)]))
    direction: Vector2D = field(default_factory=lambda: Vector2D(1, 0))
    velocity: float = 0.1


@dataclass(slots=True)
class Scene:
    snake: Snake = field(default_factory=Snake)
    food: Vector2D = field(default_factory=create_random_vector2D)
    score: int = 0
    game_over: bool = False


class Render:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.__canvas = pygame.surface.Surface(BOARD_SIZE)
        self.__font = pygame.font.Font("fonts/FreePixel.ttf", 32)
        self.__screen = screen

    def __draw_board(
        self, snake: Snake, food: Vector2D, size: int
    ) -> pygame.surface.Surface:
        self.__canvas.fill(BACKGROUND_COLOR)
        for body_part in snake.body:
            self.__canvas.fill(
                ON_BACKGROUND,
                (
                    body_part.x,
                    body_part.y,
                    1,
                    1,
                ),
            )

        self.__canvas.fill(
            FOOD_COLOR,
            (
                food.x,
                food.y,
                1,
                1,
            ),
        )

        return pygame.transform.scale(self.__canvas, (size, size))

    def draw(self, scene: Scene) -> None:
        self.__screen.fill(BACKGROUND_COLOR)

        if scene.game_over:
            self.draw_game_over_screen(scene.score)

        else:
            board = self.__draw_board(scene.snake, scene.food, RESOLUTION[0] - 64)
            self.__screen.blit(board, (32, 32))

            text = self.__font.render(f"score: {scene.score}", True, ON_BACKGROUND)
            self.__screen.blit(text, (32, 0))
            pygame.draw.rect(
                self.__screen,
                ON_BACKGROUND,
                (32, 32, RESOLUTION[0] - 64, RESOLUTION[1] - 64),
                1,
            )

        pygame.display.flip()

    def draw_game_over_screen(self, score: float) -> None:
        text = self.__font.render(f"GAME OVER", True, ON_BACKGROUND)
        rect = text.get_rect()
        rect.center = (int(600 / 2), int(600 / 2))
        self.__screen.blit(text, rect)

        text = self.__font.render(f"score: {score}", True, ON_BACKGROUND)
        rect = text.get_rect()
        rect.center = (int(600 / 2), int(600 / 2))
        rect.y += 32
        self.__screen.blit(text, rect)

        text = self.__font.render(f"press any key to restart", True, ON_BACKGROUND)
        rect = text.get_rect()
        rect.center = (int(600 / 2), int(600 / 2))
        rect.y += 128
        self.__screen.blit(text, rect)


class Game:
    def __init__(self, render: Render) -> None:
        self.__render = render
        self.__scene = Scene()
        self.__time = 0.0

    def __eat_food(self):
        snake = self.__scene.snake
        food = self.__scene.food
        head = snake.body[0]
        if head == food:
            snake.body.append(copy(head))
            self.__scene.score += 1
            positions = []
            for i in range(BOARD_SIZE[0]):
                for j in range(BOARD_SIZE[1]):
                    position = Vector2D(i, j)
                    if position not in snake.body:
                        positions.append(position)

            new_food_position = positions[randint(0, len(positions) - 1)]
            self.__scene.food = new_food_position

    def __move_snake(self) -> None:
        snake = self.__scene.snake
        head = copy(snake.body[0])
        head += snake.direction
        snake.body.rotate(1)
        snake.body[0] = head

        if head.x >= BOARD_SIZE[0]:
            head.x = 0

        if head.x < 0:
            head.x = BOARD_SIZE[0] - 1

        if head.y >= BOARD_SIZE[1]:
            head.y = 0

        if head.y < 0:
            head.y = BOARD_SIZE[1] - 1

    def __end_game(self):
        body = self.__scene.snake.body
        body_iter = iter(body)
        head = next(body_iter)
        for body in body_iter:
            if head == body:
                self.__scene.game_over = True
                break

    def update(self, delta_time: float) -> None:
        self.__time += delta_time

        if self.__time <= self.__scene.snake.velocity:
            return

        self.__time = 0

        if not self.__scene.game_over:
            self.__end_game()
            self.__eat_food()
            self.__move_snake()

        self.__render.draw(self.__scene)

    def key_down(self, key: int) -> None:
        if self.__scene.game_over:
            self.__scene = Scene()
            return

        snake = self.__scene.snake
        if key == pygame.K_w and snake.direction != Vector2D(0, 1):
            snake.direction = Vector2D(0, -1)
        elif key == pygame.K_s and snake.direction != Vector2D(0, -1):
            snake.direction = Vector2D(0, 1)
        elif key == pygame.K_d and snake.direction != Vector2D(-1, 0):
            snake.direction = Vector2D(1, 0)
        elif key == pygame.K_a and snake.direction != Vector2D(1, 0):
            snake.direction = Vector2D(-1, 0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    render = Render(screen)
    game = Game(render)

    stoped = False

    previous = time()
    while not stoped:
        now = time()
        delta_time = now - previous
        previous = now

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stoped = True

            if event.type == pygame.KEYDOWN:
                game.key_down(event.key)

        game.update(delta_time)

    pygame.quit()


if __name__ == "__main__":
    main()
