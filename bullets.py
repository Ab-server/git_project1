from constants import *
import random
import time

bullet_array = []
speed_counter = 0  # коэф. изменения скорости пули
bullet_speed = bullet_speed_init


class bullet():
    def __init__(self, x, y, v_x, v_y, rad, picture):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.rad = rad
        self.picture = picture

    def draw(self, win):
        win.blit(self.picture, (self.x - bull_w / 2, self.y - bull_w / 2))


def bullet_generator(win, x, y, bullet_picture):
    """Изменение поизции пуль и генератор новых"""
    global bullet_array
    global speed_counter
    global bullet_speed
    edge = bull_w / 2

    for shot in bullet_array:
        if (shot.x < -edge) or (shot.x > win_w + edge) or (shot.y < -edge):
            del bullet_array[bullet_array.index(shot)]
        else:
            shot.x = shot.x + shot.v_x
            shot.y = shot.y + shot.v_y


    # if speed_counter < speed_counter_lim:
    #     bullet_speed = bullet_speed_init + bullet_speed_add * (speed_counter // 500)
    #     if speed_counter == speed_counter_lim - 1:
    #         bullet_speed = bullet_speed_init + bullet_speed_add * 11


    if len(bullet_array) == 0:
        new_born_x = random.randrange(0, win_w, 5)
        new_born_y = win_h + bull_w / 2
        new_born_v_x = bullet_speed * (x - new_born_x) / (
                    (x - new_born_x) ** 2 + (y - new_born_y) ** 2) ** 0.5
        new_born_v_y = bullet_speed * (y - new_born_y) / (
                    (x - new_born_x) ** 2 + (y - new_born_y) ** 2) ** 0.5
        bullet_array.append(
            bullet(new_born_x, new_born_y, new_born_v_x, new_born_v_y, bull_w / 2, bullet_picture))
    else:
        if bullet_array[-1].y <= win_h - 3 * bull_w:
            new_born_x = random.randrange(0, win_w, 5)
            new_born_y = win_h + bull_w / 2
            new_born_v_x = bullet_speed * (x - new_born_x) / (
                        (x - new_born_x) ** 2 + (y - new_born_y) ** 2) ** 0.5
            new_born_v_y = bullet_speed * (y - new_born_y) / (
                        (x - new_born_x) ** 2 + (y - new_born_y) ** 2) ** 0.5
            bullet_array.append(
                bullet(new_born_x, new_born_y, new_born_v_x, new_born_v_y, bull_w / 2,
                       bullet_picture))

    for shot in bullet_array:
        shot.draw(win)

    # while True:
    #     bullet_speed *= 1.4
    #     time.sleep(5)

def distance(x_p, y_p, x_l, y_l, c_l):
    """Расстояние между точкой и линией """
    return abs(x_l * x_p + y_l * y_p + c_l) / (x_l ** 2 + y_l ** 2) ** 0.5


def straight(first_point, second_point):
    if first_point[0] == second_point[0]:
        return [1, 0, -first_point[0]]
    elif first_point[1] == second_point[1]:
        return [0, 1, -first_point[1]]
    else:
        return [second_point[1] - first_point[1], first_point[0] - second_point[0], first_point[1] *
                (second_point[0] - first_point[0]) - first_point[0] * (
                            second_point[1] - first_point[1])]


def projection(x_p, y_p, alfa):
    """Координаты точки"""
    if alfa[0] == 0:
        return [x_p, - alfa[2] / alfa[1]]
    elif alfa[1] == 0:
        return [- alfa[2] / alfa[0], y_p]
    else:
        x0 = (alfa[1] * x_p / alfa[0] - alfa[2] / alfa[1] - y_p) / (
                    alfa[1] / alfa[0] + alfa[0] / alfa[1])
        return [x0, - alfa[0] * x0 / alfa[1] - alfa[2] / alfa[1]]


def one_crossing(first_point, second_point, x_p, y_p, r):
    st = straight(first_point, second_point)
    if ((x_p - first_point[0]) ** 2 + (y_p - first_point[1]) ** 2) ** 0.5 <= r:
        return True
    if ((x_p - second_point[0]) ** 2 + (y_p - second_point[1]) ** 2) ** 0.5 <= r:
        return True
    p = projection(x_p, y_p, straight(first_point, second_point))
    if p[0] <= max(first_point[0], second_point[0]) and p[0] >= min(first_point[0],
                                                                    second_point[0]) and p[
        1] <= max(first_point[1], second_point[1]) and \
            p[1] >= min(first_point[1], second_point[1]) \
            and distance(x_p, y_p, st[0], st[1], st[2]) <= r:
        return True
    return False


def crossing(polygon_vertexes, x_p, y_p, r):
    for i in range(len(polygon_vertexes)):
        if one_crossing(polygon_vertexes[i - 1], polygon_vertexes[i], x_p, y_p, r):
            return True
    return False
