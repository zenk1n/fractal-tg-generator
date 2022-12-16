import random

import pygame
import threading
import time

class Base(object):

    def __init__(self, size, callRun, title=""):
        self.__run = callRun
        self.title = title
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.screen.fill([255, 255, 255])
        self.scalaRate = 4

    def save(self, title):
        pygame.image.save(self.screen, title)

    def wait(self):
        name = 0
        self.__run
        # th = threading.Thread(target=self.__run)
        # th.start()

        condition = True
        while condition:
            for event in pygame.event.get():
                # if not th.is_alive():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.save(f"{name}.png")
                            name = name + 1
                            beg = -15*name
                            end = 15*name
                            i = self.screen.get_width()/2-random.randint(beg, end)
                            j = self.screen.get_height()/2.5-random.randint(beg, end)
                            w = self.screen.get_width() // (2 * self.scalaRate)
                            h = self.screen.get_height() // (2 * self.scalaRate)
                            pygame.display.flip()
                            self.scala(i, j, self.scalaRate)
                            self.__run()
                            # th.start()
            mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (245, 221), 'button': 1})
            pygame.event.post(mouse_event)
            if (name == 6):
                condition = False
                pygame.quit()
            # if (name == 6):
            #     # exit()
            #     print("cool")




