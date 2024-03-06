from constants import *
import random

list_of_lives = []
list_of_vpn = []
list_extra = []
coordinates = []
a = 1


class bonuses():

    """Класс, представляющий бонусы в игре.

        Атрибуты:
            x (int): Координата x бонуса на экране.
            y (int): Координата y бонуса на экране.
            rad (float): Радиус бонуса.
            v_x (int): Скорость перемещения бонуса по оси x.
            picture (pygame.Surface): Изображение бонуса.

        Методы:
            draw(win): Отображает бонус на экране по указанным координатам.
    """
    def __init__(self, x, y, v_x, rad, picture):
        self.x = x
        self.y = y
        self.rad = rad
        self.v_x = v_x
        self.picture = picture

    def draw(self, win):
        win.blit(self.picture, (self.x - bonus_w/2, self.y - bonus_w/2))


def bonus_generation(win, game_time, picture, picture_1, picture_extra):
    global list_of_lives, list_of_vpn, n_ext, n_vpn, a

    def generation():
        x1 = win_w
        y1 = random.randrange(0, win_h - bonus_w)
        v_x = -bonus_speed
        return x1, y1, v_x

    def generation_extra():
        x1 = random.randrange(200, win_w-200)
        y1 = 0
        v_y = bonus_speed
        return x1, y1, v_y

    for bonus in list_of_lives:
        if bonus.x < -bonus_w:
            del list_of_lives[list_of_lives.index(bonus)]
        else:
            bonus.x = bonus.x + bonus.v_x

    for bonus in list_of_vpn:
        if bonus.x < -bonus_w:
            del list_of_vpn[list_of_vpn.index(bonus)]
        else:
            bonus.x = bonus.x + bonus.v_x

    for bonus in list_extra:
        bonus.y = bonus.y + bonus.v_x

    if (len(list_of_lives) == 0) and (len(list_of_vpn) == 0) and (game_time > t_ext * n_ext):
        n_ext = n_ext + 1
        gen_x, gen_y, gen_v_x = generation()
        list_of_lives.append(bonuses(gen_x, gen_y, gen_v_x, bonus_w / 2, picture))

    if (len(list_of_vpn) == 0) and (len(list_of_lives) == 0) and (game_time > t_vpn * n_vpn):
        n_vpn = n_vpn + 1
        gen_x, gen_y, gen_v_x = generation()
        list_of_vpn.append(bonuses(gen_x, gen_y, gen_v_x, bonus_w / 2, picture_1))

    if (len(list_of_vpn) == 0) and (len(list_of_lives) == 0) and (game_time > 15) and a:
        n_vpn = n_vpn + 1
        gen_x, gen_y, gen_v_y = generation_extra()
        a -= 1
        list_extra.append(bonuses(gen_x, gen_y, gen_v_y, bonus_w / 1.5, picture_extra))

    for bonus in list_of_lives + list_of_vpn + list_extra:
        bonus.draw(win)
