import pygame
import sys

pygame.mixer.init()

bass1 = pygame.mixer.Sound('bass1.wav')
lead1 = pygame.mixer.Sound('lead1.wav')

bass1.play()

pygame.init()
_display_surf = pygame.display.set_mode((300, 300), pygame.HWSURFACE | pygame.DOUBLEBUF)
_running = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                bass1.play()
            if event.key == pygame.K_2:
                lead1.play()
