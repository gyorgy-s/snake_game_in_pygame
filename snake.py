"""Snake class module for the snake game."""
from random import choice
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DIRECTIONS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}

TEST = [[0, -1, 0, 1], [-1, 0, 1, 0]]
TEST2 = {
    "0-1": "w",
    "-10": "a",
    "01": "s",
    "10": "d",
}

ROTATION = {
    0: {-1: 90, 1: 270},
    1: {0: 0},
    -1: {0: 180},
}


BENDS = {
    "w-a": 90,
    "w-d": 180,
    "a-w": 270,
    "a-s": 180,
    "s-a": 90,
    "s-d": 270,
    "d-w": 90,
    "d-s": 180,
}


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

    def draw(self, win, img, rotation=0):
        """Update the Rect location and draw to the screen."""
        self.rect.x = self.x * self.size
        self.rect.y = self.y * self.size
        # pygame.draw.rect(win, WHITE, self.rect)
        img = pygame.transform.rotate(img, rotation)
        win.blit(img, self.rect)


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

    def draw(self, win, img):
        """Draw each part of the snake to the screen."""
        for i in range(len(self.segments) - 1, -1, -1):
            if i == 0:
                self.segments[0].draw(
                    win,
                    img["head"],
                    ROTATION[self.segments[i].direction[0]][
                        self.segments[i].direction[1]
                    ],
                )
            elif i == len(self.segments) - 1:
                self.segments[i].draw(
                    win,
                    img["tail"],
                    ROTATION[self.segments[i].direction[0]][
                        self.segments[i].direction[1]
                    ],
                )
            else:
                if self.segments[i + 1].x - self.segments[i - 1].x == 0:
                    self.segments[i].draw(win, img["body-v"])
                elif self.segments[i + 1].y - self.segments[i - 1].y == 0:
                    self.segments[i].draw(win, img["body-h"])
                    # this_temp_x = str(self.segments[i].direction[0])
                    # this_temp_y = str(self.segments[i].direction[1])
                    # this_lookup = this_temp_x + this_temp_y
                    # prev_temp_x = str(self.segments[i - 1].direction[0])
                    # prev_temp_y = str(self.segments[i - 1].direction[1])
                    # prev_lookup = prev_temp_x + prev_temp_y
                    # rotation = BENDS[TEST2[this_lookup] + "-" + TEST2[prev_lookup]]
                    # self.segments[i].draw(win, img["bend"], rotation)
                    # is_bend = [self.segments[i].direction[0] + self.segments[i-1].direction[0], self.segments[i].direction[1] + self.segments[i-1].direction[1]]

                    # if self.segments[i].direction
                    pass

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
        self.segments[0].direction = self.direction

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
