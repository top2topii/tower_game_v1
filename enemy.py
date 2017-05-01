# coding=utf-8

import pygame
import math


# 적이 이동하는 경로를 관리
class Waypoint(object):
    _x = 0  # initial value
    _y = 0
    _waypoint = ['4:S', '19:E', '6:S', '6:W', '4:N',
                 '14:W', '5:S', '10:E', '3:S', '10:W',
                 '5:S', '14:E', '4:N', '4:E', '5:S', '6:E']

    def __init__(self, block_size, init_x = 0, init_y = 0):
        self._block_size = block_size
        self._map_position = []
        self._xy_waypoint = []
        self._x = init_x
        self._y = init_y

        self.get_xy_waypoint()

    def calc_waypoint2xy(self, distance, direction):

        x = 0
        y = 0

        real_distance = (int(distance) - 1) * self._block_size

        if direction == 'S':
            y += real_distance
        elif direction == 'E':
            x += real_distance
        elif direction == 'N':
            y -= real_distance
        elif direction == 'W':
            x -= real_distance

        return x, y

    # _waypoint를 보고 좌표로 된 xy_waypoint를 구한다.
    # map_position을 구한다.
    def get_xy_waypoint(self):

        # initial value
        self._xy_waypoint.append((self._x, self._y))
        self._map_position.append(0)

        for i, w in enumerate(self._waypoint):
            (distance, direction) = w.split(':')
            print(distance, " ", direction)

            (a, b) = self.calc_waypoint2xy(distance, direction)

            # 이전 값을 가져오자.
            (prev_a, prev_b) = self._xy_waypoint[i]
            prev_position = self._map_position[i]

            self._xy_waypoint.append((a + prev_a, b + prev_b))

            self._map_position.append((int(distance) - 1) * self._block_size + prev_position)

        print(self._xy_waypoint)
        print(self._map_position)

    def _get_xy(self, v1, v0, position, i):

        # 이전 vector
        (prev_x, prev_y) = self._xy_waypoint[i]

        # a1 - a0
        x1, y1 = v1
        x0, y0 = v0

        len_vector = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))

        delta = position / len_vector

        new_x = (x1 - x0) * delta + prev_x
        new_y = (y1 - y0) * delta + prev_y

        return new_x, new_y

    def position_to_xy(self, position):

        for i, this_position in enumerate(self._map_position):
            if position == this_position:
                return self._xy_waypoint[i]
            elif position > this_position and position < self._map_position[i+1]:

                relative_pos = position - self._map_position[i]
                (new_x, new_y) = self._get_xy(self._xy_waypoint[i+1], self._xy_waypoint[i], relative_pos, i)
                # print(new_x, " ", new_y)
                return new_x, new_y

# 적을 생성하는 매니저
class EnemyManager(object):

    def __init__(self):
        pass


class Enemy(object):
    _x = 0      # initial value
    _y = 0
    _x_move = 0
    _y_move = 0
    _position = 0       # 현재 path중 몇번째 위치인지를 표시

    def __init__(self, screen, color, block_size, init_x = 0, init_y = 0):

        self._waypoint = Waypoint(block_size, init_x, init_y)

        self._screen = screen
        self._color = color
        self._speed = 0.0
        self._block_size = block_size
        self._map_position = []
        self._xy_waypoint = []
        self._x = init_x
        self._y = init_y

    def draw(self):
        self._position += 10
        (self._x_move, self._y_move) = self._waypoint.position_to_xy(self._position)

        pygame.draw.polygon(self._screen, self._color,
                             [[15 + self._x_move, 5 + self._y_move],
                              [5 + self._x_move, 24 + self._y_move],
                              [25 + self._x_move, 24 + self._y_move]], 1)