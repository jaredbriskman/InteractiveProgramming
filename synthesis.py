import pygame
from pygame.locals import *
import math
import numpy as np
import Queue
import threading
import time
import string

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
        self.loop = [self.loop[beat] + ['click'] if beat % 4 == 0 else self.loop[beat] for beat in range(len(self.loop))]

        print self.loop

        playq = Queue.Queue()

        s = threading.Thread(target=self.main, )

    def frequencyMap(self, index):
        return 2**(index/12.0) * 440


    def main(self):
        self.count = 0
        while True:
            for e in self.loop[count]:
                playq.put(e)
                time.sleep(self.sleep_time)




class Viewer(object):
    def __init__(self, synth=None, filename='samplelist.txt'):
        if synth == None:
            synth = Synth()
        self.synth = synth

        f = open(filename)

        self.soundmap = {line.strip('\n')[:-4]:pygame.mixer.Sound(line.strip('\n')) for line in f.readlines()}
        #the number of channels specified here is NOT
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
        pygame.mixer.init()
        pygame.init()
        _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        _running = True

        m = threading.Thread(target=self.main, name="AUDIOPLAYER")
        m.start()
        m.join()

        exit = threading.Thread(target=self.exit, name='EXIT')
        exit.start()
        exit.join()

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                break
        pygame.quit()

    def main(self, synth):
        for sound in synth.playq.get():
            sound.play()

a = Synth()
b = Viewer(a)
