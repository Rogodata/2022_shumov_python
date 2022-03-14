import pygame
from math import copysign
from pygame.draw import *
from random import randint

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


def set_score(score):
    print("score is: " + str(score))


def new_ball(surface, balls_array, number):
    '''рисует новый шарик '''
    balls_array[number][0] = randint(100, 1100)
    balls_array[number][1] = randint(100, 900)
    balls_array[number][2] = randint(10, 100)
    balls_array[number][3] = COLORS[randint(0, 5)]
    balls_array[number][4] = (copysign(randint(1, 5), randint(-2, 1)))
    balls_array[number][5] = (copysign(randint(1, 5), randint(-2, 1)))
    circle(surface, balls_array[number][3], (balls_array[number][0], balls_array[number][1]), balls_array[number][2])
    pygame.display.update()


balls = []


# массив шариков 0 - х 1 - у 2 - р 3 - цвет 4 - Vx, 5 - Vy
def mergeballs(surface, balls_array, balls_number):
    for i in range(balls_number):
        if balls_array[i][0] > 1200 - balls_array[i][2] or balls_array[i][0] < balls_array[i][2]:
            balls_array[i][4] = - balls_array[i][4]
        if balls_array[i][1] > 900 - balls_array[i][2] or balls_array[i][1] < balls_array[i][2]:
            balls_array[i][5] = - balls_array[i][5]
        balls_array[i][0] += balls_array[i][4]
        balls_array[i][1] += balls_array[i][5]
        circle(surface, balls_array[i][3], (balls_array[i][0], balls_array[i][1]),
               balls_array[i][2])
    pygame.display.update()


def find_shot(surface, x_pos, y_pos, balls_array, balls_number):
    for i in range(balls_number):

        if (x_pos - balls_array[i][0]) ** 2 + (y_pos - balls_array[i][1]) ** 2 <= balls_array[i][2] ** 2:
            print('Click! You did it')
            new_ball(surface, balls_array, i)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

#print("How many balls do you want tto see on the screen simultaniously? (number)")
#balls_quantity = int(input("number:"))
#print("How many seconds would you like the ball to be on the screen")
#life_time = int(input("number:"))
#life_time *= FPS
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
            find_shot(screen, x0, y0, balls, balls_quantity)
    screen.fill(BLACK)
    mergeballs(screen, balls, balls_quantity)
    #pygame.display.update()

pygame.quit()
