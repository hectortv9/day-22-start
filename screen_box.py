import turtle
import math

X, Y = 0, 1
WINDOW_BORDER = 11  # fixed value. Do not modify
LARGE_OFFSET = 10  # tentative fixed value. Do not modify
SMALL_OFFSET = WINDOW_BORDER - LARGE_OFFSET  # fixed formula. Do not modify
UTILITY_TURTLE_COLOR = "red"
SCREEN_MODE = "standard"
SCREEN_COLORMODE = 255
SCREEN_XY_AXES_COLOR = "blue"
SCREEN_BOUNDARIES_COLOR = "red"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_BGCOLOR = "black"
SCREEN_TITLE = "Generic Game"


class _Box:

    screen = None

    def __init__(self):
        if _Box.screen is None:
            ScreenBox()


class _ScreenBox:

    def __init__(self, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT, title=SCREEN_TITLE,
                 bgcolor=SCREEN_BGCOLOR, mode=SCREEN_MODE, colormode=SCREEN_COLORMODE):
        self.screen = _ScreenBox.initialize_screen(
            turtle.Screen(), window_width, window_height, title, bgcolor, mode, colormode)
        self.right_bound = int(math.floor(window_width / 2)) - LARGE_OFFSET
        self.left_bound = -(int(math.floor(window_width / 2)) - SMALL_OFFSET)
        self.up_bound = int(math.floor(window_height / 2)) - SMALL_OFFSET
        self.down_bound = -(int(math.floor(window_height / 2)) - LARGE_OFFSET)
        self.complementary_color = self.get_complementary_color(bgcolor)
        self.utility_turtle = _ScreenBox.initialize_turtle()

    def get_complementary_color(self, color):
        canvas = self.screen.getcanvas()
        root = canvas.winfo_toplevel()
        r, g, b = root.winfo_rgb(color)

        colormode = self.screen.colormode()
        if colormode == 255:
            # the 8-bit shift is because rgb function returns 16 bit integer. Result = 65,535(0xFFFF) to 255(0xFF)
            # Complementary color is the result of subtracting the actual color from the max color value
            r, g, b = colormode - (r >> 8), colormode - (g >> 8), colormode - (b >> 8)
        else:
            pass  # don't know about the other color modes ... research and implement

        return r, g, b

    @staticmethod
    def initialize_screen(screen, window_width, window_height, title, bgcolor, mode, colormode):
        screen.screensize(canvwidth=window_width - 21, canvheight=window_height - 21)
        screen.setup(window_width, window_height)
        screen.mode(mode)
        screen.colormode(colormode)
        screen.bgcolor(bgcolor)
        screen.title(title)
        return screen

    @staticmethod
    def initialize_turtle():
        utility_turtle = turtle.Turtle(visible=False)
        utility_turtle.pensize(1)
        utility_turtle.speed(0)
        utility_turtle.pencolor(UTILITY_TURTLE_COLOR)
        utility_turtle.penup()
        return utility_turtle

    def clear_screen(self):
        backup_color = self.screen.bgcolor()
        backup_mode = self.screen.mode()
        backup_colormode = self.screen.colormode()
        self.screen.clear()
        self.screen.bgcolor(backup_color)
        self.screen.mode(backup_mode)
        self.screen.colormode(backup_colormode)
        self.utility_turtle = _ScreenBox.initialize_turtle()

    def draw_boundaries(self):
        color = self.utility_turtle.pencolor()
        self.utility_turtle.pencolor(SCREEN_BOUNDARIES_COLOR)
        self.draw_poliline(self.left_bound, self.up_bound,
                           (self.right_bound, self.up_bound),
                           (self.left_bound, self.down_bound),
                           (self.right_bound, self.down_bound),
                           (self.left_bound, self.up_bound),
                           (self.left_bound, self.down_bound))
        self.draw_line(self.right_bound, self.up_bound, self.right_bound, self.down_bound)
        self.utility_turtle.pencolor(color)

        color = self.utility_turtle.pencolor()
        self.utility_turtle.pencolor(SCREEN_XY_AXES_COLOR)
        self.draw_line(self.right_bound, 0, self.left_bound, 0)
        self.draw_line(0, self.up_bound, 0, self.down_bound)
        self.utility_turtle.pencolor(color)

    def get_visual_help(self):
        self.draw_boundaries()

    def draw_line(self, xi, yi, xf, yf):
        self.utility_turtle.goto(xi, yi)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(xf, yf)
        self.utility_turtle.penup()

    def draw_poliline(self, xi, yi, *args):
        self.utility_turtle.goto(xi, yi)
        self.utility_turtle.pendown()
        for coordinate in args:
            self.utility_turtle.goto(coordinate[X], coordinate[Y])
        self.utility_turtle.penup()


# ScreenBox singleton ---------------------------------------------------------------------------
def ScreenBox(window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT, title=SCREEN_TITLE,
              bgcolor=SCREEN_BGCOLOR, mode=SCREEN_MODE, colormode=SCREEN_COLORMODE):
    """Return the singleton _ScreenBox object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    if _Box.screen is None:
        _Box.screen = _ScreenBox(window_width, window_height, title, bgcolor, mode, colormode)
    return _Box.screen
