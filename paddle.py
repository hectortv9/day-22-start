from turtle import Turtle

paddle_color = "magenta"
PADDLE_WIDTH = 20
X, Y = 0, 1
UPWARD, DOWNWARD = PADDLE_WIDTH, -PADDLE_WIDTH


def set_default_paddle_color(color=paddle_color):
    global paddle_color
    paddle_color = color


class Paddle(Turtle):

    def __init__(self, paddle_height_stretch, is_left_paddle, nth_gap_from_border, court, color=None):
        super().__init__(shape="square", visible=False)
        self.stretch_wid = paddle_height_stretch
        self.paddle_width = PADDLE_WIDTH
        self.paddle_height = self.paddle_width * self.stretch_wid
        self.x_center = court.get_nth_gap_x(nth_gap_from_border, is_left_paddle)
        self.x_left = self.x_center - int(self.paddle_width / 2)
        self.x_right = self.x_center + int(self.paddle_width / 2)
        self.y_center = court.get_centered_y(self.paddle_height)
        self.y_max = court.up_bound - int(self.paddle_height / 2)
        self.y_min = court.down_bound + int(self.paddle_height / 2)
        color = paddle_color if color is None else color
        self.penup()
        self.speed(0)
        self.shapesize(stretch_wid=self.stretch_wid, stretch_len=1)
        self.color(color)
        self.setposition(self.x_center, self.y_center)
        self.showturtle()

    def get_top_ycord(self):
        return self.ycor() + (self.paddle_height / 2)

    def get_bottom_ycord(self):
        return self.ycor() - (self.paddle_height / 2)

    @staticmethod
    def move_paddle(paddle, direction):
        paddle.setposition(paddle.xcor(), paddle.ycor() + direction)

    def up(self):
        if self.ycor() < self.y_max:
            Paddle.move_paddle(self, UPWARD)

    def down(self):
        if self.ycor() > self.y_min:
            Paddle.move_paddle(self, DOWNWARD)
