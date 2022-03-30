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
INTERFACE_COLOR = 0x5d4a33
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1100
HEIGHT = 600
INTERFACE_HEIGHT = 150

# FIXME вырази через ширину и высоту
PLAYER_START_POS_X = 110
PLAYER_START_POS_Y = 420


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

class KeyboardOperatedEntity:
    def __init__(self, button1, button2):
        self

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
    def ini(self):
        self.ptur = 1

    def move_by_keyboard(self, moving_event):
        if moving_event.key == pygame.K_d:
            self.v = 2
        elif moving_event.key == pygame.K_a:
            self.v = -2

    def stop_by_keyboard(self, stopping_event):
        if stopping_event.key == pygame.K_d or stopping_event.key == pygame.K_a:
            self.v = 0

    def targetting(self, target_event):
        if target_event.pos[0] - self.x > 0:
            self.fire_angle = math.atan((target_event.pos[1] - self.y) / (target_event.pos[0] - self.x))
        elif target_event.pos[0] - self.x < 0:
            self.fire_angle = math.atan((target_event.pos[1] - self.y) / (target_event.pos[0] - self.x)) - math.pi
        else:
            self.fire_angle = math.copysign(math.pi / 2, target_event.pos[1] - self.y)

    # def find_ground_angle


class Interface:
    def __init__(self, surface, player_tank):
        self.e = 1
        self.screen = surface
        self.tank = player_tank

    def draw(self):
        dr.rect(self.screen, INTERFACE_COLOR, (0, HEIGHT, WIDTH, INTERFACE_HEIGHT))


class Landshaft:
    def __init__(self, surface):
        self.screen = surface


class Ptur:
    def __init__(self, surface, x, y, v, angle, d = 3, l = 10):
        self.screen = surface
        self.length = l
        self.diam = d
        self.angle = angle
        self.omega = 0
        self.v = v
        self.x = x
        self.y = y

    def draw(self):
        dr.polygon(self.screen, BLACK, [(self.x - self.length / 2, self.y - self.diam / 2),
                                        (self.x + self.length / 2, self.y - self.diam / 2),
                                        (self.x + self.length / 2, self.y + self.diam / 2),
                                        (self.x - self.length / 2, self.y + self.diam / 2),
                                        (self.x - self.length / 2, self.y - self.diam / 2)])
        dr.ellipse(self.screen, BLACK, ((self.x, self.y - self.diam / 2),
                                        (self.length, self.diam)))

    def move_by_keyboard(self, moving_event):
        if moving_event.key == pygame.K_w:
            self.omega = math.pi / (2 * FPS)
        elif moving_event.key == pygame.K_s:
            self.omega = - math.pi / (2 * FPS)

    def stop_by_keyboard(self, stopping_event):
        if stopping_event.key == pygame.K_w or stopping_event.key == pygame.K_s:
            self.omega = 0

    def move(self):
        self.angle += self.omega
        self.x += self.v * math.cos(self.angle)
        self.y += self.v * math.sin(self.angle)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + INTERFACE_HEIGHT))
clock = pygame.time.Clock()
finished = False

ptur= Ptur(screen, 20, 20, 1, 0)
player = PlayerTank(screen, PLAYER_START_POS_X, PLAYER_START_POS_Y)
interface = Interface(screen, player)

while not finished:
    clock.tick(FPS)
    screen.fill(WHITE)
    # ТУТ рисуем
    player.draw()
    ptur.draw()
    interface.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            player.move_by_keyboard(event)
            ptur.move_by_keyboard(event)
        elif event.type == pygame.KEYUP:
            player.stop_by_keyboard(event)
            ptur.stop_by_keyboard(event)
        elif event.type == pygame.MOUSEMOTION:
            player.targetting(event)
    # gun.power_up()
    player.move()
    ptur.move()

pygame.quit()

'''elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)'''
