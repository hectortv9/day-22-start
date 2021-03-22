from screen_box import ScreenBox
from game import Game

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
if __name__ == '__main__':

    while True:
        game = Game()
        if game.do_start_game():
            game.play()
        else:
            break
