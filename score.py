"""Score module for the snake game."""
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Score:
    """Score class, to kepp track of the nember of the eaten food, and time elapsed."""

    def __init__(self) -> None:
        self.score = 0
        self.time = 0
        self.font_type = pygame.font.get_default_font()
        self.font = None

    def draw_score(self, win, size, x, y):
        """Draw the score on screen."""
        self.font = pygame.font.Font(self.font_type, size)
        ren = self.font.render(str(self.score), 1, WHITE)
        win.blit(ren, (x, y))

    def draw_final_score(self, win, size):
        """Draw the final score on the screen and prompt to exit or restart."""
        final_score_font = pygame.font.Font(self.font_type, size)
        message_font = pygame.font.Font(self.font_type, size // 2)

        message_first = f"You ded, your final score is {self.score}"
        message_second = f"The round lasted for {self.time} seconds"
        message_third = "Pres ESC to quit or ENTER to try again"

        ren_first = final_score_font.render(message_first, 1, WHITE)
        ren_second = final_score_font.render(message_second, 1, WHITE)
        ren_third = message_font.render(message_third, 1, WHITE)

        win_size = win.get_size()
        size_first = list(ren_first.get_size())
        size_second = list(ren_second.get_size())
        size_third = list(ren_third.get_size())

        ulc_first = (
            win_size[0] // 2 - size_first[0] // 2,
            win_size[1] // 2 - size_first[1],
        )
        ulc_second = (
            win_size[0] // 2 - size_second[0] // 2,
            win_size[1] // 2 + size_second[1],
        )
        ulc_third = (
            win_size[0] // 2 - size_third[0] // 2,
            win_size[1] // 2 + size_second[1] * 2 + size_third[1],
        )

        win.blit(ren_first, ulc_first)
        win.blit(ren_second, ulc_second)
        win.blit(ren_third, ulc_third)

    def update_time(self, time: int):
        """Updates the time."""
        self.time = round(time / 1000, 2)

    def get_time(self):
        """Return the time."""
        return self.time
