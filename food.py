"""Food module for the snake game."""
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



class Food:
    """Food class, to model the food to grow the snake."""

    def __init__(self, x, y, size) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(
            self.x * self.size, self.y * self.size, self.size, self.size
        )

    def draw(self, win, img):
        """Draw the food on the window."""
        self.rect.x = self.x * self.size
        self.rect.y = self.y * self.size
        # pygame.draw.rect(win, GREEN, self.rect)
        win.blit(img, self.rect)

    def eaten(self, x, y):
        """Update the location of the food."""
        self.x = x
        self.y = y
