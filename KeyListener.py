"""A listener class that turns on and off keys in the Synthesis class"""
from pygame.key import *
import pygame
import time

#holds onto keys we're looking for
keys = {pygame.K_0:0, pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4, pygame.K_5:5, pygame.K_6:6, pygame.K_7:7, pygame.K_8:8, pygame.K_9:9, pygame.K_PLUS:10, pygame.K_MINUS:11}

class KeyListener(object):

    # def __init__(self, synth):
    #     self.synth = synth
    #     main()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print(keys.get(event.key, NotImplemented))
                    # synth.on.append(keys.get(event.key, 0))
            # print self.synth.on

if __name__ == '__main__':
    pygame.init()
    _display_surf = pygame.display.set_mode((300, 300), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _running = True
    k = KeyListener()
    k.main()
