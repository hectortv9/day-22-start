from turtle import Turtle
from screen_box import ScreenBox
from time import sleep

X, Y = 0, 1
POSITIVE, NEGATIVE = 1, -1
COLORS = ("red", "blue", "green", "magenta", "yellow", "orange", "purple", "cyan")
UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"
GRID_EDGE_COLOR = "magenta"
BALL_SHAPE = "circle"
# Visual help variables
GRID_COLOR = "yellow"
FILL_GAP_COLOR = "orange"
FILL_GAP_SHAPE = "circle"

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


class CourtGrid:

    def __init__(self, scoreboard, gap_size, ball_color=None):
        self.gap_size = gap_size
        self.scoreboard = scoreboard

        self.boundaries = self.get_grid_bounds()
        self.up_bound = self.boundaries[UP]
        self.left_bound = self.boundaries[LEFT]
        self.right_bound = self.boundaries[RIGHT]
        self.down_bound = self.boundaries[DOWN]

        self.horizontal_gap_count = int(abs(self.right_bound - self.left_bound) / gap_size)
        self.vertical_gap_count = int(abs(self.up_bound - self.down_bound) / gap_size)
        self.lowest_gap = (int(self.left_bound + gap_size / 2), int(self.down_bound + gap_size / 2))
        self.center_gap = (int(self.horizontal_gap_count / 2) * gap_size + self.lowest_gap[X],
                           int(self.vertical_gap_count / 2) * gap_size + self.lowest_gap[Y])
        # center_gap will lean towards +x, +y when gaps are even, it will get perfectly centered when they are odd

        self.ball = Ball(self.center_gap[X], self.center_gap[Y], ball_color)
        self.bouncing_distance = gap_size * 0.55  # distance at which ball can be considered to bounce against

    def get_nth_gap_x(self, gap_number, from_left_to_right=True):
        if from_left_to_right:
            return (gap_number - 1) * self.gap_size + self.lowest_gap[X]
        else:
            return (self.horizontal_gap_count - gap_number) * self.gap_size + self.lowest_gap[X]

    def get_centered_y(self, shape_height):
        grid_height = self.vertical_gap_count * self.gap_size
        if shape_height > grid_height:
            raise Exception(f"ERROR: INSUFFICIENT SPACE. COURT HEIGHT={grid_height}, SHAPE HEIGHT={grid_height}")
        shape_vertical_gap_count = int(shape_height / self.gap_size)
        if shape_vertical_gap_count % 2 == 0:  # if the vertical gap count is odd
            y = self.center_gap[Y] - int(self.gap_size / 2)
        else:
            y = self.center_gap[Y]
        return y

    def get_visual_help(self):
        self.draw_grid()
        self.draw_grid_edges()
        self.fill_lowest_gaps()

    def draw_grid_edges(self, color=None):
        color = GRID_EDGE_COLOR if color is None else color
        backup_color = ScreenBox().utility_turtle.pencolor()
        speed = ScreenBox().utility_turtle.speed()
        ScreenBox().utility_turtle.speed(0)
        ScreenBox().utility_turtle.pencolor(color)
        turtle = ScreenBox().utility_turtle
        turtle.goto(self.boundaries[LEFT], self.boundaries[UP])
        turtle.pendown()
        turtle.goto(self.boundaries[RIGHT], self.boundaries[UP])
        turtle.goto(self.boundaries[RIGHT], self.boundaries[DOWN])
        turtle.goto(self.boundaries[LEFT], self.boundaries[DOWN])
        turtle.goto(self.boundaries[LEFT], self.boundaries[UP])
        turtle.penup()
        ScreenBox().utility_turtle.pencolor(backup_color)
        ScreenBox().utility_turtle.speed(speed)

    def draw_grid(self):
        color = ScreenBox().utility_turtle.pencolor()
        speed = ScreenBox().utility_turtle.speed()
        ScreenBox().utility_turtle.speed(0)
        ScreenBox().utility_turtle.pencolor(GRID_COLOR)
        turtle = ScreenBox().utility_turtle
        for y in range(self.boundaries[DOWN], self.boundaries[UP] + 1, self.gap_size):
            turtle.goto(self.boundaries[LEFT], y)
            turtle.pendown()
            turtle.goto(self.boundaries[RIGHT], y)
            turtle.penup()
        for x in range(self.boundaries[LEFT], self.boundaries[RIGHT] + 1, self.gap_size):
            turtle.goto(x, self.boundaries[UP])
            turtle.pendown()
            turtle.goto(x, self.boundaries[DOWN])
            turtle.penup()
        ScreenBox().utility_turtle.pencolor(color)
        ScreenBox().utility_turtle.speed(speed)

    def fill_lowest_gaps(self):
        for x in range(self.horizontal_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X] + (x * self.gap_size), self.lowest_gap[Y])
        for y in range(self.vertical_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X], self.lowest_gap[Y] + (y * self.gap_size))

    @staticmethod
    def adjust_boundary(boundary, gap_size):
        # boundary is the distance between origin (0, 0) and a point at a coordinate axes
        # boundary is signed indicating the direction of axis (e.g. +x, -x, +y, -y)
        # grid will be aligned with coordinate axes but they won't overlap
        adjusted_boundary = abs(boundary)  # remove sign to work only with magnitudes
        adjusted_boundary -= abs(boundary) % (gap_size / 2)  # round down to multiples of half gap size
        if adjusted_boundary % gap_size == 0:  # means grid is aligned with origin (0, 0)
            adjusted_boundary -= gap_size / 2  #
        adjusted_boundary = int(adjusted_boundary * (abs(boundary) / boundary))  # recover sign
        return adjusted_boundary

    def get_grid_bounds(self):
        left_bound = ScreenBox().left_bound
        right_bound = ScreenBox().right_bound
        up_bound = ScreenBox().up_bound - self.scoreboard.scoreboard_height
        down_bound = ScreenBox().down_bound

        # calculate amount of gaps that can fit horizontally
        raw_width = abs(left_bound) + abs(right_bound)
        raw_width -= raw_width % self.gap_size
        # calculate amount of gaps that can fit vertically
        raw_height = abs(up_bound) + abs(down_bound)
        raw_height -= raw_height % self.gap_size
        if raw_width < self.gap_size or raw_height < self.gap_size:
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")
        # adjust top boundary with respect to origin and size of grid's gaps
        up = self.adjust_boundary(up_bound, self.gap_size)
        # adjust left boundary with respect to origin and size of grid's gaps
        left = self.adjust_boundary(left_bound, self.gap_size)
        # adjust right boundary with respect to origin and size of grid's gaps
        right = self.adjust_boundary(right_bound, self.gap_size)
        # adjust bottom boundary with respect to origin and size of grid's gaps
        down = self.adjust_boundary(down_bound, self.gap_size)
        if not (up > down and right > left):
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")

        return {UP: up, DOWN: down, LEFT: left, RIGHT: right, }
