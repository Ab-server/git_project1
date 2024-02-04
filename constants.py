# Все используемые константы
win_w = 800  # Ширина окна
win_h = int(3 * win_w / 4)  # Высота окна
scaling = win_w / 800  # Масштаб
bull_w = 50  # Размер пули
bonus_w = 70  # Размер бонуса

# Константы, необходимые для отрисовки самолётика
pl_w = 150 * scaling  # Ширина фигуры самолётика
pl_h = pl_w / 3  # Высота фигуры самолётика

midle_x = (win_w - pl_w) / 2  # Координаты центра экрана
midle_y = (win_h - pl_h) / 2
pl_x0 = midle_x  # Стартовые координаты самолётика
pl_y0 = midle_y
bull_w = 55 * scaling  # Размер пули
bonus_w = 55 * scaling  # Размер бонуса
bullet_speed_init = 4.6 * scaling
bullet_speed_add = 0.7 * scaling

bonus_speed = 5 * scaling  # скорость бонус жизни
t_ext = 15  # время, через которое выпускается новая бонус жизнь
n_ext = 4  # количество бонус жизней, сгенерированных за игру
t_vpn = 10  # время, через которое выпускается VPN
n_vpn = 5  # количество VPN, сгенерированных за игру

spd = 7 * scaling  # Скорость самолетика вдоль оси х
pl_g = 0.5 * scaling  # Ускорение свободного самолёта
a_down = pl_g * 1.2  # Ускорение самолета при движении вниз
shell_r = 3 * scaling  # Радиус снаряда
delay = 17
t = 1  # Время одного движения
spd_up = -8 * scaling  # Скорость, приобретаемая при движении вверх

invulnerability_t = 300  # Время неуязвимости после потери жизни
invulnerability_t_damage = 500
invulnerability_t_bonus = 1000
invulnerability_t_extra = 3000

t_vul = 0  # Счетчик который отвечает за учет invulnerability_t в процедуре check_lives()
t_add = 5  # Для счетчика , сколько должен самолет быть неуязвимым
rescue_spd = 2 * spd

# Необходимо ограничить движение самолётика вдоль оси Х
brd = spd  # min расстояние на которое самолетик может приблизится к краям экрана

# Константы, необходимые для отрисовки облаков
cld_w = int(160 * scaling)
cld_h = int(103 * scaling)
shift = int(0.3 * cld_h)

cld_border_shift = cld_w * 0.5

cld_v = 3.5 * scaling  # Скорость движения облаков, с ней можно играться

speed_counter_lim = 4000  # Предел увеличения скорости пуль
