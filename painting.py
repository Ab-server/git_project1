from constants import *


def draw_menu(win, font_small, font_normal, font_ns, font_huge, logo, best_time):
    """Процедура, при вызове которой отрисовывается экран мен.
            Аргументы:
            win - окно отрисовки
            font_small, font_normal, font_hugу - соотв. шрифты из main
            logo - файл logo.png
            best_time - лучшее время за сессию"""
    telerun_txt = font_huge.render('FLYDODGE', True, (0, 137, 204))
    win.blit(telerun_txt, [0.46 * win_w, 0.3 * win_h])

    press_txt = font_ns.render('', True, (0, 137, 204))
    win.blit(press_txt, [0.13 * win_w, 0.6 * win_h])
    press_txt = font_ns.render('', True, (0, 137, 204))
    win.blit(press_txt, [0.2 * win_w, 0.65 * win_h])
    press_txt = font_normal.render('Нажмите ENTER для старта...', True, (0, 137, 204))
    win.blit(press_txt, [0.13 * win_w, 0.8 * win_h])

    bestt_txt = font_small.render('Лучшее время: ' + str(round(best_time, 1)) + 'С', True, (0, 137, 204))
    win.blit(bestt_txt, [10 * scaling, 0.93 * win_h])

    win.blit(logo, (int(145 * scaling), int(108 * scaling)))


def draw_go(win, font_small, font_normal, font_huge, game_time, best_time, level):
    """Процедура, при вызове которой отрисовывается экран 'GAME OVER'
            Аргументы:
            win - окно отрисовки
            font_small, font_normal, font_hugу - соотв. шрифты из main
            game_time - время завершенной игры
            best_time - лучшее время за сессию"""
    go_txt = font_huge.render('Игра окончена', True, (0, 137, 204))
    go_rec = go_txt.get_rect()
    go_rec.center = (win_w / 2, win_h / 3)
    win.blit(go_txt, go_rec)

    yres_txt = font_small.render('Ваш результат: ' + str(round(game_time, 1)) + 'С;  ' + 'Ваш уровень: ' + str(level),
                                 True, (0, 137, 204))
    yres_rec = yres_txt.get_rect()
    yres_rec.center = (win_w / 2, win_h / 3 + 100 * scaling)
    bestres_txt = font_normal.render('Лучший результат: ' + str(round(best_time, 1)) + 'С', True, (0, 137, 204))
    bestres_rec = bestres_txt.get_rect()
    bestres_rec.center = (win_w / 2, win_h / 3 + 150 * scaling)
    win.blit(yres_txt, yres_rec)
    win.blit(bestres_txt, bestres_rec)

    rest_txt = font_small.render('Нажмите ENTER чтобы начать заново', True, (0, 137, 204))
    rest_rec = rest_txt.get_rect()
    rest_rec.center = (win_w / 2, 2 * win_h / 3 + 50 * scaling)

    back_txt1 = font_small.render('Нажмите SPACE', True, (0, 137, 204))
    back_rec1 = back_txt1.get_rect()
    back_rec1.center = (win_w / 2, 2 * win_h / 3 + 110 * scaling)

    back_txt2 = font_small.render('для паузы', True, (0, 137, 204))
    back_rec2 = back_txt2.get_rect()
    back_rec2.center = (win_w / 2, 2 * win_h / 3 + 150 * scaling)

    win.blit(rest_txt, rest_rec)
    win.blit(back_txt1, back_rec1)
    win.blit(back_txt2, back_rec2)


def draw_pause(win, font_small, font_normal, font_huge, game_time):
    """Процедура, при вызове которой отрисовывается экран паузы
            Аргументы:
            win - окно отрисовки
            font_small, font_normal, font_hugу - соотв. шрифты из main
            game_time - время завершенной игры"""
    go_txt = font_huge.render('ПАУЗА', True, (0, 137, 204))
    go_rec = go_txt.get_rect()
    go_rec.center = (win_w / 2, win_h / 3)
    win.blit(go_txt, go_rec)

    yres_txt = font_normal.render('Ваше время: ' + str(round(game_time, 1)) + 'С', True, (0, 137, 204))
    yres_rec = yres_txt.get_rect()
    yres_rec.center = (win_w / 2, win_h / 3 + 100 * scaling)
    win.blit(yres_txt, yres_rec)

    res_txt = font_small.render('Нажмите ENTER для продолжения...', True, (0, 137, 204))
    res_rec = res_txt.get_rect()
    res_rec.center = (win_w / 2, 2 * win_h / 3 + 50 * scaling)
    win.blit(res_txt, res_rec)


def draw_plane(win, x, y, plane, plane_dmg, vulnerable):
    """Процедура, при вызове которой отрисовывается самолётик
            Аргументы:
            win - окно отрисовки
            x - координата самолётика по оси Х (верхний левый угол)
            y - координата самолётика по оси Y (верхний левый угол)
            plane - файл plane.png (обычный самолётик)
            plane_png - файл plane_dmg.png (самолётик после ранения)
            vulnerable - флаг, говорящий о том уязвим самолётик или нет"""
    if vulnerable:  # Рисуем самолётик
        win.blit(plane, (x, y))
    else:
        win.blit(plane_dmg, (x, y))


def lives_counter(win, font, lives):
    """Процедура, при вызове которой отрисовывается текущее количество жизней
            Аргументы:
            win - окно отрисовки
            font - шрифт
            lives - переменная, отвечающая за количество жизней"""
    lives_txt = font.render(lives * "*", True, (0, 137, 204))
    win.blit(lives_txt, (10 * scaling, 10 * scaling))


def print_time(win, font, time):
    """Процедура, при вызове которой отрисовывается время текущей игры
            Аргументы:
            win - окно отрисовки
            font - шрифт
            time - переменная, отвечающая за отсчет времени"""
    time_txt = font.render(str(round(time, 1)) + " С", True, (0, 137, 204))
    time_rec = time_txt.get_rect()
    time_rec.center = (win_w / 2, 27 * scaling)
    win.blit(time_txt, time_rec)


def draw_level(win, font, level):
    level_txt = font.render('Уровень: ' + str(level), True, (0, 137, 204))
    time_rec = level_txt.get_rect()
    time_rec.center = (win_w * 0.8, 27 * scaling)
    win.blit(level_txt, time_rec)
