from random import randint
import pygame.draw as dr
import pygame
import math
import time

FPS = 60

RED = 0xFF0000
LIGHT_BLUE = 0x55e2e3
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = 0x5d8900
INTERFACE_COLOR = 0x999696
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1100
HEIGHT = 600
INTERFACE_HEIGHT = 150

# FIXME вырази через ширину и высоту
PLAYER_START_POS_X = 110
PLAYER_START_POS_Y = 500


class Tank:
    def __init__(self, surface, x, y, v=0):
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
        self.v = v
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

    def hittest(self, attack_bullet):
        return (self.x + self.width / 2 > attack_bullet.x > self.x - self.width / 2 and self.y + self.height / 2 >
                attack_bullet.y > self.y - self.height / 2) or \
               ((attack_bullet.x - self.x) ** 2 + (attack_bullet.y - self.y - self.height / 2) ** 2 < self.r ** 2)

    def death(self, explosions_array):
        explosion = Explosion(self.surface, 10, 10, self.x, self.y, self.width // 2, minr=3)
        explosions_array.append(explosion)
        self.life = 0
        self.color = BLACK

    def alive(self):
        return self.life > 0


class Bullet:
    def __init__(self, surface, x, y, v, angle, r):
        self.screen = surface
        self.x = x
        self.y = y
        self.r = r
        self.vx = v * math.cos(angle)
        self.vy = v * math.sin(angle)
        self.color = BLACK

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.vy += 10 / FPS
        self.x += self.vx
        self.y += self.vy

    def in_bounds(self):
        return WIDTH > self.x > 0 and HEIGHT > self.y > 0


class PlayerTank(Tank):
    def __init__(self, surface, x, y):
        Tank.__init__(self, surface, x, y)
        self.ptured = 0
        self.timer_s = 0
        self.reload_rate = 1

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

    def power_up(self):
        self.power_on = 1
        self.timer_s = time.time()

    def empower(self):
        if self.power_on:
            if time.time() - self.timer_s > self.reload_rate:
                if self.power < 20:
                    self.power += 5
                self.timer_s = time.time()

    def fire(self, bullets_array):
        bullet = Bullet(self.surface, self.x + math.cos(self.fire_angle) * self.width / 2,
                        self.y - self.height / 2 + math.sin(self.fire_angle) * self.width / 2, self.power,
                        self.fire_angle, self.caliber // 2)
        bullets_array.append(bullet)
        self.power = 10
        self.power_on = 0
        return bullets_array

    # def find_ground_angle


class Interface:
    def __init__(self, surface, player_tank):
        self.e = 1
        self.screen = surface
        self.tank = player_tank

    def draw(self):
        dr.rect(self.screen, INTERFACE_COLOR, (0, HEIGHT, WIDTH, INTERFACE_HEIGHT))
        dr.rect(self.screen, YELLOW, (WIDTH // 10, HEIGHT + INTERFACE_HEIGHT // 3, WIDTH // 10, INTERFACE_HEIGHT // 3))
        dr.rect(self.screen, RED,
                (WIDTH // 10, HEIGHT + INTERFACE_HEIGHT // 3, WIDTH // 300 * self.tank.power, INTERFACE_HEIGHT // 3))


class Landshaft:
    def __init__(self, surface):
        self.screen = surface


class Ptur(Bullet):
    def __init__(self, surface, x, y, v, angle, d=5, l=15, lifetime=13):
        Bullet.__init__(self, surface, x, y, v, angle, d)
        self.length = l
        self.angle = angle
        self.omega = 0
        self.v = v
        self.lifetime = lifetime
        self.lived_s = time.time()

    def draw(self):
        dr.line(self.screen, BLACK,
                (self.x - math.cos(self.angle) * self.length, self.y - math.sin(self.angle) * self.length),
                # (self.x + math.cos(self.angle) * self.length / 2, self.y + math.sin(self.angle) * self.length / 2),
                (self.x, self.y),
                width=self.r)
        dr.circle(self.screen, RED,
                  (self.x + math.cos(self.angle) * self.length / 2, self.y + math.sin(self.angle) * self.length / 2),
                  self.r * 3 // 4)
        explosion = Explosion(self.screen, 3, 1, self.x - math.cos(self.angle) * self.length / 2,
                              self.y - math.sin(self.angle) * self.length / 2, 3)
        explosion.draw()

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


class Explosion:
    def __init__(self, surface, number, lifetime, x, y, r, minr=1, color=YELLOW):
        self.screen = surface
        self.number = number
        self.lifetime = lifetime
        self.x = x
        self.y = y
        self.r = r
        self.minr = minr
        self.color = color

    def draw(self):
        for j in range(self.number):
            dr.circle(self.screen, self.color, (self.x + randint(-self.r, self.r), self.y + randint(-self.r, self.r)),
                      randint(self.minr, self.r // 2))


def merge_bullets(bullets_array):
    bullets_merged = []
    for b in bullets_array:
        if b.in_bounds():
            b.move()
            b.draw()
            bullets_merged.append(b)
    return bullets_merged


def merge_ptur(ptur_entity):
    if time.time() - ptur_entity.lived_s < ptur_entity.lifetime:
        ptur_entity.draw()


def merge_hits(player_tank, bullets_array, enemy_tanks_array, explosions_array):
    for b in bullets_array:
        if player_tank.hittest(b):
            player_tank.death(explosions_array)
        for t in enemy_tanks_array:
            if t.hittest(b):
                t.death(explosions_array)


def merge_explosions(explosions_array):
    explosions_merged = []
    for e in explosions_array:
        e.draw()
        e.lifetime -= 1
        if e.lifetime > 0:
            explosions_merged.append(e)
    return explosions_merged


def merge_tanks(tanks_array):
    tanks_merged = []
    for t in tanks_array:
        if t.alive():
            t.move()
            t.draw()
            tanks_array.append(tanks_merged)
    return tanks_merged


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + INTERFACE_HEIGHT))
clock = pygame.time.Clock()
finished = False

bullets = []
enemy_tanks = []
explosions = []

for i in range(3):
    tank = Tank(screen, WIDTH + 100 * i, PLAYER_START_POS_Y, v=-3)
    enemy_tanks.append(tank)

ptur = Ptur(screen, 20, 20, 2, 0)
player = PlayerTank(screen, PLAYER_START_POS_X, PLAYER_START_POS_Y)
interface = Interface(screen, player)

while not finished:
    clock.tick(FPS)
    screen.fill(LIGHT_BLUE)
    # ТУТ рисуем
    bullets = merge_bullets(bullets)
    enemy_tanks = merge_tanks(enemy_tanks)
    merge_ptur(ptur)
    player.draw()
    interface.draw()
    merge_hits(player, bullets, enemy_tanks, explosions)
    explosions = merge_explosions(explosions)
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.power_up()
        elif event.type == pygame.MOUSEBUTTONUP:
            bullets = player.fire(bullets)

    player.empower()
    player.move()
    ptur.move()

pygame.quit()

'''elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)'''
