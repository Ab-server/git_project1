from constants import *
import bullets as bul
import bonuses as bon


def check_lives(y, pl_spdy, lives, vulnerable, polygon, hit):

    """Процедура, которая проверяет события, влекущие за собой потерю жизней
            Аргументы:
            y - координата самолётика по оси Y
            pl_spdy - скорость самолётика по оси Y
            lives - переменная, отвечающая за количество жизней
            vulnerable - флаг, показывающий является ли цель уязвимой в данный момент
            polygon - многоугольник, задающий самолётик
            hit - звук при попадании пули"""

    global t_vul, invulnerability_t
    if y > (win_h - brd) and vulnerable:
        pl_spdy = -rescue_spd
        lives = lives - 1
        vulnerable = False
        invulnerability_t = invulnerability_t_damage
    for bull in bul.bullet_array:
        if bul.crossing(polygon, bull.x, bull.y, bull.rad) and vulnerable:
            lives = lives - 1
            hit_channel = hit.play()
            hit_channel.set_volume(0.1)
            del bul.bullet_array[bul.bullet_array.index(bull)]
            vulnerable = False
            invulnerability_t = invulnerability_t_damage
    if not vulnerable:
        if y >= win_h:
            pl_spdy = -rescue_spd
        t_vul += t_add
        if t_vul >= invulnerability_t:
            vulnerable = True
            t_vul = 0

    return pl_spdy, lives, vulnerable


def check_bonuses(lives, vulnerable, polygon, bonus_life):
    """Процедура, которая проверяет подбор бонуса
            Аргументы:
            lives - переменная, отвечающая за количество жизней
            vulnerable - флаг, показывающий является ли цель уязвимой в данный момент
            polygon - многоугольник, задающий самолётик
            bonus_life - звук при подбирании бонуса"""
    global invulnerability_t
    for bonus in bon.list_of_lives:
        if bul.crossing(polygon, bonus.x, bonus.y, bonus.rad):
            if lives < 6:
                lives = lives + 1
            bonus_life_channel = bonus_life.play()
            bonus_life_channel.set_volume(0.1)
            del bon.list_of_lives[bon.list_of_lives.index(bonus)]

    for bonus in bon.list_of_vpn:
        if bul.crossing(polygon, bonus.x, bonus.y, bonus.rad):
            vulnerable = False
            bonus_life_channel = bonus_life.play()
            bonus_life_channel.set_volume(0.1)
            del bon.list_of_vpn[bon.list_of_vpn.index(bonus)]
            invulnerability_t = invulnerability_t_bonus

    for bonus in bon.list_extra:
        if bul.crossing(polygon, bonus.x, bonus.y, bonus.rad):
            vulnerable = False
            bonus_life_channel = bonus_life.play()
            bonus_life_channel.set_volume(0.1)
            del bon.list_extra[bon.list_extra.index(bonus)]
            invulnerability_t = invulnerability_t_extra

    return lives, vulnerable

