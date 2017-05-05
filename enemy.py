# coding=utf-8

import pygame
import math


# 적이 이동하는 경로를 관리
class Waypoint(object):

    _waypoint = {0: ['4:S', '19:E', '6:S', '6:W', '4:N',
                 '14:W', '5:S', '10:E', '3:S', '10:W',
                 '5:S', '14:E', '4:N', '4:E', '5:S', '6:E'],
                 1: ['3:S', '19:E', '8:S', '8:W', '4:N',
                  '12:W', '3:S', '10:E', '5:S', '10:W',
                  '3:S', '12:E', '4:N', '6:E', '5:S', '5:E']
                 }





    def __init__(self, block_size, init_x=0, init_y=0, waypoint_id=0):


        self._x = init_x
        self._y = init_y
        self._len_vector = []
        self._map_position = []
        self._xy_waypoint = []
        self._block_size = block_size
        self._waypoint_id = waypoint_id

        # 0, 1만 만들 수 있다.
        if not waypoint_id in self._waypoint:
            raise NotImplementedError

        self.get_xy_waypoint()
        self.get_len_vector()

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
    # map_position을 구한다. position을 보고 현재 어느 구간에 있는지 알아보기 위한 map table이다.

    def get_xy_waypoint(self):

        if len(self._xy_waypoint) > 0:
            return

        # initial value

        target_waypoint = Waypoint._waypoint[self._waypoint_id]
        target_xy_waypoint = self._xy_waypoint
        target_map_position = self._map_position
        target_xy_waypoint.append((self._x, self._y))
        target_map_position.append(0)

        for i, w in enumerate(target_waypoint):
            (distance, direction) = w.split(':')
            print(distance, " ", direction)

            (a, b) = self.calc_waypoint2xy(distance, direction)

            # 이전 값을 가져오자.
            (prev_a, prev_b) = target_xy_waypoint[i]
            prev_position = target_map_position[i]

            target_xy_waypoint.append((a + prev_a, b + prev_b))

            target_map_position.append((int(distance) - 1) * self._block_size + prev_position)

        print(target_xy_waypoint)
        print(target_map_position)


    # _len_vector를 미리 구해 놓는다.
    def get_len_vector(self):
            # init value

        if len(self._len_vector) > 0:
            return

        target_xy_waypoint = self._xy_waypoint
        target_len_vector = self._len_vector

        for i, v in enumerate(target_xy_waypoint):

            if i == 0:
                continue

            v0 = target_xy_waypoint[i-1]
            v1 = target_xy_waypoint[i]

            # v1 - v0
            x1, y1 = v1
            x0, y0 = v0

            len_vector = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
            target_len_vector.append(len_vector)

        print(target_len_vector)

    def _get_xy(self, v1, v0, position, i):

        target_xy_waypoint = self._xy_waypoint
        target_len_vector = self._len_vector

        # 이전 vector
        (prev_x, prev_y) = target_xy_waypoint[i]

        # a1 - a0
        x1, y1 = v1
        x0, y0 = v0

        #len_vector = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))

        len_vector = target_len_vector[i]

        delta = position / len_vector

        new_x = (x1 - x0) * delta + prev_x
        new_y = (y1 - y0) * delta + prev_y

        return new_x, new_y

    def position_to_xy(self, position):

        target_xy_waypoint = self._xy_waypoint
        target_map_position = self._map_position

        for i, this_position in enumerate(target_map_position):
            if position == this_position:
                return target_xy_waypoint[i]
            elif position > this_position and position < target_map_position[i+1]:

                relative_pos = position - target_map_position[i]
                (new_x, new_y) = self._get_xy(target_xy_waypoint[i+1], target_xy_waypoint[i], relative_pos, i)
                # print(new_x, " ", new_y)
                return new_x, new_y

# 적을 생성하는 매니저
class EnemyManager(object):
    _screen = None
    _block_size = None
    _enemy_list = []
    _waypoint_dic = {}

    def __init__(self, screen, block_size):
        self._screen = screen
        self._block_size = block_size

    def add_enemy(self, color, start_position, init_x=0, init_y=0, waypoint_id=0):

        # Waypoint 객체가 없으면 생성해서 등록한다.
        if not waypoint_id in self._waypoint_dic:
            self._waypoint_dic[waypoint_id] = Waypoint(self._block_size, init_x, init_y, waypoint_id)

        self._enemy_list.append(Enemy(self._screen, color, self._block_size, start_position, self._waypoint_dic[waypoint_id], init_x, init_y))

    def draw(self, count):

        for a_enemy in self._enemy_list:
            a_enemy.draw(count)



class Enemy(object):
    # _x = 0      # initial value
    # _y = 0
    # _x_move = 0
    # _y_move = 0
    # _position = 0       # 현재 path중 몇번째 위치인지를 표시
    # _start_position = None

    def __init__(self, screen, color, block_size, start_position, waypoint_obj, init_x=0, init_y=0):

        self._waypoint = waypoint_obj

        self._screen = screen
        self._color = color
        self._speed = 0.0
        self._block_size = block_size

        self._start_position = start_position
        self._x = init_x
        self._y = init_y
        self._x_move = 0
        self._y_move = 0
        self._position = 0

    def draw(self, count):

        if count > self._start_position:
            self._position += 1

            (self._x_move, self._y_move) = self._waypoint.position_to_xy(self._position)

            #
            # TODO: 목적지에 도달하면 enemy를 삭제하자.
            #

            pygame.draw.polygon(self._screen, self._color,
                                 [[15 + self._x_move, 5 + self._y_move],
                                  [5 + self._x_move, 24 + self._y_move],
                                  [25 + self._x_move, 24 + self._y_move]], 1)