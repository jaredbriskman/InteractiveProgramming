import pygame
from pygame.locals import *
import math
import numpy as np

#TODO: actually implement this class

class Synth(object):
    """ Document here..."""
    def __init__(self, on = None, duration = 0.1, loops = 0):
        if on == None:
            on = []
        self.on = on
        self.duration = duration
        self.loops = loops

    def frequencyMap(self, index):
        return 2**(index/12.0) * 440

class Viewer(object, synth = None):
    def __init__(self, *size):
        if synth = None
            synth = Synth()
        self.BITS = 16
        self.synth = synth
        #the number of channels specified here is NOT
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
        pygame.mixer.pre_init(44100, -self.BITS, 2)
        pygame.init()
        _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        _running = True
        main(self.synth)

    def main(self, synth):
        duration = synth.duration # in seconds
        frequency = synth.frequencyMap(synth.on.pop())
        #freqency for the left speaker
        frequency_l = frequency
        #frequency for the right speaker
        frequency_r = frequency
        sample_rate = 44100
        n_samples = int(round(duration*sample_rate))

        #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
        buf = np.zeros((n_samples, 2), dtype = np.int16)
        max_sample = 2**(self.BITS - 1) - 1

        for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds

        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
        buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

        sound = pygame.sndarray.make_sound(buf)
        #play once, then loop forever
        sound.play(self.loops)


        #This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
        while _running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False
            break
            pygame.quit()

a = synth([1, 2, 3, 4, 5, 6, 7, 8], 1, 0])
b = Viewer(a)
