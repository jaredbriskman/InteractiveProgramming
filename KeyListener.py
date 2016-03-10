"""A listener class that turns on and off keys in the Synthesis class"""
from pygame.key import *
import pygame
import time
import sys

#holds onto keys we're looking for
keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PLUS, pygame.K_MINUS]

class KeyListener(object):

    def __init__(self, synth=None, filename='samplelist.txt'):
        self.synth = synth
        f = open(filename)
        samplenames = f.readlines()
        self.soundmap = {keys[i]:samplenames[i][:-5] for i in range(len(keys))}

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.synth.loop[self.synth.count].append(self.soundmap.get(event.key, 'Zoom'))
                # print self.soundmap.get(event.key, 'Zoom')
            if event.type == pygame.QUIT:
                self.synth.playq.put('exit')
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    _display_surf = pygame.display.set_mode((300, 300), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _running = True
    k = KeyListener()
    while True:
        k.main()
        time.sleep(.01)
