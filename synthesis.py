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
import tkSimpleDialog
from Tkinter import *

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
            sound.play()

if __name__ == '__main__':
    pygame.init()

    a, b, c = None, None, None
    def _synthstart():
        d = MyDialog(Tk())
        a = Synth(*d.values())
        print 'running SYNTH'
        while _running:
            a.main()
        print 'finished SYNTH'

    def _keylistenerstart():
        b = KeyListener(a)
        'running KEYLISTENER'
        while _running:
            b.main()
        print 'finished KEYLISTENER'

    def _viewerstart():
        c = Viewer(a, 'samplelist.txt')
        print 'running VIEWER'
        while _running:
            c.main()
        print 'started VIEWER'

    def _exit():
        print 'running EXIT'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False
                    pygame.quit()
                    sys.exit()


    _display_surf = pygame.display.set_mode((1000,1000), pygame.HWSURFACE | pygame.DOUBLEBUF)
    global _running
    _running = True

    s = Thread(target=_synthstart, name="SYNTH")
    k = Thread(target=_keylistenerstart, name='KEYLISTENER')
    v = Thread(target=_viewerstart, name='VIEWER')
    exit = Thread(target=_exit, name='EXIT')

    exit.start()
    s.start()
    k.start()
    v.start()

    s.join()
    v.join()
    k.join()
    exit.join()
