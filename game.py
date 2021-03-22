from screen_box import ScreenBox
from paddle import Paddle
import paddle
import time
import court
import scoreboard
import turtle

UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"  # Key names
INITIAL_DELAY = 0.2
DELAY_DECREMENT = 0.5
DELAY_AFTER_SCORE = 1
SCREEN_TITLE = "Pong"
MAX_SCORE = 10

class Game:

    def __init__(self):

        self.screen_box = ScreenBox(title=SCREEN_TITLE)
        self.screen = self.screen_box.screen
        self.scoreboard = scoreboard.Scoreboard(self.screen_box.up_bound, self.screen_box.complementary_color)
        self.court = court.CourtGrid(self.scoreboard, paddle.PADDLE_WIDTH)
        self.left_paddle_x = self.court.get_nth_gap_x(1, True)
        self.right_paddle_x = self.court.get_nth_gap_x(1, False)
        self.left_paddle = Paddle(self.left_paddle_x, self.court.up_bound, self.court.down_bound,
                                  self.screen_box.complementary_color)
        self.right_paddle = Paddle(self.right_paddle_x, self.court.up_bound, self.court.down_bound,
                                   self.screen_box.complementary_color)
        self.initialize_game()
        # self.get_visual_help()

    def start_listening(self):
        self.screen.onkeypress(self.right_paddle.up, UP)
        self.screen.onkeypress(self.right_paddle.down, DOWN)
        self.screen.onkeypress(self.left_paddle.up, "w")
        self.screen.onkeypress(self.left_paddle.up, "W")
        self.screen.onkeypress(self.left_paddle.down, "s")
        self.screen.onkeypress(self.left_paddle.down, "S")
        self.screen.listen()

    def initialize_game(self):
        self.court.draw_grid_edges(self.screen_box.complementary_color)
        self.start_listening()

    def get_visual_help(self):
        self.screen_box.get_visual_help()
        # self.court.draw_grid()
        self.court.get_visual_help()

    def stop_listening(self):
        self.screen.onkeypress(None, UP)
        self.screen.onkeypress(None, DOWN)
        self.screen.onkeypress(None, "w")
        self.screen.onkeypress(None, "W")
        self.screen.onkeypress(None, "s")
        self.screen.onkeypress(None, "S")

    def do_start_game(self):
        player_input = self.screen.textinput(
            "Get ready", "Close this window whenever you are ready to start playing;\n "
                         "otherwise, type 'quit' and press [OK] to exit game.")
        return player_input is None or player_input.lower() != "quit"

    def play(self):
        delay = INITIAL_DELAY
        while True:
            interactions = self.court.ball.move(self.court, self.left_paddle, self.right_paddle)
            if interactions["did_miss_paddle"]:
                top_y = interactions["paddle_in_turn"].get_top_ycord()
                bottom_y = interactions["paddle_in_turn"].get_bottom_ycord()
                self.court.ball.miss_hit_animation(self.court, top_y, bottom_y, delay, DELAY_AFTER_SCORE)
                delay = INITIAL_DELAY
                self.scoreboard.increase_score(court.x_direction < 0)
                if self.scoreboard.score_left >= MAX_SCORE or self.scoreboard.score_right >= MAX_SCORE:
                    self.stop_listening()
                    self.scoreboard.print_game_over()
                    break
                self.court.ball.reset_ball()
            elif interactions["did_hit_paddle"]:
                delay = delay * DELAY_DECREMENT
            time.sleep(delay)
        self.screen.textinput(
            "GAME OVER", f"The final score is  {self.scoreboard.score_left} - {self.scoreboard.score_right}.  "
                         f"Close this dialog to continue.")
        self.screen_box.clear_screen()
