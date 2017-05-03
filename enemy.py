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
    _len_vector = []
    _map_position = []
    _xy_waypoint = []

    _block_size = 0
    _path_id =''

    def __init__(self, path_id, block_size, init_x = 0, init_y = 0):
        Waypoint._path_id = path_id
        Waypoint._block_size = block_size
        Waypoint._x = init_x
        Waypoint._y = init_y

        Waypoint.get_xy_waypoint()
        Waypoint.get_len_vector()

    @classmethod
    def make(cls, path_id, block_size, init_x = 0, init_y = 0):

        return Waypoint(path_id, block_size, init_x, init_y)

    @classmethod
    def calc_waypoint2xy(cls, distance, direction):

        x = 0
        y = 0

        real_distance = (int(distance) - 1) * cls._block_size

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
    # map_position을 구한다. position을 보고 현재 어느 구간에 있는지 알아보기 위한 map table이다.
    @classmethod
    def get_xy_waypoint(cls):

        if len(cls._xy_waypoint) > 0:
            return

        # initial value
        cls._xy_waypoint.append((cls._x, cls._y))
        cls._map_position.append(0)

        for i, w in enumerate(cls._waypoint):
            (distance, direction) = w.split(':')
            print(distance, " ", direction)

            (a, b) = cls.calc_waypoint2xy(distance, direction)

            # 이전 값을 가져오자.
            (prev_a, prev_b) = cls._xy_waypoint[i]
            prev_position = cls._map_position[i]

            cls._xy_waypoint.append((a + prev_a, b + prev_b))

            cls._map_position.append((int(distance) - 1) * cls._block_size + prev_position)

        print(cls._xy_waypoint)
        print(cls._map_position)


    # _len_vector를 미리 구해 놓는다.
    @classmethod
    def get_len_vector(cls):
            # init value

        if len(cls._len_vector) > 0:
            return

        for i, v in enumerate(cls._xy_waypoint):

            if i == 0:
                #self._len_vector.append(0.0)
                continue

            v0 = cls._xy_waypoint[i-1]
            v1 = cls._xy_waypoint[i]

            # v1 - v0
            x1, y1 = v1
            x0, y0 = v0

            len_vector = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
            cls._len_vector.append(len_vector)

        print(cls._len_vector)

    @classmethod
    def _get_xy(cls, v1, v0, position, i):

        # 이전 vector
        (prev_x, prev_y) = cls._xy_waypoint[i]

        # a1 - a0
        x1, y1 = v1
        x0, y0 = v0

        #len_vector = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))

        len_vector = cls._len_vector[i]

        delta = position / len_vector

        new_x = (x1 - x0) * delta + prev_x
        new_y = (y1 - y0) * delta + prev_y

        return new_x, new_y

    @classmethod
    def position_to_xy(cls, position):

        for i, this_position in enumerate(cls._map_position):
            if position == this_position:
                return cls._xy_waypoint[i]
            elif position > this_position and position < cls._map_position[i+1]:

                relative_pos = position - cls._map_position[i]
                (new_x, new_y) = Waypoint._get_xy(cls._xy_waypoint[i+1], cls._xy_waypoint[i], relative_pos, i)
                # print(new_x, " ", new_y)
                return new_x, new_y

# 적을 생성하는 매니저
class EnemyManager(object):
    _screen = None
    _block_size = None
    _enemy_list = []

    def __init__(self, screen, block_size):
        self._screen = screen
        self._block_size = block_size

    def add_enemy(self, color, start_position, init_x=0, init_y=0):
        self._enemy_list.append(Enemy(self._screen, color, self._block_size, start_position, init_x, init_y))

    def draw(self, count):

        for a_enemy in self._enemy_list:
            a_enemy.draw(count)



class Enemy(object):
    _x = 0      # initial value
    _y = 0
    _x_move = 0
    _y_move = 0
    _position = 0       # 현재 path중 몇번째 위치인지를 표시
    _start_position = None

    def __init__(self, screen, color, block_size, start_position, init_x=0, init_y=0,):

        self._waypoint = Waypoint.make("path1", block_size, init_x, init_y)

        self._screen = screen
        self._color = color
        self._speed = 0.0
        self._block_size = block_size
        self._map_position = []
        self._xy_waypoint = []
        self._start_position = start_position
        self._x = init_x
        self._y = init_y

    def draw(self, count):

        if count > self._start_position:
            self._position += 1

            (self._x_move, self._y_move) = Waypoint.position_to_xy(self._position)

            #
            # TODO: 목적지에 도달하면 enemy를 삭제하자.
            #

            pygame.draw.polygon(self._screen, self._color,
                                 [[15 + self._x_move, 5 + self._y_move],
                                  [5 + self._x_move, 24 + self._y_move],
                                  [25 + self._x_move, 24 + self._y_move]], 1)