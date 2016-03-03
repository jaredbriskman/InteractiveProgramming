"""A listener class that turns on and off keys in the Synthesis class"""
from pygame.key import *
import time

#holds onto keys we're looking for
keys = ['K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', "K_6", "K_7", "K_8", "K_9", "K_PLUS", "K_MINUS"]

class KeyListener(object):

    def __init__(self, synth):
        self.synth = synth
        main()

    def main():
        while True:
            pressed = get_pressed()
            output = []
            i = 0
            for k in keys:
                if pressed[k] == True:
                    output.append[i]
                i += 1
            synth.on = output
            time.sleep(.01)
