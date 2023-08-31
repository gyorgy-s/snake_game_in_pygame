"""Main module for the snake game."""
import os
from random import randint
import pygame
from snake import Snake
from food import Food
from score import Score

pygame.init()


INITIAL_SNAKE_LENGHT = 10


desktop_size = pygame.display.get_desktop_sizes()
desktop_size = list(desktop_size[0])
desktop_size.sort()

SEGMENT_SIZE = desktop_size[0] // 48
SEGMENT_COUNT = 30

WIDTH, HEIGHT = SEGMENT_COUNT * SEGMENT_SIZE, SEGMENT_COUNT * SEGMENT_SIZE

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sanke")

window_border = window.get_rect()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60
MOVE_TIMER = pygame.USEREVENT
pygame.time.set_timer(MOVE_TIMER, 100)

UP = [0, -1]
LEFT = [-1, 0]
DOWN = [0, 1]
RIGHT = [1, 0]

grass1 = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "grass_tile4.png")).convert(),
    (SEGMENT_SIZE, SEGMENT_SIZE),
)
grass2 = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "grass_tile5.png")).convert(),
    (SEGMENT_SIZE, SEGMENT_SIZE),
)

apple = pygame.transform.scale(
    pygame.image.load("assets/apple.png").convert_alpha(), (SEGMENT_SIZE, SEGMENT_SIZE)
)

snake_body = {
    "head": pygame.transform.scale(
        pygame.image.load("assets/head.png").convert_alpha(),
        (SEGMENT_SIZE, SEGMENT_SIZE),
    ),
    "body-h": pygame.transform.scale(
        pygame.image.load("assets/body.png").convert_alpha(),
        (SEGMENT_SIZE, SEGMENT_SIZE),
    ),
    "body-v": pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load("assets/body.png").convert_alpha(),
            (SEGMENT_SIZE, SEGMENT_SIZE),
        ),
        90,
    ),
    "tail": pygame.transform.scale(
        pygame.image.load("assets/tail.png").convert_alpha(),
        (SEGMENT_SIZE, SEGMENT_SIZE),
    ),
    "bend-0": pygame.transform.scale(
        pygame.image.load("assets/bend.png").convert_alpha(),
        (SEGMENT_SIZE, SEGMENT_SIZE),
    ),
    "bend-90": pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load("assets/bend.png").convert_alpha(),
            (SEGMENT_SIZE, SEGMENT_SIZE),
        ),
        90,
    ),
    "bend-180": pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load("assets/bend.png").convert_alpha(),
            (SEGMENT_SIZE, SEGMENT_SIZE),
        ),
        180,
    ),
    "bend-270": pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load("assets/bend.png").convert_alpha(),
            (SEGMENT_SIZE, SEGMENT_SIZE),
        ),
        270,
    ),
}


def draw_BG(win):
    for y in range(0, SEGMENT_COUNT, 1):
        for x in range(SEGMENT_COUNT):
            if y % 2:
                if x % 2:
                    win.blit(grass1, (x * SEGMENT_SIZE, y * SEGMENT_SIZE))
                else:
                    win.blit(grass2, (x * SEGMENT_SIZE, y * SEGMENT_SIZE))
            else:
                if x % 2:
                    win.blit(grass2, (x * SEGMENT_SIZE, y * SEGMENT_SIZE))
                else:
                    win.blit(grass1, (x * SEGMENT_SIZE, y * SEGMENT_SIZE))


def draw(win, snake, food, score):
    """Draw the main window."""
    draw_BG(win)
    food.draw(win, apple)
    snake.draw(win, snake_body)
    score.draw_score(win, SEGMENT_SIZE, 10, 10)
    pygame.display.flip()


def final_score(win, score):
    """Draw the final sore on the screen."""
    score.draw_final_score(win, int(SEGMENT_SIZE * 1.5))
    pygame.display.update()


def main():
    """Main game loop."""
    run = True
    clock = pygame.time.Clock()
    snake = Snake(
        (WIDTH // SEGMENT_SIZE) // 2,
        (HEIGHT // SEGMENT_SIZE) // 2,
        SEGMENT_SIZE,
        INITIAL_SNAKE_LENGHT,
    )

    food = Food(
        randint(0 + SEGMENT_SIZE, WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE,
        randint(0 + SEGMENT_SIZE, HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE,
        SEGMENT_SIZE,
    )

    score = Score()
    playing = True
    session_start = 0
    session_end = 0

    while run:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        if playing:
            draw(window, snake, food, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOVE_TIMER and playing:
                snake.move()
                if (not snake.collision(window_border)) or snake.self_collision():
                    session_end = pygame.time.get_ticks()
                    playing = False
                    score.update_time(session_end - session_start)
                    final_score(window, score)
                if snake.collision(food.rect):
                    food.eaten(
                        randint(0 + SEGMENT_SIZE, WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE,
                        randint(0 + SEGMENT_SIZE, HEIGHT - SEGMENT_SIZE)
                        // SEGMENT_SIZE,
                    )
                    snake.grow(SEGMENT_SIZE)
                    score.score += 1

            if keys_pressed[pygame.K_w]:
                snake.change_direction(UP)
            if keys_pressed[pygame.K_a]:
                snake.change_direction(LEFT)
            if keys_pressed[pygame.K_s]:
                snake.change_direction(DOWN)
            if keys_pressed[pygame.K_d]:
                snake.change_direction(RIGHT)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_RETURN:
                    clock = pygame.time.Clock()
                    snake = Snake(
                        (WIDTH // SEGMENT_SIZE) // 2,
                        (HEIGHT // SEGMENT_SIZE) // 2,
                        SEGMENT_SIZE,
                        INITIAL_SNAKE_LENGHT,
                    )

                    food = Food(
                        randint(0, WIDTH) // SEGMENT_SIZE,
                        randint(0, HEIGHT) // SEGMENT_SIZE,
                        SEGMENT_SIZE,
                    )

                    score = Score()
                    playing = True
                    session_start = pygame.time.get_ticks()


if __name__ == "__main__":
    main()
