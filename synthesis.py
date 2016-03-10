import pygame
from pygame.mixer import *
from pygame.locals import *
import math
import numpy as np
from Queue import Queue
from threading import Thread
import time
from KeyListener import KeyListener
import sys

SUBDIVISIONS = 16

class Synth(object):

    """ Document here..."""
    def __init__(self, bpm=120, bars=8, click=True):
        self.bpm = bpm
        self.bars = bars
        self.click = click
        self.sleep_time = 60 / (4 * bpm)

        #TODO replace with class constant

        self.loop = [[] for sub in range(bars * SUBDIVISIONS)]
        self.loop = [self.loop[beat] + ['beep'] if beat % 4 == 0 else self.loop[beat] for beat in range(len(self.loop))]

        print self.loop

        self.playq = Queue()


    def frequencyMap(self, index):
        return 2**(index/12.0) * 440


    def main(self):
        self.count = 0
        while True:
            for e in self.loop[self.count]:
                self.playq.put(e)
                time.sleep(self.sleep_time)




class Viewer(object):
    def __init__(self, synth=None, filename='samplelist.txt', *size):
        if synth == None:
            synth = Synth()
        self.synth = synth

        pygame.mixer.init()

        f = open(filename)

        self.soundmap = {line.strip('\n')[:-4]:Sound(line.strip('\n')) for line in f.readlines()}
        #the number of channels specified here is NOT
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
        pygame.init()
        _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        _running = True

        m = Thread(target=self.main, name="AUDIOPLAYER", args=(self.synth,))
        m.start()
        exit = Thread(target=self.exit, name='EXIT')
        exit.start()

        exit.join()
        m.join()

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                break
        sys.exit()
        pygame.quit()

    def main(self, synth):
        for sound in synth.playq.get():
            sound.play()

if __name__ == '__main__':

    a, b, c = None, None, None
    def _synthstart():
        a = Synth()

    def _keylistenerstart():
        b = KeyListener(a)

    def _viewerstart():
        b = Viewer(a, 'samplelist.txt', 400, 400)

    s = Thread(target=_synthstart, name="SYNTH")
    s.start()
    k = Thread(target=_keylistenerstart, name='KEYLISTENER')
    k.start()
    v = Thread(target=_viewerstart, name='VIEWER')
    v.start()

    s.join()
    k.join()
    v.join()
