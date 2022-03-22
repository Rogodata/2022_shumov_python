import pygame
from math import copysign
from math import sqrt
import pygame.draw as dr
from random import randint
import time

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

score = 0


def game_over(score_number):
    """
    Завершает игру, выводит набранные очки в чат, выводит в чат рекорд и имя игрока, поставившего его.
    Если рекорд в ходе игры был побит, то теперь предлагается вписать имя текущего игрока для добавления его
    в файл с лидерами
    :param score_number: число очков, полученных игроком на данный момент
    """
    print("Congratulations!")
    print("score is: " + str(score_number))
    with open('lab4/leader_table.txt', 'r') as f:
        lines = f.readlines()
        player = lines[-1].split()[0]
        high_score = int(lines[-1].split()[1])
    print("existing highscore is " + str(high_score) + " by " + str(player))
    if score_number > high_score:
        print("You managed to set the highscore!")
        name = str(input("tell us your name:"))
        with open('lab4/leader_table.txt', 'a') as f:
            f.write("\n" + name + ' ' + str(score_number))


def timer(surface, measured_time):
    """
    Функция, выводящая оставшееся до конца время на экран.
    :param surface: объект pygame.surface
    :param measured_time: Время от которого начинается отсчёт(в данном случае - старт игры)
    """
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render("time left" + str(30.0 - (time.time() - measured_time)), False, (0, 255, 0))
    surface.blit(textsurface, (0, 0))


def new_mukhomor(mukhomor_array):
    """
    Мухомор (сложная мишень) изначально определяется данной функцией
    Точнее определяются "поля" мухомора, характеризующие его состояние
    :param mukhomor_array: это массив определяющий состояние мухомора
    """
    mukhomor_array[0] = randint(30, 450)
    mukhomor_array[1] = randint(-60, -30)
    mukhomor_array[2] = 70
    mukhomor_array[3] = 40
    mukhomor_array[4] = randint(3, 5)
    mukhomor_array[5] = 0


def draw_mukhomor(surface, mukhomor_array):
    """
    рисует мухомор (его характеристики расписаны далее и представлены в виде списка)
    Сначала рисуется мухомор на виртуальной картинке, а затем картинка вклеивается на наш экран
    :param surface: объект pygame.surface
    :param mukhomor_array: Это список значений, характеризующих мухомор
    (конкретно написано в описании к экземпляру списка)
    """
    x = mukhomor_array[0]
    y = mukhomor_array[1]
    lx = mukhomor_array[2]
    ly = mukhomor_array[3]
    shape_surf = pygame.Surface([max(lx, ly), max(lx, ly)], pygame.SRCALPHA)
    dr.ellipse(shape_surf, (160, 160, 160), [lx / 2 - ly / 2, 0, ly, lx])
    dr.ellipse(shape_surf, (104, 102, 103), [lx / 2 - ly / 2, 0, ly, lx], width=1)
    dr.ellipse(shape_surf, (212, 50, 19), [0, 0, lx, ly])
    dr.ellipse(shape_surf, (104, 102, 103), [0, 0, lx, ly], width=1)
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 4, ly / 4, lx / 8, ly / 6])
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 2, ly / 3, lx / 6, ly / 7])
    dr.ellipse(shape_surf, (255, 255, 255), [3 * lx / 4, ly / 4, lx / 6, ly / 7])
    surface.blit(shape_surf, dest=[x, y])


def new_ball(surface, balls_array, number):
    """
    Рисует шарик с заданными в виде списка характеристиками. На вход подаётся непосредственно список шариков
    :param surface: объект pygame.surface
    :param balls_array: список списков, характеризующих шары
    :param number: номер текущего списка в массиве списков (номер шара, который мы хотим создать)
    """
    balls_array[number][2] = randint(20, 100)
    balls_array[number][0] = randint(100, 1100)
    balls_array[number][1] = randint(100, 800)
    balls_array[number][3] = COLORS[randint(0, 5)]
    balls_array[number][4] = (copysign(randint(2, 8), randint(-2, 1)))
    balls_array[number][5] = (copysign(randint(2, 8), randint(-2, 1)))
    dr.circle(surface, balls_array[number][3], (balls_array[number][0], balls_array[number][1]), balls_array[number][2])
    pygame.display.update()


'''
Это - массив шариков
каждый его эллемент явлется списком, хранящим данные о шарике, а именно (поиндексно):
0 - координата x центра шара
1 - координата y центра шара
2 - радиус шара
3 - хранит цвет шара (они определены в начале программы)
4 - скорость по оси x
5 - скорость по оси y
'''
balls = []
'''
список, определяющий состояние мухомора. Изначально все значения заданы нулями но затем, после подачи в функцию
new_mukhomor
каждое значение будет определено
Ячейки с соттветствующим индексом хранят:
0 - x - координата х правого верхнего угла, в который вписан гриб
1 - y - координата y правого верхнего угла, в который вписан гриб
2 - lx - удвоенная большая полуось эллипса шляпки мухомора
3 - ly - удвоенная малая полуось эллипса шляпки мухомора
4 - Vx - скорость изображения по оси х
5 - Vy - скорость изображения по оси y
'''
mukhomor = [0, 0, 0, 0, 0, 0]
new_mukhomor(mukhomor)


def mergeballs(surface, balls_array, balls_number):
    """
    Данная функция осуществлет проход по массиву шариков с целью развернуть те, что долетели до стенок и снова вывести
    все шары на экран для его покадрового обновления (отрисовать их)
    :param surface: объект pygame.surface
    :param balls_array: массив шариков
    :param balls_number: оличсетво шариков на экране (является количсетвом элементов в массиве шаров)
    """
    for i in range(balls_number):
        if balls_array[i][0] + balls_array[i][4] > 1200 - balls_array[i][2] or balls_array[i][0] + balls_array[i][4] < \
                balls_array[i][2]:
            balls_array[i][4] = -copysign(randint(2, 8), balls_array[i][4])
            balls_array[i][5] = copysign(randint(2, 8), balls_array[i][5])
        if balls_array[i][1] + balls_array[i][5] > 900 - balls_array[i][2] or balls_array[i][1] + balls_array[i][5] < \
                balls_array[i][2]:
            balls_array[i][5] = -copysign(randint(2, 8), balls_array[i][5])
            balls_array[i][4] = copysign(randint(2, 8), balls_array[i][4])
        balls_array[i][0] += balls_array[i][4]
        balls_array[i][1] += balls_array[i][5]
        dr.circle(surface, balls_array[i][3], (balls_array[i][0], balls_array[i][1]),
                  balls_array[i][2])


def merge_mukhomor(surface, mukhomor_array):
    """
    Данная функция переотрисовывает мухомор при обновлении экрана с учётом его скорости.
    Заметим, что он движется с ускорением
    :param surface: объект pygame.surface
    :param mukhomor_array: Это массив, определяющий мухомор (его положение)
    """
    mukhomor_array[0] += mukhomor_array[4]
    mukhomor_array[5] += 10 / FPS
    mukhomor_array[1] += mukhomor_array[5]
    draw_mukhomor(surface, mukhomor_array)


def find_shot(surface, x_pos, y_pos, balls_array, balls_number, score_number):
    """
    Данная функция проверяет, попали ли мы по шарику, то есть смотрит лежит ли точка с переданными в функцию
    координатами внутри какого-нибудь из шаров, все из которых переданы в функцию списком списков. Если мы попали,
     число очков увеличивается на 1 и пишется соответствующая надпись ('Click! You did it')
    :param surface: объект pygame.surface
    :param x_pos: координата x точки, в которой произошло событие
    :param y_pos: координата y точки, в которой произошло событие
    :param balls_array: список содержащий списки, охарактеризовывающие шары
    :param balls_number: число шаров
    :param score_number: текущее число очков, набранное игроком
    """
    for i in range(balls_number):
        if (x_pos - balls_array[i][0]) ** 2 + (y_pos - balls_array[i][1]) ** 2 <= balls_array[i][2] ** 2:
            print('Click! You did it')
            score_number += 1
            new_ball(surface, balls_array, i)
    return score_number


def mukhomor_shot(x_pos, y_pos, score_number, mukhomor_array):
    """
    Данная функция проверяет, попали ли мы по мухомору и, если попали, то в какую часть.
    Проверка ведётся сравнивая сумму расстояний от точки события до фокусов эллипсв (ножки или шляпки гриба)
    с удвоенной длиной полуоси и если сумма расстояний меньше, то точка лежит внутри эллипса.
    Если мы попали по шляпке, то в чат пишется (Cap!) и к теккущим очкам игрока прибавляется 1,
    если же мы попали по ножке (по той части, что не перекрыта шляпкой, то к текущим очкам прибавляется 3
    и в чат пишется (leg!!!!) В данном случае в функции координаты точки события переводятся в аналогичные
    в системе коррдинат прямоугольника (верхний левый угол и две стороны), в который вписан данный мухомор
    (стороны прямоугольника параллельны сторонам экрана, шляпка вписана по касательной к прямоугольнику)
    :param x_pos: координата x точки, в которой произошло событие
    :param y_pos: координата y точки, в которой произошло событие
    :param score_number: текущее число очков, набранное игроком
    :param mukhomor_array: Список, характеризующий мухомор
    """
    c = sqrt((mukhomor_array[2] / 2) ** 2 - (mukhomor_array[3] / 2) ** 2)
    x_pos -= mukhomor_array[0]
    y_pos -= mukhomor_array[1]
    if (x_pos - (mukhomor_array[2] / 2 - c)) ** 2 + (x_pos - (mukhomor_array[2] / 2 + c)) ** 2 + 2 * (
            (y_pos - mukhomor_array[3] / 2) ** 2) <= mukhomor_array[2] ** 2:
        print('Cap!')
        score_number += 1
    elif (y_pos - (mukhomor_array[2] / 2 - c)) ** 2 + (y_pos - (mukhomor_array[2] / 2 + c)) ** 2 + 2 * (
            (x_pos - mukhomor_array[2] / 2) ** 2) <= mukhomor_array[2] ** 2:
        print("Leg!!!!")
        score_number += 3
    return score_number


pygame.display.update()
clock = pygame.time.Clock()
finished = False

print("How many balls do you want to see on the screen at once? (number)")
balls_quantity = int(input("number:"))

# Время начала игры. Первое - для вызова мухомора, второе - для подсчёта таймера
start_time = time.time()
game_start_time = time.time()

for j in range(balls_quantity):
    balls.append([0, 0, 0, 0, 0, 0])
    new_ball(screen, balls, j)

score = 0
while not finished:
    clock.tick(FPS)
    # обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x0, y0) = event.pos
            score = find_shot(screen, x0, y0, balls, balls_quantity, score)
            score = mukhomor_shot(x0, y0, score, mukhomor)
    screen.fill(BLACK)
    mergeballs(screen, balls, balls_quantity)
    timer(screen, game_start_time)
    if time.time() - start_time >= 3.5:
        start_time = time.time()
        new_mukhomor(mukhomor)
        draw_mukhomor(screen, mukhomor)
    if time.time() - game_start_time > 30:
        finished = True
    merge_mukhomor(screen, mukhomor)
    pygame.display.update()

pygame.quit()

game_over(score)
