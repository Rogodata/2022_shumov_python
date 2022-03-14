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

start_time = time.time()


def set_score(score):
    print("score is: " + str(score))


def new_mukhomor(mukhomor_array):
    mukhomor_array[0] = randint(30, 450)
    mukhomor_array[1] = randint(-60, -30)
    mukhomor_array[2] = 70
    mukhomor_array[3] = 40
    mukhomor_array[4] = randint(3, 5)
    mukhomor_array[5] = 0
    mukhomor_array[6] = 0
    mukhomor_array[7] = 0


def draw_mukhomor(surface, mukhomor_array):
    x = mukhomor_array[0]
    y = mukhomor_array[1]
    lx = mukhomor_array[2]
    ly = mukhomor_array[3]
    angle = mukhomor_array[6]
    shape_surf = pygame.Surface([max(lx, ly), max(lx, ly)], pygame.SRCALPHA)
    dr.ellipse(shape_surf, (160, 160, 160), [lx / 2 - ly / 2, 0, ly, lx])
    dr.ellipse(shape_surf, (104, 102, 103), [lx / 2 - ly / 2, 0, ly, lx], width=1)
    dr.ellipse(shape_surf, (212, 50, 19), [0, 0, lx, ly])
    dr.ellipse(shape_surf, (104, 102, 103), [0, 0, lx, ly], width=1)
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 4, ly / 4, lx / 8, ly / 6])
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 2, ly / 3, lx / 6, ly / 7])
    dr.ellipse(shape_surf, (255, 255, 255), [3 * lx / 4, ly / 4, lx / 6, ly / 7])
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, dest=[x, y])


def new_ball(surface, balls_array, number):
    '''рисует новый шарик '''
    balls_array[number][2] = randint(20, 100)
    balls_array[number][0] = randint(100, 1100)
    balls_array[number][1] = randint(100, 800)
    balls_array[number][3] = COLORS[randint(0, 5)]
    balls_array[number][4] = (copysign(randint(1, 5), randint(-2, 1)))
    balls_array[number][5] = (copysign(randint(1, 5), randint(-2, 1)))
    dr.circle(surface, balls_array[number][3], (balls_array[number][0], balls_array[number][1]), balls_array[number][2])
    pygame.display.update()


balls = []
# 0 - x, 1 - y 2 - lx, 3 - ly, 4 - Vx, 5 - Vy, 6 - angle,7 - falls
mukhomor = [0, 0, 0, 0, 0, 0, 0, 0]
new_mukhomor(mukhomor)


# массив шариков 0 - х 1 - у 2 - р 3 - цвет 4 - Vx, 5 - Vy
def mergeballs(surface, balls_array, balls_number):
    for i in range(balls_number):
        if balls_array[i][0] > 1200 - balls_array[i][2] or balls_array[i][0] < balls_array[i][2]:
            balls_array[i][4] = - balls_array[i][4]
        if balls_array[i][1] > 900 - balls_array[i][2] or balls_array[i][1] < balls_array[i][2]:
            balls_array[i][5] = - balls_array[i][5]
        balls_array[i][0] += balls_array[i][4]
        balls_array[i][1] += balls_array[i][5]
        dr.circle(surface, balls_array[i][3], (balls_array[i][0], balls_array[i][1]),
                  balls_array[i][2])
    # pygame.display.update()


def merge_mukhomor(surface, mukhomor_array):
    mukhomor_array[0] += mukhomor_array[4]
    mukhomor_array[5] += 10 / FPS
    mukhomor_array[1] += mukhomor_array[5]
    draw_mukhomor(surface, mukhomor_array)


def find_shot(surface, x_pos, y_pos, balls_array, balls_number, score):
    for i in range(balls_number):
        if (x_pos - balls_array[i][0]) ** 2 + (y_pos - balls_array[i][1]) ** 2 <= balls_array[i][2] ** 2:
            print('Click! You did it')
            score += 1
            new_ball(surface, balls_array, i)
    return score


def mukhomor_shot(x_pos, y_pos, score, mukhomor_array):
    c = sqrt((mukhomor_array[2] / 2) ** 2 - (mukhomor_array[3] / 2) ** 2)
    x_pos -= mukhomor_array[0]
    y_pos -= mukhomor_array[1]
    if (x_pos - (mukhomor_array[2] / 2 - c)) ** 2 + (x_pos - (mukhomor_array[2] / 2 + c)) ** 2 + 2 * (
            (y_pos - mukhomor_array[3] / 2) ** 2) <= mukhomor_array[2] ** 2:
        print('Head!')
        score += 1
    elif (y_pos - (mukhomor_array[2] / 2 - c)) ** 2 + (y_pos - (mukhomor_array[2] / 2 + c)) ** 2 + 2 * (
            (x_pos - mukhomor_array[2] / 2) ** 2) <= mukhomor_array[2] ** 2:
        print("tail!!!!")
        score += 3
    return score

pygame.display.update()
clock = pygame.time.Clock()
finished = False

# print("How many balls do you want to see on the screen at once? (number)")
# balls_quantity = int(input("number:"))
# print("How many difficult targets do you want to see on the screen at once?")
# targets_quantity = int(input("number:"))
balls_quantity = 5

for i in range(balls_quantity):
    balls.append([0, 0, 0, 0, 0, 0])
    new_ball(screen, balls, i)

score = 0
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set_score(score)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x0, y0) = event.pos
            score = find_shot(screen, x0, y0, balls, balls_quantity, score)
            score = mukhomor_shot(x0, y0, score, mukhomor)
    screen.fill(BLACK)
    mergeballs(screen, balls, balls_quantity)
    if time.time() - start_time >= 3.5:
        start_time = time.time()
        new_mukhomor(mukhomor)
        draw_mukhomor(screen, mukhomor)
    merge_mukhomor(screen, mukhomor)
    pygame.display.update()

pygame.quit()
