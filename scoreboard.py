from turtle import Turtle
from tkinter.font import Font

SCORE_FONT = ("Terminal", 16, "bold")
GAME_OVER_FONT = ("Terminal", 50, "bold")
X, Y = 0, 1
SCORE_COLOR = "magenta"
GAME_OVER_SHADOW_COLOR = "yellow"
GAME_OVER_COLOR = "red"
TOP_MARGIN = 20
BOTTOM_MARGIN = 10


class Scoreboard(Turtle):

    def __init__(self, up_bound, color=None):
        super().__init__(visible=False)
        color = SCORE_COLOR if color is None else color
        self.score_left = 0
        self.score_right = 0
        self.scoreboard_width = 0
        self.scoreboard_height = self.get_font_height(SCORE_FONT) + TOP_MARGIN + BOTTOM_MARGIN
        self.starting_position = 0, up_bound - (self.scoreboard_height - BOTTOM_MARGIN)
        self.pencolor(color)
        self.speed(0)
        self.penup()
        self.print_score()

    @staticmethod
    def get_font_height(font):
        font_config = Font(font=font)
        font_ascent = font_config.metrics('ascent')  # keep this just for reference
        line_space = font_config.metrics('linespace') - font_ascent
        return int(font_ascent + line_space)

    def print_score(self):
        self.clear()
        self.setposition(self.starting_position)
        baseline_start = self.position()[X]
        self.write(f"{self.score_left}   -   {self.score_right}", move=True, align="center", font=SCORE_FONT)
        baseline_end = self.position()[X]
        self.setposition(self.starting_position)

        self.scoreboard_width = baseline_end - baseline_start

    def print_game_over(self):
        x = 0
        y = - int(self.get_font_height(GAME_OVER_FONT) / 2)
        self.color(GAME_OVER_SHADOW_COLOR)
        rotation_degrees = 45
        for _ in range(int(360 / rotation_degrees)):
            self.setposition(x, y)
            self.right(rotation_degrees)
            self.forward(8)
            self.write("GAME OVER", move=False, align="center", font=GAME_OVER_FONT)

        self.setposition(x, y)
        self.color(GAME_OVER_COLOR)
        self.write("GAME OVER", move=False, align="center", font=GAME_OVER_FONT)

    def increase_score(self, did_left_score):
        if did_left_score:
            self.score_left += 1
        else:
            self.score_right += 1
        self.print_score()
