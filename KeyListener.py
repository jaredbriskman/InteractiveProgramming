"""A listener class that turns on and off keys in the Synthesis class"""
from pygame.key import *
import pygame
import time
import sys

#holds onto keys we're looking for
keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PLUS, pygame.K_MINUS,
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m,
    pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]

class KeyListener(object):
    """
    This class implements the Controller in our MVC. It uses a separate thread to
    loop through the event queue, looking for keyboard events and passing the
    corresponding sounds into the Model.
    """

    def __init__(self, synth=None, filename='samplelist.txt'):
        """This method initializes the KeyListener and reads in the sound sample
        names from a text file.
        """
        self.synth = synth
        f = open(filename)
        samplenames = f.readlines()
        self.soundmap = {keys[i]:samplenames[i][:-5] for i in range(len(keys))}

    def main(self):
        """This method loops through the pygame event queue checking for key
        presses or for a quit event. 
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.synth.loop[self.synth.count].append(self.soundmap.get(event.key, 'Zoom'))
                # print self.soundmap.get(event.key, 'Zoom')
            if event.type == pygame.QUIT:
                self.synth.playq.put('exit',)
                sys.exit()

if __name__ == '__main__':
    pygame.init()
    _display_surf = pygame.display.set_mode((300, 300), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _running = True
    k = KeyListener()
    while True:
        k.main()
        time.sleep(.01)
