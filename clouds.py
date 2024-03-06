import random
from constants import *


class cloud():
    def __init__(self, x, y, v, png):
        """
            Инициализирует объект облака.

            Параметры:
            - x: координата по оси X
            - y: координата по оси Y
            - v: скорость сдвига облака
            - png: изображение облака
        """
        self.x = x
        self.y = y
        self.speed = v
        self.png = png

    def shift(self):
        """Сдвигает облако влево."""
        self.x -= self.speed

    def draw(self, win):
        """Отрисовывает облако на экране."""
        win.blit(self.png, (self.x, self.y))


def clouds_run(win, clouds, clouds_img, counter_cloud):
    """
        Создает новые облака со случайной координатой и удаляет старые, а также отрисовывает их на экране.

        Параметры:
        - win: окно для отрисовки
        - clouds: список объектов облаков
        - clouds_img: список изображений облаков
        - counter_cloud: счетчик для создания новых облаков

        Возвращает:
        - res: флаг, указывающий были ли созданы новые облака
    """
    res = False
    if counter_cloud > cld_border_shift:
        # Генерация новых координат для облака
        new_y = random.randrange(0, win_h, win_h / 10)
        while len(clouds) > 0 and (clouds[-1].y - cld_h / 2 < new_y) and (
                new_y < clouds[-1].y + cld_h / 2):
            new_y = random.randrange(0, win_h - cld_h, win_h / 2)

        # Создание нового облака и добавление его в список
        clouds.append(cloud(win_w, new_y, cld_v, clouds_img[random.randint(0, 3)]))
        res = True

    # Сдвиг всех облаков влево
    for cl in clouds:
        if (cl.x + cld_w) > 0:
            cl.shift()
        else:
            del clouds[clouds.index(cl)]

    # Отрисовка всех облаков на экране
    for cld in clouds:
        cld.draw(win)

    return res
