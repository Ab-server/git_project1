"""
Импорт необходимых библиотек и модулей.
"""
import pygame
from constants import *  # Импорт констант из файла constants.py
import painting as pnt  # Импорт функций для отрисовки из модуля painting.py
import clouds as cl  # Импорт функций для работы с облаками из модуля clouds.py
import lives as liv  # Импорт функций для работы с жизнями из модуля lives.py
import bullets as bul  # Импорт функций для работы с пулями из модуля bullets.py
import bonuses as bon  # Импорт функций для работы с бонусами из модуля bonuses.py


"""
Инициализация Pygame и создание окна игры.
"""

pygame.init()
win = pygame.display.set_mode((win_w, win_h))  # Создание окна с заданными размерами
pygame.display.set_caption("FLYDODGE")  # Установка заголовка окна
clock = pygame.time.Clock()  # Создание объекта Clock для управления временем в игре

"""
Загрузка шрифтов и изображений для игры.
"""

f = 'Agitpropc.otf'
font_huge = pygame.font.Font(f, int(62 * scaling))  # Определение крупного шрифта
font_normal = pygame.font.Font(f, int(38 * scaling))  # Определение обычного шрифта
font_ns = pygame.font.Font(f, int(30 * scaling))  # Определение шрифта меньшего размера
font_small = pygame.font.Font(f, int(26 * scaling))  # Определение шрифта маленького размера

logo = pygame.image.load("img/logo_tr.png").convert_alpha()  # Загрузка логотипа игры
logo = pygame.transform.smoothscale(logo, (int(192 * scaling), int(192 * scaling)))  # Изменение размера логотипа

plane = pygame.image.load("img/plane.png").convert_alpha()  # Загрузка изображения самолета
plane = pygame.transform.smoothscale(plane, (int(pl_w * scaling), int(pl_h * scaling)))  # Изменение размера самолета

plane_dmg = pygame.image.load("img/plane_dmg.png").convert_alpha()  # Загрузка изображения поврежденного самолета
plane_dmg = pygame.transform.smoothscale(plane_dmg, (int(pl_w * scaling), int(pl_h * scaling)))  # Изменение размера

rkn = pygame.image.load("img/circle.png").convert_alpha()  # Загрузка изображения пули
rkn = pygame.transform.smoothscale(rkn, (int(bull_w * scaling), int(bull_w * scaling)))  # Изменение размера пули

vpn = pygame.image.load("img/Щит.png").convert_alpha()  # Загрузка изображения бонуса "щит"
vpn = pygame.transform.smoothscale(vpn, (int(bonus_w * scaling), int(bonus_w * scaling)))  # Изменение размера

vpn_extra = pygame.transform.smoothscale(vpn, (int(bonus_w * 1.5), int(bonus_w * 1.5)))  # Изменение размера для доп. "щита"

extr_l = pygame.image.load("img/life.png").convert_alpha()  # Загрузка изображения бонуса "жизнь"
extr_l = pygame.transform.smoothscale(extr_l, (int(bonus_w * scaling), int(bonus_w * scaling)))  # Изменение размера

cloud_0 = pygame.image.load("img/cloud0.png").convert_alpha()  # Загрузка изображений облаков
cloud_1 = pygame.image.load("img/cloud1.png").convert_alpha()
cloud_2 = pygame.image.load("img/cloud2.png").convert_alpha()
cloud_3 = pygame.image.load("img/cloud3.png").convert_alpha()
cloud0 = pygame.transform.smoothscale(cloud_0, (cld_w, cld_h))  # Изменение размеров облаков
cloud1 = pygame.transform.smoothscale(cloud_1, (cld_w, cld_h))
cloud2 = pygame.transform.smoothscale(cloud_2, (cld_w, cld_h))
cloud3 = pygame.transform.smoothscale(cloud_3, (cld_w, cld_h))
clouds_img = [cloud0, cloud1, cloud2, cloud3]  # Список изображений облаков
clouds = []  # Список для хранения облаков

pl_spdx0 = spd  # Изначальная скорость самолета по оси x
pl_spdy0 = 0  # Изначальная скорость самолета по оси y
pl_spdx = pl_spdx0  # Текущая скорость самолета по оси x
pl_spdy = pl_spdy0  # Текущая скорость самолета по оси y

level = 1  # Текущий уровень игры

pl_lives0 = 3  # Изначальное количество жизней
pl_lives = pl_lives0  # Текущее количество жизней

pl_x = midle_x  # Начальная координата x самолета
pl_y = midle_y  # Начальная координата y самолета

vulnerable = True  # Переменная, определяющая уязвимость самолета

best_result = open('best_result.txt', 'r+')  # Открытие файла с лучшим результатом
game_time = 0  # Изначальное время игры
best_time = float(best_result.readline())  # Получение лучшего времени из файла

counter_cloud = cld_border_shift  # Счетчик для генерации облаков

crashed = False  # Переменная, определяющая состояние игры (закрыта или нет)
menu = True  # Переменная, определяющая, находится ли игра в меню
game_over = False  # Переменная, определяющая, закончена ли игра
game = False  # Переменная, определяющая, идет ли игра
pause = False  # Переменная, определяющая, находится ли игра на паузе

# Загрузка звуковых файлов
hit = pygame.mixer.Sound('sound/telerun_hit.ogg')
bonus_life = pygame.mixer.Sound('sound/telerun_bonus_life.ogg')
music = pygame.mixer.music.load('sound/telerun_theme.ogg')
up = pygame.mixer.Sound('sound/telerun_up.ogg')
click = pygame.mixer.Sound('sound/telerun_click.ogg')
pygame.mixer.music.play(-1)  # Запуск музыки в цикле
pygame.mixer.music.set_volume(0.03)  # Установка громкости музыки


def fall(dt, y, spdy, ay):

    """
    Функция для свободного падения объекта.
    Принимает текущее время dt, текущую координату y, текущую скорость по оси y spdy и ускорение по оси y ay.
    Возвращает новую координату объекта и его новую скорость по оси y после применения законов движения.
    """

    y += spdy * dt + ay * dt ** 2 / 2
    spdy += ay * dt
    return y, spdy

spawn_timer = pygame.time.get_ticks()  # Таймер для отслеживания времени создания объектов

"""
Основной игровой цикл.
"""

while not crashed:
    win.fill((255, 255, 255))  # Заполнение экрана белым цветом
    if cl.clouds_run(win, clouds, clouds_img, counter_cloud):  # Запуск анимации облаков
        counter_cloud = 0
    else:
        counter_cloud += 1

    if menu:  # Отображение меню
        pygame.time.delay(delay)  # Задержка
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_channel = click.play()
                click_channel.set_volume(0.5)
                crashed = True

        pnt.draw_menu(win, font_small, font_normal, font_ns, font_huge, logo, best_time)  # Отрисовка меню
        pygame.display.update()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:  # Обработка нажатия клавиши Enter
            click_channel = click.play()
            click_channel.set_volume(0.05)
            pl_x, pl_y, = pl_x0, pl_y0
            pl_spdx, pl_spdy = pl_spdx0, pl_spdy0
            pl_lives = pl_lives0
            menu = False
            game = True
            game_time = 0
            bon.n_vpn = 1
            bon.n_ext = 1
            clock.tick()
            spawn_timer = pygame.time.get_ticks()

    if game:  # Игровой процесс
        if pl_lives > 0:  # Проверка количества жизней
            clock.tick()  # Установка FPS
            if pygame.time.get_ticks() - spawn_timer >= 10000:  # Увеличение уровня сложности
                bul.bullet_speed *= 1.2
                level += 1
                spawn_timer = pygame.time.get_ticks()
            pygame.time.delay(delay)  # Задержка для стабилизации процессорного времени

            for event in pygame.event.get():  # Обработка событий
                if event.type == pygame.QUIT:
                    crashed = True
                    click_channel = click.play()
                    click_channel.set_volume(0.1)

            keys = pygame.key.get_pressed()  # Получение нажатых клавиш

            if keys[pygame.K_SPACE]:  # Пауза по нажатию клавиши Space
                pause = True
                click_channel = click.play()
                click_channel.set_volume(0.1)

            if keys[pygame.K_RIGHT] and (win_w - pl_x >= pl_w + brd):  # Движение вправо
                pl_x += pl_spdx * t

            if keys[pygame.K_LEFT] and (pl_x >= brd):  # Движение влево
                pl_x -= pl_spdx * t

            # Обработка движения вверх/вниз
            if (not keys[pygame.K_DOWN] and not keys[pygame.K_UP]) or (keys[pygame.K_DOWN] and keys[pygame.K_UP]):
                pl_y, pl_spdy = fall(t, pl_y, pl_spdy, pl_g)
            else:
                if keys[pygame.K_UP] and (pl_y > brd):  # Движение вверх
                    pl_y, pl_spdy = fall(t, pl_y, spd_up, pl_g)
                if pl_y < brd:
                    pl_spdy = 0
                if keys[pygame.K_DOWN]:  # Движение вниз
                    pl_y, pl_spdy = fall(t, pl_y, pl_spdy, a_down)
            if pl_y <= brd:
                pl_y = brd

            if pl_y >= win_h - brd:  # Звуковое оповещение при достижении нижней границы экрана
                up_channel = up.play()
                up_channel.set_volume(0.1)

            # Отрисовка самолета и других элементов
            polygon = [[pl_x + 0.21 * pl_w, pl_y + 0.32 * pl_h], [pl_x + 0.19 * pl_w, pl_y],
                       [pl_x + pl_w, pl_y + 0.32 * pl_h], [pl_x + 0.21 * pl_w, pl_y + pl_h],
                       [pl_x + 0.21 * pl_w, pl_y + 0.75 * pl_h], [pl_x, pl_y + 0.85 * pl_h]]
            bul.bullet_generator(win, pl_x + pl_w / 2, pl_y + pl_h / 2, rkn)
            game_time += clock.get_time() / 1000
            pnt.print_time(win, font_small, game_time)
            pl_lives, vulnerable = liv.check_bonuses(pl_lives, vulnerable, polygon, bonus_life)
            pl_spdy, pl_lives, vulnerable = liv.check_lives(pl_y, pl_spdy, pl_lives, vulnerable, polygon, hit)
            bon.bonus_generation(win, game_time, extr_l, vpn, vpn_extra)
            pnt.lives_counter(win, font_normal, pl_lives)
            pnt.draw_plane(win, pl_x, pl_y, plane, plane_dmg, vulnerable)
            pnt.draw_level(win, font_normal, level)
            pygame.display.update()

        else:  # Завершение игры
            game = False
            game_over = True
            if game_time > best_time:
                best_time = game_time
                best_result.seek(0)
                best_result.truncate()
                best_result.write(str(round(best_time, 2)) + '\n')

    if pause:  # Пауза
        pygame.time.delay(delay)
        game = False
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                click_channel = click.play()
                click_channel.set_volume(0.05)

        keys2 = pygame.key.get_pressed()

        if keys2[pygame.K_RETURN]:  # Возобновление игры по нажатию клавиши Enter
            pause = False
            game = True
            click_channel = click.play()
            click_channel.set_volume(0.05)
            spawn_timer = pygame.time.get_ticks()

        pnt.draw_pause(win, font_small, font_normal, font_huge, game_time)
        pygame.display.update()

    if game_over:  # Экран завершения игры
        vulnerable = True
        bul.speed_counter = 0
        bul.bullet_array = []
        bon.list_of_lives = []
        bon.list_of_vpn = []
        bon.list_extra = []
        bon.a = 1
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        pnt.draw_go(win, font_small, font_normal, font_huge, game_time, best_time, level)
        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:  # Начать новую игру по нажатию клавиши Enter
            level = 1
            click_channel = click.play()
            click_channel.set_volume(0.05)
            pl_x, pl_y, = pl_x0, pl_y0
            pl_spdx, pl_spdy = pl_spdx0, pl_spdy0
            pl_lives = pl_lives0
            bul.bullet_speed = bullet_speed_init
            game_over = False
            game = True
            game_time = 0
            bon.n_vpn = 1
            bon.n_ext = 1
            clock.tick()
            spawn_timer = pygame.time.get_ticks()

        if keys[pygame.K_BACKSPACE]:  # Возврат в главное меню по нажатию клавиши Backspace
            click_channel = click.play()
            click_channel.set_volume(0.05)
            game_over = False
            menu = True

best_result.close()  # Закрытие файла с лучшим результатом
pygame.quit()  # Завершение Pygame
quit()  # Завершение программы
