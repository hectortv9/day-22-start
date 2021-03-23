from screen_box import ScreenBox
from turtle import Turtle
from time import sleep

POSITIVE, NEGATIVE = 1, -1

COLORS = ("red", "blue", "green", "magenta", "yellow", "orange", "purple", "cyan")
BALL_SHAPE = "circle"
BALL_SPEED = 10  # displacement in pixels
x_direction = POSITIVE
y_direction = POSITIVE


class Ball(Turtle):

    def __init__(self, x, y, ball_color=None):
        super().__init__(shape=BALL_SHAPE, visible=True)
        if ball_color is None:
            ball_color = ScreenBox().complementary_color
        self.ball_color = ball_color
        self.x_center = x
        self.y_center = y
        self.color(ball_color)
        self.penup()
        self.speed(0)
        self.setposition(x, y)
        self.showturtle()

    def validate_vertical_travel(self, up_bound, down_bound, bouncing_distance):
        global y_direction
        if y_direction == POSITIVE:
            distance = abs(up_bound - self.ycor())
            if distance < bouncing_distance:
                y_direction = NEGATIVE
        else:
            distance = abs(self.ycor() - down_bound)
            if distance < bouncing_distance:
                y_direction = POSITIVE

    def miss_hit_animation(self, court, top_y, bottom_y, animation_sleep, final_sleep):
        global x_direction, y_direction
        self.change_color()
        self.validate_vertical_travel(bottom_y, top_y, court.bouncing_distance)
        edge_case = 1  # If equal to 1 means no edge case is present
        if self.ycor() > 0 and abs(court.up_bound - top_y) <= court.gap_size + court.bouncing_distance:
            edge_case = 0  # Trigger edge case
        elif self.ycor() < 0 and abs(court.down_bound - bottom_y) <= court.gap_size + court.bouncing_distance:
            edge_case = 0  # Trigger edge case
        if x_direction == POSITIVE:
            while True:
                sleep(animation_sleep)
                distance = court.right_bound - self.xcor()
                if distance < court.bouncing_distance:
                    break
                self.setposition(self.xcor() + BALL_SPEED * x_direction,
                                 self.ycor() + BALL_SPEED * y_direction * edge_case)
            x_direction = NEGATIVE
        else:
            while True:
                sleep(animation_sleep)
                distance = self.xcor() - court.left_bound
                if distance < court.bouncing_distance:
                    break
                self.setposition(self.xcor() + BALL_SPEED * x_direction,
                                 self.ycor() + BALL_SPEED * y_direction * edge_case)
            x_direction = POSITIVE
        sleep(final_sleep)

    def move(self, court, left_paddle, right_paddle):
        global x_direction
        self.validate_vertical_travel(court.up_bound, court.down_bound, court.bouncing_distance)
        did_miss_paddle = False
        did_hit_paddle = False
        paddle_in_turn = None
        if x_direction == POSITIVE:
            distance = right_paddle.x_left - self.xcor()
            if distance < court.bouncing_distance:
                if right_paddle.get_top_ycord() >= self.ycor() >= right_paddle.get_bottom_ycord():
                    x_direction = NEGATIVE
                    did_hit_paddle = True
                else:
                    did_miss_paddle = True
                    paddle_in_turn = right_paddle
        else:
            distance = self.xcor() - left_paddle.x_right
            if distance < court.bouncing_distance:
                if left_paddle.get_top_ycord() >= self.ycor() >= left_paddle.get_bottom_ycord():
                    x_direction = POSITIVE
                    did_hit_paddle = True
                else:
                    did_miss_paddle = True
                    paddle_in_turn = left_paddle
        if not did_miss_paddle:
            self.setposition(self.xcor() + BALL_SPEED * x_direction, self.ycor() + BALL_SPEED * y_direction)
        return {"did_miss_paddle": did_miss_paddle, "did_hit_paddle": did_hit_paddle, "paddle_in_turn": paddle_in_turn}

    def reset_ball(self):
        self.color(self.ball_color)
        self.setposition(self.x_center, self.y_center)

    def change_color(self):
        # self.color(random.choice(COLORS))
        self.color(COLORS[0])
