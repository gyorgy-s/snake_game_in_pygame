"""Main module for the snake game."""
from random import randint
import pygame
from snake import Snake
from food import Food
from score import Score

pygame.init()

SEGMENT_SIZE = 20

INITIAL_SNAKE_LENGHT = 3


desktop_sizes = pygame.display.get_desktop_sizes()
desktop_size = desktop_sizes[0]
WIDTH, HEIGHT = (
    (int(desktop_size[0] * 0.8) // SEGMENT_SIZE) * SEGMENT_SIZE,
    (int(desktop_size[1] * 0.8) // SEGMENT_SIZE) * SEGMENT_SIZE,
)

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

UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)


def draw(win, snake, food, score):
    """Draw the main window."""
    win.fill(BLACK)
    snake.draw(win)
    food.draw(win)
    score.draw_score(win, 24, 10, 10)
    pygame.display.update()


def final_score(win, score):
    """Draw the final sore on the screen."""
    score.draw_final_score(win, 72)
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
        if playing:
            draw(window, snake, food, score)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOVE_TIMER and playing:
                snake.move()
                if snake.collision(food.rect):
                    food.eaten(
                        randint(0 + SEGMENT_SIZE, WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE,
                        randint(0 + SEGMENT_SIZE, HEIGHT - SEGMENT_SIZE)
                        // SEGMENT_SIZE,
                    )
                    snake.grow(SEGMENT_SIZE)
                    score.score = +1
                if (not snake.collision(window_border)) or snake.self_collision():
                    session_end = pygame.time.get_ticks()
                    playing = False
                    score.update_time(session_end - session_start)
                    final_score(window, score)

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
