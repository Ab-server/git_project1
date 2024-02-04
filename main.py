import pygame
from constants import *
import painting as pnt
import clouds as cl
import lives as liv
import bullets as bul
import bonuses as bon


pygame.init()
win = pygame.display.set_mode((win_w, win_h))  # Создание экрана для отрисовки
pygame.display.set_caption("FLYDODGE")  # Название, которое будет в шапке окна
clock = pygame.time.Clock()  # Штуковина для отсчета clock'ов

# Подгружаем всякие картинки для отрисовки
f = 'Agitpropc.otf'
font_huge = pygame.font.Font(f, int(62 * scaling))
font_normal = pygame.font.Font(f, int(38 * scaling))
font_ns = pygame.font.Font(f, int(30 * scaling))
font_small = pygame.font.Font(f, int(26 * scaling))

# Подгружаем картинки и изменяем их размер для отрисовки
logo = pygame.image.load("img/logo_tr.png").convert_alpha()
logo = pygame.transform.smoothscale(logo, (int(192 * scaling), int(192 * scaling)))

plane = pygame.image.load("img/plane.png").convert_alpha()
plane = pygame.transform.smoothscale(plane, (int(pl_w * scaling), int(pl_h * scaling)))

plane_dmg = pygame.image.load("img/plane_dmg.png").convert_alpha()
plane_dmg = pygame.transform.smoothscale(plane_dmg, (int(pl_w * scaling), int(pl_h * scaling)))

# противник
rkn = pygame.image.load("img/circle.png").convert_alpha()
rkn = pygame.transform.smoothscale(rkn, (int(bull_w * scaling), int(bull_w * scaling)))

# Бонус Щит
vpn = pygame.image.load("img/Щит.png").convert_alpha()
vpn = pygame.transform.smoothscale(vpn, (int(bonus_w * scaling), int(bonus_w * scaling)))
vpn_extra = pygame.transform.smoothscale(vpn, (int(bonus_w * 1.5), int(bonus_w * 1.5)))

# Дополнительная жизнь
extr_l = pygame.image.load("img/life.png").convert_alpha()
extr_l = pygame.transform.smoothscale(extr_l, (int(bonus_w * scaling), int(bonus_w * scaling)))

# Подгружаем картинки облаков и изменяем их размер для отрисовки
cloud_0 = pygame.image.load("img/cloud0.png").convert_alpha()
cloud_1 = pygame.image.load("img/cloud1.png").convert_alpha()
cloud_2 = pygame.image.load("img/cloud2.png").convert_alpha()
cloud_3 = pygame.image.load("img/cloud3.png").convert_alpha()
cloud0 = pygame.transform.smoothscale(cloud_0, (cld_w, cld_h))
cloud1 = pygame.transform.smoothscale(cloud_1, (cld_w, cld_h))
cloud2 = pygame.transform.smoothscale(cloud_2, (cld_w, cld_h))
cloud3 = pygame.transform.smoothscale(cloud_3, (cld_w, cld_h))

clouds_img = [cloud0, cloud1, cloud2, cloud3]  # Массив всех возможных форм облачков
clouds = []  # Массив облачков, которые на экране уже бегут

pl_spdx0 = spd
pl_spdy0 = 0
pl_spdx = pl_spdx0  # Текущие скорости самолётика по осям
pl_spdy = pl_spdy0

level = 1 # Уровень игры


pl_lives0 = 3
pl_lives = pl_lives0

pl_x = midle_x  # Текущие координаты самолётика
pl_y = midle_y

vulnerable = True  # Флаг, показывающий является ли цель уязвимой в данный момент

best_result = open('best_result.txt', 'r+')
game_time = 0  # Счётчик текущего времени игры
best_time = float(best_result.readline())  # Тут хранится лучшее время на данном устройстве

counter_cloud = cld_border_shift

# Всякие флаги
crashed = False  # Флаг для проверки закрывания программы
menu = True  # Флаг, показывающий, что игрок находится (не находится) в меню
game_over = False  # Флаг, показывающий, что игрок играет (не играет)
game = False  # Флаг, показывающий, что игрок видит (не видит) окно GAME OVER
pause = False

# Прогружаем звуки для игры
hit = pygame.mixer.Sound('sound/telerun_hit.ogg')
bonus_life = pygame.mixer.Sound('sound/telerun_bonus_life.ogg')
music = pygame.mixer.music.load('sound/telerun_theme.ogg')
up = pygame.mixer.Sound('sound/telerun_up.ogg')
click = pygame.mixer.Sound('sound/telerun_click.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)


# Функция, свободного падения
def fall(dt, y, spdy, ay):
    y += spdy * dt + ay * dt ** 2 / 2
    spdy += ay * dt
    return y, spdy

spawn_timer = pygame.time.get_ticks()

while not crashed:
    win.fill((255, 255, 255))
    if cl.clouds_run(win, clouds, clouds_img, counter_cloud):
        counter_cloud = 0
    else:
        counter_cloud += 1

    if menu:
        pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_channel = click.play()
                click_channel.set_volume(0.5)
                crashed = True

        pnt.draw_menu(win, font_small, font_normal, font_ns, font_huge, logo, best_time)  # Рисуем меню
        pygame.display.update()
        keys = pygame.key.get_pressed()  # Все нажатые кнопки

        if keys[pygame.K_RETURN]:  # Новая игра
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

    if game:
        if pl_lives > 0:
            clock.tick()
            if pygame.time.get_ticks() - spawn_timer >= 10000:
                bul.bullet_speed *= 1.2
                level += 1
                spawn_timer = pygame.time.get_ticks()
            pygame.time.delay(delay)

            for event in pygame.event.get():  # Проверка на выход из игры
                if event.type == pygame.QUIT:
                    crashed = True
                    click_channel = click.play()
                    click_channel.set_volume(0.1)

            keys = pygame.key.get_pressed()  # Все нажатые кнопки

            if keys[pygame.K_SPACE]:
                pause = True
                click_channel = click.play()
                click_channel.set_volume(0.1)

            if keys[pygame.K_RIGHT] and (win_w - pl_x >= pl_w + brd):  # Движение вправо
                pl_x += pl_spdx * t

            if keys[pygame.K_LEFT] and (pl_x >= brd):  # Движение влево
                pl_x -= pl_spdx * t

            if (not keys[pygame.K_DOWN] and not keys[pygame.K_UP]) or (
                    keys[pygame.K_DOWN] and keys[pygame.K_UP]):  # Падение
                pl_y, pl_spdy = fall(t, pl_y, pl_spdy, pl_g)

            else:
                if keys[pygame.K_UP] and (pl_y > brd):  # Движение вверх
                    pl_y, pl_spdy = fall(t, pl_y, spd_up, pl_g)

                if pl_y < brd:  # Выход за границы по высоте
                    pl_spdy = 0

                if keys[pygame.K_DOWN]:  # Движение вниз
                    pl_y, pl_spdy = fall(t, pl_y, pl_spdy, a_down)
            if pl_y <= brd:  # Ограничение сверху
                pl_y = brd

            if pl_y >= win_h - brd:
                up_channel = up.play()
                up_channel.set_volume(0.1)

            polygon = [[pl_x + 0.21 * pl_w, pl_y + 0.32 * pl_h], [pl_x + 0.19 * pl_w, pl_y],
                       [pl_x + pl_w, pl_y + 0.32 * pl_h], [pl_x + 0.21 * pl_w, pl_y + pl_h],
                       [pl_x + 0.21 * pl_w, pl_y + 0.75 * pl_h], [pl_x, pl_y + 0.85 * pl_h]]
            bul.bullet_generator(win, pl_x + pl_w / 2, pl_y + pl_h / 2, rkn)

            game_time += clock.get_time() / 1000  # Обновление игрового времени
            pnt.print_time(win, font_small, game_time)  # Вывод времени на экран

            pl_lives, vulnerable = liv.check_bonuses(pl_lives, vulnerable, polygon, bonus_life)
            pl_spdy, pl_lives, vulnerable = liv.check_lives(pl_y, pl_spdy, pl_lives, vulnerable,
                                                            polygon, hit)
            bon.bonus_generation(win, game_time, extr_l, vpn, vpn_extra)
            pnt.lives_counter(win, font_normal, pl_lives)  # Прорисовка счетчика жизней

            pnt.draw_plane(win, pl_x, pl_y, plane, plane_dmg, vulnerable)
            pnt.draw_level(win, font_normal, level)
            pygame.display.update()  # Перерисовка всего экрана

        else:
            game = False
            game_over = True
            if game_time > best_time:  # Сохранение лучшего времени
                best_time = game_time
                best_result.seek(0)
                best_result.truncate()
                best_result.write(str(round(best_time, 2)) + '\n')
    if pause:
        pygame.time.delay(delay)
        game = False
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                click_channel = click.play()
                click_channel.set_volume(0.05)

        keys2 = pygame.key.get_pressed()  # Все нажатые кнопки

        if keys2[pygame.K_RETURN]:
            pause = False
            game = True
            click_channel = click.play()
            click_channel.set_volume(0.05)
            spawn_timer = pygame.time.get_ticks()

        pnt.draw_pause(win, font_small, font_normal, font_huge, game_time)
        pygame.display.update()

    if game_over:
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
        pnt.draw_go(win, font_small, font_normal, font_huge, game_time,
                    best_time, level)  # Отрисовка game_over
        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:  # Новая игра
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

        if keys[pygame.K_BACKSPACE]:  # Выход в меню
            click_channel = click.play()
            click_channel.set_volume(0.05)
            game_over = False
            menu = True

best_result.close()
pygame.quit()  # Завершение программы
quit()
