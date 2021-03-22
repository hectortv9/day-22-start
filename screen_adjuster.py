from turtle import Screen, Turtle, TurtleScreen

# w*h= 648*648, [2]
# w*h= 649*649, [3]
# w*h= 667*667, [21]

# from 649*649[3] to 667*667[21] there's one-to-one increment between window size and border.
# After that 21 is constant. This applies only for square windows (width = height)

TURTLE_SIZE = 20
UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"
SHIFT_L, SHIFT_R, ESCAPE, TAB = "Shift_L", "Shift_R", "Escape", "Tab"
snapshots = []
recurse = True
border_flag = False

# Customizable setup values below
SQUARE_RATIO_MODE = False  # Toggle this flag to adjust borders/window sides independently
increment = 1
window_width = 800
border_width = 20
window_height = 600 if not SQUARE_RATIO_MODE else window_width
border_height = 20 if not SQUARE_RATIO_MODE else border_width
print(f"INITIALIZING: w*h = {window_width}*{window_height}  [{border_width}*{border_height}]  +{increment}")
print(f"SQUARE_RATIO_MODE = {SQUARE_RATIO_MODE}")
print(("Adjusting: " + ("BORDERS\n" if border_flag else "WINDOW\n")) if not SQUARE_RATIO_MODE else "")


def print_snapshots():
    print("\n\n\nSaved snapshots:\n----------------\n")
    for item in snapshots:
        print(item)


def start_adjusting():
    adjust()
    print_snapshots()


def print_window_data():
    print(f"w*h=  {window_width}*{window_height}  [{border_width}*{border_height}]  +{increment}")


def adjust():

    if SQUARE_RATIO_MODE:
        def increase_window():
            global window_width, window_height
            window_width += increment
            window_height += increment
            screen.bye()

        def decrease_window():
            global window_width, window_height
            window_width -= increment
            window_height -= increment
            screen.bye()

        def increase_border():
            global border_width, border_height
            border_width += increment
            border_height += increment
            screen.bye()

        def decrease_border():
            global border_width, border_height
            border_width -= increment
            border_height -= increment
            screen.bye()

        def change_window_width_and_height():
            global window_width, window_height
            while True:
                user_input = screen.numinput("Change window width and height",
                                             "Enter a natural number (positive integer grater than zero):",
                                             window_width)
                if user_input is not None:
                    break
            window_width = int(user_input)
            window_height = int(user_input)
            screen.bye()
            print_window_data()

        def change_borders():
            global border_width, border_height
            while True:
                user_input = screen.numinput("Change border width and height",
                                             "Enter a natural number (positive integer grater than zero):",
                                             border_width)
                if user_input is not None:
                    break
            border_width = int(user_input)
            border_height = int(user_input)
            screen.bye()
            print_window_data()
    else:
        def increase_window_width():
            global window_width
            window_width += increment
            screen.bye()

        def increase_window_height():
            global window_height
            window_height += increment
            screen.bye()

        def decrease_window_width():
            global window_width
            window_width -= increment
            screen.bye()

        def decrease_window_height():
            global window_height
            window_height -= increment
            screen.bye()

        def increase_border_width():
            global border_width
            border_width += increment
            screen.bye()

        def increase_border_height():
            global border_height
            border_height += increment
            screen.bye()

        def decrease_border_width():
            global border_width
            border_width -= increment
            screen.bye()

        def decrease_border_height():
            global border_height
            border_height -= increment
            screen.bye()

        def change_window_width():
            global window_width
            while True:
                user_input = screen.numinput("Change window width",
                                             "Enter a natural number (positive integer grater than zero):",
                                             window_width)
                if user_input is not None:
                    break
            window_width = int(user_input)
            screen.bye()
            print_window_data()

        def change_window_height():
            global window_height
            while True:
                user_input = screen.numinput("Change window height",
                                             "Enter a natural number (positive integer grater than zero):",
                                             window_height)
                if user_input is not None:
                    break
            window_height = int(user_input)
            screen.bye()
            print_window_data()

        def change_borders():
            global border_width, border_height
            while True:
                width = screen.numinput("Change border width",
                                        "Enter a natural number (positive integer grater than zero):",
                                        border_width)
                if width is not None:
                    break
            border_width = int(width)
            while True:
                height = screen.numinput("Change border height",
                                         "Enter a natural number (positive integer grater than zero):",
                                         border_height)
                if height is not None:
                    break
            border_height = int(height)
            screen.bye()
            print_window_data()

    def change_increment():
        global increment
        while True:
            user_input = screen.numinput("Change increment",
                                         "Enter a natural number (positive integer grater than zero):", increment)
            if user_input is not None:
                break
        increment = int(user_input)
        print_window_data()

    def save_snapshot():
        global snapshots
        snapshots.append(f"w*h= {window_width}*{window_height}  [{border_width}*{border_height}]")

    def stop_recursion():
        global recurse
        recurse = False
        screen.bye()

    def toggle_border_flag():
        global border_flag
        border_flag = not border_flag
        if border_flag:
            print("Adjusting: BORDERS")
        else:
            print("Adjusting: WINDOW")
        screen.bye()

    canvas_width = window_width - border_width
    canvas_height = window_height - border_height
    screen = Screen()
    screen.screensize(canvwidth=canvas_width, canvheight=canvas_height)
    screen.setup(window_width, window_height)
    turtle = Turtle("circle")
    turtle.shapesize(min(canvas_width, canvas_height) / TURTLE_SIZE)
    print(f"w*h= {screen.window_width()}*{screen.window_height()}  [{screen.canvwidth}*{screen.canvheight}] <<turtle>>")
    if SQUARE_RATIO_MODE:
        screen.onkey(increase_window, RIGHT)
        screen.onkey(decrease_window, LEFT)
        screen.onkey(increase_border, UP)
        screen.onkey(decrease_border, DOWN)
        screen.onkey(change_window_width_and_height, "w")
        screen.onkey(change_window_width_and_height, "W")
        screen.onkey(change_window_width_and_height, "h")
        screen.onkey(change_window_width_and_height, "H")
    else:
        screen.onkey(toggle_border_flag, TAB)
        screen.onkey(change_window_width, "w")
        screen.onkey(change_window_width, "W")
        screen.onkey(change_window_height, "h")
        screen.onkey(change_window_height, "H")
        if border_flag:
            screen.onkey(increase_border_width, RIGHT)
            screen.onkey(decrease_border_width, LEFT)
            screen.onkey(increase_border_height, UP)
            screen.onkey(decrease_border_height, DOWN)
        else:
            screen.onkey(increase_window_width, RIGHT)
            screen.onkey(decrease_window_width, LEFT)
            screen.onkey(increase_window_height, UP)
            screen.onkey(decrease_window_height, DOWN)

    screen.onkey(change_borders, "b")
    screen.onkey(change_borders, "B")
    screen.onkey(change_increment, SHIFT_L)
    screen.onkey(change_increment, SHIFT_R)
    screen.onkey(save_snapshot, "s")
    screen.onkey(save_snapshot, "S")
    screen.onkey(stop_recursion, ESCAPE)
    screen.listen()
    print_window_data()

    screen.mainloop()
    TurtleScreen._RUNNING = True  # Avoid Terminator exception when creating turtle after closing screen
    if recurse:
        adjust()


def draw_window_with_custom_values():
    # w*h= 648*648, [2]
    # w*h= 649*649, [3]
    # w*h= 667*667, [21]
    width = 666
    height = 655

    if width <= 648:
        horizontal_border = 2
    elif width >= 667:
        horizontal_border = 21
    else:
        horizontal_border = width - 646 - 9

    if height <= 648:
        vertical_border = 2
    elif height >= 667:
        vertical_border = 21
    else:
        vertical_border = height - 646

    Screen().screensize(canvwidth=width - horizontal_border, canvheight=height - vertical_border)
    Screen().setup(width, height)
    print(width, height, horizontal_border, vertical_border)
    Screen().exitonclick()


def no_scrollbars_square_window(width):
    # w*h= 648*648, [2]
    # w*h= 649*649, [3]
    # w*h= 667*667, [21]
    # width = [300, 450, 511, 648, 649, 650, 666, 667, 668, 670, 811, 945]
    # for w in width:
    #     no_scrollbars_square_window(w)

    w = width
    h = w

    if w <= 648:
        b = 2
    elif w >= 667:
        b = 21
    else:
        b = w - 646

    Screen().screensize(canvwidth=w - b, canvheight=h - b)
    Screen().setup(w, h)
    print(w, h, b)
    Screen().exitonclick()


if __name__ == '__main__' or __name__ == '__screen_adjuster__':
    start_adjusting()
