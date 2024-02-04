import random
from constants import *


class cloud():
    def __init__(self, x, y, v, png):
        self.x = x
        self.y = y
        self.speed = v
        self.png = png

    def shift(self):  # сдвигает облако влево
        self.x -= self.speed

    def draw(self, win):  # отрисовывает облако на экране
        win.blit(self.png, (self.x, self.y))


# создает новые облака со случайной координатой и удаляет старые + отрисовка
def clouds_run(win, clouds, clouds_img, counter_cloud):
    res = False
    if counter_cloud > cld_border_shift:
        new_y = random.randrange(0, win_h, win_h / 10)
        while len(clouds) > 0 and (clouds[-1].y - cld_h / 2 < new_y) and (
                new_y < clouds[-1].y + cld_h / 2):
            new_y = random.randrange(0, win_h - cld_h, win_h / 2)

        clouds.append(cloud(win_w, new_y, cld_v, clouds_img[random.randint(0, 3)]))
        res = True

    for cl in clouds:
        if (cl.x + cld_w) > 0:
            cl.shift()
        else:
            del clouds[clouds.index(cl)]

    for cld in clouds:
        cld.draw(win)

    return res
