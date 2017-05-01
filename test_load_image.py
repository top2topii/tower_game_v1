# coding=utf-8

import pygame

pygame.init()

display_width = 800
display_height = 600

myscreen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('타워게임')

myImage = pygame.image.load('pygame_tiny.png')


def myImg(x, y):
    myscreen.blit(myImage, (x, y))

x = (display_width * 0.5)
y = (display_height * 0.5)

isFinish = False

clock = pygame.time.Clock()

while not isFinish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isFinish = True

    myscreen.fill((0, 0, 0))

    myImg(x, y)

    pygame.display.flip()
    clock.tick(60)
