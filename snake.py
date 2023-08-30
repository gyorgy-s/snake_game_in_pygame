"""Snake class module for the snake game."""
from random import choice
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DIRECTIONS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}


class Segment:
    """Segment class, to model the body parts of the snake."""

    def __init__(self, x, y, size, direction) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.rect = pygame.Rect(
            self.x * self.size, self.y * self.size, self.size, self.size
        )

    def draw(self, win):
        """Update the Rect location and draw to the screen."""
        self.rect.x = self.x * self.size
        self.rect.y = self.y * self.size
        pygame.draw.rect(win, WHITE, self.rect)


class Snake:
    """Snake class, to modell the behavior of the snake."""

    def __init__(self, x, y, size, lenght) -> None:
        self.x = x
        self.y = y
        self.direction = choice(list(DIRECTIONS.values()))
        self.segments = [
            Segment(
                x + i * -self.direction[0],
                y + i * -self.direction[1],
                size,
                self.direction,
            )
            for i in range(lenght)
        ]
        self.direction_changed = False

    def draw(self, win):
        """Draw each part of the snake to the screen."""
        for segment in self.segments:
            segment.draw(win)

    def move(self):
        """Move the head of the snake and update
        the location and direction for the rest of the body."""
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i - 1].x
            self.segments[i].y = self.segments[i - 1].y
            self.segments[i].direction = self.segments[i - 1].direction

        self.x += self.direction[0]
        self.y += self.direction[1]

        self.segments[0].x = self.x
        self.segments[0].y = self.y

        self.direction_changed = False

    def change_direction(self, direction):
        """Change the direction in which the head of the snake is moviing."""
        if not self.direction_changed:
            self.direction_changed = True
            if direction == DIRECTIONS["w"] and self.direction != DIRECTIONS["s"]:
                self.direction = DIRECTIONS["w"]
            if direction == DIRECTIONS["a"] and self.direction != DIRECTIONS["d"]:
                self.direction = DIRECTIONS["a"]
            if direction == DIRECTIONS["s"] and self.direction != DIRECTIONS["w"]:
                self.direction = DIRECTIONS["s"]
            if direction == DIRECTIONS["d"] and self.direction != DIRECTIONS["a"]:
                self.direction = DIRECTIONS["d"]

    def grow(self, size):
        """Increase the size of the body by one."""
        self.segments.append(
            Segment(
                self.segments[len(self.segments) - 1].x,
                self.segments[len(self.segments) - 1].y,
                size,
                self.segments[len(self.segments) - 1].direction
                # self.x - self.direction[0],
                # self.y - self.direction[1],
                # size,
                # self.direction,
            ),
        )

    def collision(self, rect):
        """Check the head for collision."""
        return self.segments[0].rect.colliderect(rect)

    def self_collision(self):
        """Check if the head is overlaping with any part of the body."""
        coll = False
        for i in range(1, len(self.segments)):
            if self.segments[0].rect.center == self.segments[i].rect.center:
                coll = True
        return coll
