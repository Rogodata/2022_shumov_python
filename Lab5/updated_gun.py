from random import randint
import pygame.draw as dr
import pygame
import math

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = 0x5d8900
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1100
HEIGHT = 700


class Tank:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.fire_angle = 0
        self.ground_angle = 0
        self.height = 15
        self.width = 50
        self.r = 10
        self.caliber = 3
        self.color = DARK_GREEN
        self.power_on = 0
        self.v = 0
        self.wheel_radius = self.width // 10
        self.life = 1
        self.power = 10

    def change_speed(self, v):
        self.v = v

    def draw(self):
        dr.polygon(self.surface, self.color, [(self.x - self.width / 2, self.y - self.height / 2),
                                              (self.x + self.width / 2, self.y - self.height / 2),
                                              (self.x + self.width / 2, self.y + self.height / 2),
                                              (self.x - self.width / 2, self.y + self.height / 2),
                                              (self.x - self.width / 2, self.y - self.height / 2)])
        dr.circle(self.surface, self.color, (self.x, self.y - self.height / 2), self.width / 4)
        dr.line(self.surface, BLACK, (self.x, self.y - self.height / 2),
                (self.x + math.cos(self.fire_angle) * self.width / 2,
                 (self.y - self.height / 2) + math.sin(self.fire_angle) * self.width / 2), width=self.caliber)
        dr.circle(self.surface, BLACK,
                  (self.x - self.width / 2 + self.wheel_radius, self.y + self.height / 2 + self.wheel_radius),
                  self.wheel_radius)
        dr.circle(self.surface, BLACK,
                  (self.x + self.width / 2 - self.wheel_radius, self.y + self.height / 2 + self.wheel_radius),
                  self.wheel_radius)

    def move(self):
        self.x += self.v * math.cos(self.ground_angle)
        self.y += self.v * math.sin(self.ground_angle)

    def power_start(self):
        self.power_on = 1

    '''def targetting(self):
        if event_o.pos[0] - 20 != 0:
            self.fire_angle = math.atan((event_o.pos[1] - 450) / (event_o.pos[0] - 20))
        else:
            self.fire_angle = math.copysign(math.pi / 2, event_o.pos[1] - 450)
    def find_ground_angle'''


class Bullet:
    def __init__(self, surface, x, y, vx, vy, r):
        self.screen = surface
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = BLACK

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.vy += 10 / FPS
        if self.x + self.vx > WIDTH - self.r or self.x + self.vx < self.r:
            self.vx = -self.vx
        if self.y + self.vy > HEIGHT - self.r or self.y + self.vy < self.r:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy


class PlayerTank(Tank):
    def move_by_keyboard(self, moving_event):
        if moving_event.key == pygame.K_RIGHT:
            self.change_speed(4)
        if moving_event.key == pygame.K_a:
            self.change_speed(-4)
        self.move()
    def targetting(self, target_event):
        if target_event.pos[0] - self.x != 0:
            self.fire_angle = math.atan((target_event.pos[1] - self.y) / (target_event.pos[0] - self.x))
        else:
            self.fire_angle = -math.copysign(math.pi / 2, target_event.pos[1] - self.y)

    #def find_ground_angle

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

PLAYER_START_POS_X = 110
PLAYER_START_POS_Y = 220
player = PlayerTank(screen, PLAYER_START_POS_X, PLAYER_START_POS_Y)

while not finished:
    clock.tick(FPS)
    screen.fill(WHITE)
    # ТУТ рисуем
    player.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            player.targetting(event)
        elif event.type == pygame.KEYDOWN:
            player.move_by_keyboard(event)
    # gun.power_up()

pygame.quit()

'''elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)'''
