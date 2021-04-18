import pygame
import time

mainSurface = pygame.display.set_mode((300, 300))
ball = pygame.Rect(0,0,10,10)
time.sleep(1)
while True:
    mainSurface.fill((0,0,0))
    pygame.draw.circle(pygame.display,(255,255,255),ball.center,5)
    ball.move_ip(1,1)
    pygame.display.update()