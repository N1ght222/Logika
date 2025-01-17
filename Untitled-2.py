import sys
import time
import pygame
import threading
import os
from colorama import init, Fore, Style

init()

__HEART__ = '''

          @@@@@@@@@@@                @@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@
   @@@@@@@@@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@
 @@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@
 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@@@@@@@@@@@@@
                  @@@@@@@@@@@@@@@@@@@@@@
                     @@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@
                              @@

'''


class Valentine:
    def __init__(self, name):
        self.loved_one = name

    def romanticize(self):
        you_in_my_heart = __HEART__

        while '@' in you_in_my_heart:
            for letter in list(self.loved_one):
                you_in_my_heart = \
                    you_in_my_heart.replace('@', letter, 1)

        return you_in_my_heart

    def i_love_you(self):
        heart_lines = self.romanticize().split('\n')
        for line in heart_lines:
            print(f"{Fore.RED}{line}{Style.RESET_ALL}")
            time.sleep(0.3)  # Задержка между строками

        return f'I love you, {Fore.YELLOW}{self.loved_one}{Style.RESET_ALL}, you are the most valuable thing i have!'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def main():
    try:
        name = sys.argv[1]
    except IndexError:
        name = 'Liza' #ТУТ СЛОВО, ИЗ КОТОРОГО РИСУЕМ

    my_beloved = Valentine(name)
    print(my_beloved.i_love_you())

    time.sleep(15)

    pygame.mixer.music.stop()
    sys.exit()


if __name__ == '__main__':
    main()