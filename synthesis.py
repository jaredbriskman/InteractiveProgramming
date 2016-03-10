import pygame
from pygame.mixer import *
from pygame.locals import *
import math
import numpy as np
from Queue import Queue
import threading
from threading import Thread
import time
from KeyListener import KeyListener
import sys
from Tkinter import Tk
import entrytest

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
        self.loop = [self.loop[beat] + ['Beep'] if beat % 4 == 0 else self.loop[beat] for beat in range(len(self.loop))]
        self.playq = Queue()

    def frequencyMap(self, index):
        return 2**(index/12.0) * 440


    def main(self):
        self.count = 0
        self.loop_process()
        time.sleep(self.sleep_time)

    def loop_process(self):
        self.count = self.count % (self.bars * SUBDIVISIONS)
        for e in self.loop[self.count]:
            self.playq.put(e)
        self.count += 1




class Viewer(object):
    def __init__(self, synth=None, filename='samplelist.txt'):
        if synth == None:
            synth = Synth()
        self.synth = synth

        pygame.mixer.init()

        f = open(filename)

        self.soundmap = {line.strip('\n')[:-4]:Sound('Samples/' + line.strip('\n')) for line in f.readlines()}
        #the number of channels specified here is NOT
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

    def main(self):
        for sound in self.synth.playq.get():
            if sound == 'exit':
                break
            self.soundmap[sound].play()

if __name__ == '__main__':
    pygame.init()
    _display_surf = pygame.display.set_mode((1000,1000), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _running = True


    d = entrytest.MyDialog(Tk())
    a = Synth(*d.values())
    b = KeyListener(a)
    c = Viewer(a, 'samplelist.txt')

    def _synthstart():
        print 'running SYNTH'
        global _running
        while _running:
            a.main()
        print 'finished SYNTH'

    def _keylistenerstart():
        'running KEYLISTENER'
        try:
            global _running
            while _running:
                b.main()
        except SystemExit:
            _running = False
            pygame.quit()
        print 'finished KEYLISTENER'

    def _viewerstart():
        print 'running VIEWER'
        global _running
        while _running:
            c.main()
        print 'finished VIEWER'

    # def _exit():
    #     print 'running EXIT'
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 _running = False
    #                 pygame.quit()
    #                 sys.exit()

    s = Thread(target=_synthstart, name="SYNTH")
    k = Thread(target=_keylistenerstart, name='KEYLISTENER')
    v = Thread(target=_viewerstart, name='VIEWER')
    # exit = Thread(target=_exit, name='EXIT')

    # exit.start()
    s.start()
    k.start()
    v.start()

    s.join()
    v.join()
    k.join()
    # exit.join()
