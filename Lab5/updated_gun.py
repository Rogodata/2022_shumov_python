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
LANDSHAFT_HEIGHT = 70

PLAYER_START_POS_X = 110
PLAYER_START_POS_Y = 500


class Tank:
    def __init__(self, surface, x, y, v=0):
        self.surface = surface
        self.x = x
        self.y = y
        self.fire_angle = - 5 * math.pi / 6
        self.height = 15
        self.width = 50
        self.r = 10
        self.caliber = 3
        self.color = 0x3c3e4d
        self.power_on = 0
        self.v = v
        self.wheel_radius = self.width // 10
        self.life = 1
        self.power = 10
        self.ptured = 0
        self.previous_ptur = time.time()
        self.ptur_reload = 15

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
        if self.ptured:
            ptur_0 = Ptur(self.surface, self.x, self.y - 2 * self.r, 4, 0)
            ptur_0.draw()

    def move(self):
        self.x += self.v

    def power_start(self):
        self.power_on = 1

    def hittest(self, attack_bullet):
        return (self.x + self.width / 2 > attack_bullet.x > self.x - self.width / 2 and self.y + self.height / 2 >
                attack_bullet.y > self.y - self.height / 2) or \
               ((attack_bullet.x - self.x) ** 2 + (attack_bullet.y - self.y + self.height / 2) ** 2 < self.r ** 2)

    def death(self, explosions_array):
        explosion = Explosion(self.surface, 10, 0, self.x, self.y, self.width // 2, minr=3)
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
        self.hit = 0

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
        self.color = DARK_GREEN
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

    def fire_ptur(self, firing_event, pturs_array):
        if firing_event.key == pygame.K_f and self.ptured == 1:
            ptur_rocket = Ptur(self.surface, self.x, self.y - 2 * self.r, 4, 0)
            self.ptured = 0
            pturs_array.append(ptur_rocket)
        return pturs_array


class Interface:
    def __init__(self, surface, player_tank):
        self.e = 1
        self.screen = surface
        self.tank = player_tank

    def draw(self):
        dr.rect(self.screen, INTERFACE_COLOR, (0, HEIGHT, WIDTH, INTERFACE_HEIGHT))
        dr.rect(self.screen, YELLOW, (WIDTH // 5, HEIGHT + INTERFACE_HEIGHT // 3, WIDTH // 10, INTERFACE_HEIGHT // 3))
        dr.rect(self.screen, RED,
                (WIDTH // 10, HEIGHT + INTERFACE_HEIGHT // 3, WIDTH // 300 * self.tank.power, INTERFACE_HEIGHT // 3))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Power:", False, (0, 255, 0))
        self.screen.blit(textsurface, (WIDTH // 20, HEIGHT + INTERFACE_HEIGHT // 4))


class Landshaft:
    def __init__(self, surface):
        self.screen = surface

    def draw(self):
        dr.rect(self.screen, GREEN, (0, HEIGHT - LANDSHAFT_HEIGHT, WIDTH, LANDSHAFT_HEIGHT))

    def hittest(self, attack_bullet):
        return attack_bullet.y > HEIGHT - LANDSHAFT_HEIGHT

    def death(self, attack_bullet, explosions_array):
        explosion = Explosion(self.screen, 3, 3, attack_bullet.x, attack_bullet.y, 6, minr=2)
        explosions_array.append(explosion)


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
                  (self.x, self.y),
                  self.r * 3 // 4)
        explosion = Explosion(self.screen, 3, 1, self.x - math.cos(self.angle) * self.length,
                              self.y - math.sin(self.angle) * self.length, 3)
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


class Bomb(Ptur):
    def __init__(self, surface, x, y, v):
        Ptur.__init__(self, surface, x, y, v, angle=math.pi / 2, d=5, l=10, lifetime=13)

    def draw(self):
        dr.line(self.screen, BLACK,
                (self.x - math.cos(self.angle) * self.length, self.y - math.sin(self.angle) * self.length),
                (self.x, self.y),
                width=self.r)
        dr.circle(self.screen, RED,
                  (self.x, self.y),
                  self.r * 3 // 4)

    def move_by_keyboard(self, moving_event):
        return 0

    def stop_by_keyboard(self, stopping_event):
        return 0


class Bomber:
    def __init__(self, surface, x, y, x_dest, y_dest, v=2):
        self.screen = surface
        self.x = x
        self.y = y
        self.x_dest = x_dest
        self.y_dest = y_dest
        self.color = 0x3c3e4d
        self.v = v
        self.r = 15
        self.bombed = 1
        self.life = 1
        self.dest_angle = 0
        self.mission = 1
        if x_dest - self.x > 0:
            self.dest_angle = math.atan((y_dest - self.y) / (x_dest - self.x))
        elif x_dest - self.x < 0:
            self.dest_angle = math.atan((y_dest - self.y) / (x_dest - self.x)) - math.pi
        else:
            self.dest_angle = math.copysign(math.pi / 2, y_dest - self.y)
        self.vx = self.v * math.cos(self.dest_angle)
        self.vy = self.v * math.sin(self.dest_angle)

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)
        if self.bombed:
            bomb = Bomb(self.screen, self.x, self.y + self.r, 0)
            bomb.draw()

    def move(self):
        if not (self.x_dest - 5 <self.x < self.x_dest + 5 or self.y_dest - 5 <self.y < self.y_dest + 5):
            self.x += self.vx
            self.y += self.vy
        else:
            self.mission = 0

    def hittest(self, attack_bullet):
        return (attack_bullet.x - self.x) ** 2 + (attack_bullet.y - self.y) ** 2 < self.r ** 2

    def death(self, explosions_array):
        explosion = Explosion(self.screen, 10, 0, self.x, self.y, self.r, minr=3)
        explosions_array.append(explosion)
        self.life = 0
        self.color = BLACK

    def alive(self):
        return self.life > 0

    def release_bomb(self):
        bomb = Bomb(self.screen, self.x, self.y + self.r, 6)
        self.bombed = 0
        self.x_dest = 200
        self.y_dest = -50
        return bomb


def merge_bullets(bullets_array):
    bullets_merged = []
    for b in bullets_array:
        if b.in_bounds() and b.hit == 0:
            b.move()
            b.draw()
            bullets_merged.append(b)
    return bullets_merged

def merge_bombs(bombs_array):
    bombs_merged = []
    for b in bombs_array:
        if b.in_bounds() and b.hit == 0:
            b.move()
            b.draw()
            bombs_merged.append(b)
    return bombs_merged

def merge_ptur(pturs_array):
    merged_pturs = []
    for ptur_entity in pturs_array:
        if time.time() - ptur_entity.lived_s < ptur_entity.lifetime and ptur_entity.hit == 0:
            ptur_entity.draw()
            ptur_entity.move()
            merged_pturs.append(ptur_entity)
    return merged_pturs


def merge_hits(player_tank, bullets_array, enemy_tanks_array, explosions_array, pturs_array, land, bombs_array):
    hits_array = []
    for bullet in bullets_array:
        hits_array.append(bullet)
    for ptur_entity in pturs_array:
        hits_array.append(ptur_entity)
    for bomb in bombs_array:
        hits_array.append(bomb)
    for h in hits_array:
        if player_tank.hittest(h):
            player_tank.death(explosions_array)
            h.hit = 1
        for t in enemy_tanks_array:
            if t.hittest(h):
                t.death(explosions_array)
                h.hit = 1
        if land.hittest(h):
            land.death(h, explosions_array)
            h.hit = 1


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
            tanks_merged.append(t)
    return tanks_merged


def merge_player_tank(player_tank):
    if time.time() - player_tank.previous_ptur > player_tank.ptur_reload and not player_tank.ptured:
        player_tank.ptured = 1
        player_tank.previous_ptur = time.time()
    player_tank.move()
    player_tank.draw()
    player_tank.empower()

def merge_bombers(bombers_array, bombs_array):
    bombers_merged = []
    for b in bombers_array:
        if b.alive() and (b.mission or b.y > -20):
            b.move()
            b.draw()
            if b.mission == 0 and b.bombed:
                released_bomb = b.release_bomb()
                bombs_array.append(released_bomb)
            bombers_merged.append(b)
    return bombers_merged, bombs_array


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + INTERFACE_HEIGHT))
clock = pygame.time.Clock()
finished = False

bullets = []
enemy_tanks = []
explosions = []
pturs = []
bombs = []
bombers = []
player = PlayerTank(screen, PLAYER_START_POS_X, PLAYER_START_POS_Y)
landshaft = Landshaft(screen)
interface = Interface(screen, player)
game_start_time = time.time()


def time_played(start_time):
    return time.time() - start_time


for i in range(3):
    tank = Tank(screen, WIDTH + 100 * i, PLAYER_START_POS_Y, v=-3)
    enemy_tanks.append(tank)

for i in range(3):
    bomber = Bomber(screen, -20, -30, randint(100, 300), randint(100, 200))
    bombers.append(bomber)

while not finished:
    clock.tick(FPS)
    screen.fill(LIGHT_BLUE)
    # ТУТ рисуем
    bullets = merge_bullets(bullets)
    enemy_tanks = merge_tanks(enemy_tanks)
    bombers, bombs = merge_bombers(bombers, bombs)
    bombs = merge_bombs(bombs)
    pturs = merge_ptur(pturs)
    merge_player_tank(player)
    landshaft.draw()
    interface.draw()
    merge_hits(player, bullets, enemy_tanks, explosions, pturs, landshaft, bombers)
    explosions = merge_explosions(explosions)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            player.move_by_keyboard(event)
            for ptur in pturs:
                ptur.move_by_keyboard(event)
            pturs = player.fire_ptur(event, pturs)
        elif event.type == pygame.KEYUP:
            player.stop_by_keyboard(event)
            for ptur in pturs:
                ptur.stop_by_keyboard(event)
        elif event.type == pygame.MOUSEMOTION:
            player.targetting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.power_up()
        elif event.type == pygame.MOUSEBUTTONUP:
            bullets = player.fire(bullets)

pygame.quit()
