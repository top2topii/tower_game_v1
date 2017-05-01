# coding=utf-8

import pygame
import enemy

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BLOCK_SIZE = 32

display_width = 800
display_height = 600


def pygame_mainloop():
    pygame.init()

    myscreen = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('타워게임')

    isFinish = False
    isColorBlue = True

    x_delta = 10
    y_delta = 1

    clock = pygame.time.Clock()

    mymap = make_map()

    x_move = 0
    y_move = 0

    a_triangle = enemy.Enemy(myscreen, RED, BLOCK_SIZE, 42, 1)

    while not isFinish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isFinish = True

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     isColorBlue = not isColorBlue
        #
        # pressed = pygame.key.get_pressed()
        #
        # if pressed[pygame.K_UP]: y -= 3
        # if pressed[pygame.K_DOWN]: y += 3
        # if pressed[pygame.K_LEFT]: x -= 3
        # if pressed[pygame.K_RIGHT]: x += 3

        myscreen.fill((0, 0, 0))

        # if isColorBlue: color = (0, 128, 255)
        # else: color = (0, 128, 255)

        #

        a_triangle.draw()

        pygame.draw.polygon(myscreen, GREEN, [[15 + x_move, 5 + y_move], [5 + x_move, 24 + y_move], [25 + x_move, 24 + y_move]], 1)

        x_move += 0
        y_move += 0.7

        if x_move > display_width + BLOCK_SIZE:
            x_move = 0

        if y_move > display_height + BLOCK_SIZE:
            y_move = 0

        for x in range(0, 22):
            for y in range(0, 18):
                visible_flag = get_map_xy(mymap , x, y)

                if visible_flag == '1':
                    pygame.draw.rect(myscreen, BLUE, pygame.Rect(x * BLOCK_SIZE + x_delta, y * BLOCK_SIZE + y_delta, BLOCK_SIZE, BLOCK_SIZE), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def make_map():
    map = ["1001111111111111111111",    # 1
           "1001111111111111111111",    # 2
           "1000000000000000000001",    # 3
           "1000000000000000000001",    # 4
           "1111111111111111111001",    # 5
           "1000000000000001111001",    # 6
           "1000000000000001111001",    # 7
           "1001111111111001111001",    # 8
           "1000000000001000000001",    # 9
           "1000000000001000000001",    # 10
           "1111111111001111111111",    # 11
           "1000000000001000000111",    # 12
           "1000000000001000000111",    # 13
           "1001111111111001100111",    # 14
           "1000000000000001100111",    # 15
           "1000000000000001100000",    # 16
           "1111111111111111100000",    # 17
           "1111111111111111111111"]    # 18

    return map

# x, y의 격자를 그릴 지 말 지를 결정한다.
# return value: 1: 그린다, 0: 안 그린다.
def get_map_xy(map, x, y):
    line_str = map[y]

    return line_str[x]

# 격자를 테스트 해 보자.
def test():
    mymap = make_map()

    value = get_map_xy(mymap, 1, 0)
    print(value)

if __name__ == "__main__":
    pygame_mainloop()