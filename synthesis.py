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

SUBDIVISIONS = 8

class Synth(object):
    """This class holds onto the state of our synthesizer. It is the M in our MVC.
    This class has a list of "16th notes", which are lists of sounds to be played.
    As it loops through the list, it adds any key presses to the list and places
    any sounds already in the list onto the playing queue.

    attributes: bpm, bars, click, sleep_time
    """

    def __init__(self, bpm=120, bars=8, click=True):
        """This method initializes the synthesizer's bpm, the length of the loop,
        its sleep time, and sets up the empty sample loop.
        """
        self.bpm = bpm
        self.bars = bars
        self.click = click
        self.sleep_time = 60/ (4.0 * bpm)
        self.count = 0

        self.loop = [[] for sub in range(bars * SUBDIVISIONS)]
        self.loop = [self.loop[beat] + ['Beep'] if beat % 4 == 0 and click else self.loop[beat] for beat in range(len(self.loop))]
        self.playq = Queue()

    # def frequencyMap(self, index):
    #     return 2**(index/12.0) * 440


    def main(self):
        """This method keeps track of our position in the sample loop and puts
        any samples it finds in the current subdivision into the sound playing
        queue.
        """
        for e in self.loop[self.count]:
            # Note that queues will take tuples, but will break up strings.
            self.playq.put((e,))
        self.count += 1
        self.count = self.count % (self.bars * SUBDIVISIONS)
        time.sleep(self.sleep_time)




class Viewer(object):
    """This class is the View part of our MVC model. It runs in its own separate
    thread, waiting for sounds to appear in its queue. It then maps those sounds
    to pygame Sound objects and plays them.
    """
    def __init__(self, synth=None, filename='samplelist.txt'):
        """This method handles initializing this class's synth, and also prepares
        the name-sound mapping for playing sounds.
        """
        if synth == None:
            synth = Synth()
        self.synth = synth

        pygame.mixer.init()

        f = open(filename)

        #preparing the sound map
        self.soundmap = {line.strip('\n')[:-4]:Sound('Samples/' + line.strip('\n')) for line in f.readlines()}
        print self.soundmap

    def main(self):
        """This method interprets the play queue, and plays sounds unless it
        receives a special exit tag.
        """
        for sound in self.synth.playq.get():
            if sound == ('exit'):
                break
            self.soundmap[sound].play()

if __name__ == '__main__':
    """This main function is where a lot of learning happened. We went through
    many iterations to get the threading to work properly. First, everything is
    initialized, and then three threads are started, one on each of the classes'
    main methods. Conditionals in these loops serve to clean up when the
    controller receives an exit event.
    """

    #pygame initialization
    pygame.init()
    _display_surf = pygame.display.set_mode((46,45), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _running = True
    img = pygame.image.load('speaker.bmp')
    screen.blit(img, pygame.Surface.getRect(img))

    #synthesizer initialization
    d = entrytest.MyDialog(Tk())
    a = Synth(*d.values())
    b = KeyListener(a)
    c = Viewer(a, 'samplelist.txt')

    #thread target functions
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
