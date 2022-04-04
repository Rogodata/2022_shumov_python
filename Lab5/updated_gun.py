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
PLAYER_START_POS_Y = 515

ENEMY_TANKS_NUM = 4
BOMBERS_RESPAWN = 3
FIREBOMBERS_RESPAWN = 3

DEFEAT_X_POS = 200


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
        self.ptur_reload = 10

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
            self.v = 3
        elif moving_event.key == pygame.K_a:
            self.v = -3

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
            self.previous_ptur = time.time()
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
        self.height = LANDSHAFT_HEIGHT

    def draw(self):
        dr.rect(self.screen, 0x243c07, (0, HEIGHT - LANDSHAFT_HEIGHT, WIDTH, LANDSHAFT_HEIGHT))

    def hittest(self, attack_bullet):
        return attack_bullet.y > HEIGHT - self.height

    def death(self, attack_bullet, explosions_array):
        explosion = Explosion(self.screen, 3, 3, attack_bullet.x, attack_bullet.y, 6, minr=2)
        explosions_array.append(explosion)


class Ptur(Bullet):
    def __init__(self, surface, x, y, v, angle, d=5, l=15, lifetime=7):
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
        self.vx = self.v * math.cos(self.dest_angle)
        self.vy = self.v * math.sin(self.dest_angle)
        self.set_dest(x_dest, y_dest)

    def set_dest(self, x_dest, y_dest):
        self.x_dest = x_dest
        self.y_dest = y_dest
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
        if not (self.x_dest - 5 < self.x < self.x_dest + 5 and self.y_dest - 5 < self.y < self.y_dest + 5):
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
        self.set_dest(200, -100)
        return bomb


class FiringBomber(Bomber):
    def __init__(self, surface, x, y, x_dest, y_dest):
        Bomber.__init__(self, surface, x, y, x_dest, y_dest)
        self.bombed = 0
        self.target_angle = -math.pi
        self.ready_to_fire = 0
        self.previous_shot = time.time()
        self.reload = 3
        self.caliber = 3
        self.length = self.r * 1.5

    def set_target(self, target_x, target_y):
        if target_x - self.x > 0:
            self.target_angle = math.atan((target_y - self.y) / (target_x - self.x))
        elif target_x - self.x < 0:
            self.target_angle = math.atan((target_y - self.y) / (target_x - self.x)) - math.pi
        else:
            self.target_angle = math.copysign(math.pi / 2, target_y - self.y)

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)
        dr.line(self.screen, BLACK, (self.x, self.y),
                (self.x + math.cos(self.target_angle) * self.length,
                 self.y + math.sin(self.target_angle) * self.length), width=self.caliber)

    def fire(self):
        bullet = Bullet(self.screen, self.x + math.cos(self.target_angle) * self.length,
                        self.y + math.sin(self.target_angle) * self.length, 10,
                        self.target_angle, self.caliber // 2)
        return bullet

class Times:
    def __init__(self):
        self.start_time = time.time()
        self.firebomber_time = time.time()
        self.bomber_time = time.time()

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


def merge_hits(player_tank, bullets_array, enemy_tanks_array, explosions_array, pturs_array, land, bombs_array,
               bombers_array, firebombers_array):
    hits_array = []
    for bullet in bullets_array:
        hits_array.append(bullet)
    for ptur_entity in pturs_array:
        hits_array.append(ptur_entity)
    for bomb in bombs_array:
        hits_array.append(bomb)
    for hit in hits_array:
        if player_tank.hittest(hit):
            player_tank.death(explosions_array)
            hit.hit = 1
        for t in enemy_tanks_array:
            if t.hittest(hit):
                t.death(explosions_array)
                hit.hit = 1
        for b in bombers_array:
            if b.hittest(hit):
                b.death(explosions_array)
                hit.hit = 1
        for fb in firebombers_array:
            if fb.hittest(hit):
                fb.death(explosions_array)
                hit.hit = 1
        if land.hittest(hit):
            land.death(hit, explosions_array)
            hit.hit = 1


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
    player_tank.move()
    player_tank.draw()
    player_tank.empower()


def merge_bombers(bombers_array, bombs_array):
    bombers_merged = []
    for b in bombers_array:
        if b.alive() and (b.mission or b.y > -30):
            b.move()
            b.draw()
            if b.mission == 0 and b.bombed:
                released_bomb = b.release_bomb()
                bombs_array.append(released_bomb)
            bombers_merged.append(b)
    return bombers_merged


def merge_firebombers(bombers_array, bullets_array):
    bombers_merged = []
    for b in bombers_array:
        if b.alive():
            b.move()
            b.draw()
            if time.time() - b.previous_shot > b.reload:
                bullets_array.append(b.fire())
                b.previous_shot = time.time()
                b.set_dest(randint(700, 900), randint(200, 300))
            bombers_merged.append(b)
    return bombers_merged, bullets_array


def merge_objects(player_tank, bullets_array, enemy_t_array, explosions_array, pturs_array, land, bombs_array,
                  bombers_array, firebombers_array):
    bullets_array = merge_bullets(bullets_array)
    enemy_t_array = merge_tanks(enemy_t_array)
    bombers_array = merge_bombers(bombers_array, bombs_array)
    firebombers_array, bullets_array = merge_firebombers(firebombers_array, bullets_array)
    bombs_array = merge_bombs(bombs_array)
    pturs_array = merge_ptur(pturs_array)
    merge_player_tank(player_tank)
    land.draw()
    merge_hits(player_tank, bullets_array, enemy_t_array, explosions_array, pturs_array, land, bombs_array,
               bombers_array, firebombers_array)
    return bullets_array, enemy_t_array, bombers_array, firebombers_array, bombs_array, pturs_array


def event_merger(event_0, game_finish, player_tank, pturs_array, bullets_array):
    if event_0.type == pygame.QUIT:
        game_finish = True
    elif event_0.type == pygame.KEYDOWN:
        player.move_by_keyboard(event_0)
        for ptur_entity in pturs_array:
            ptur_entity.move_by_keyboard(event_0)
        pturs_array = player_tank.fire_ptur(event_0, pturs_array)
    elif event_0.type == pygame.KEYUP:
        player_tank.stop_by_keyboard(event_0)
        for ptur_entity in pturs_array:
            ptur_entity.stop_by_keyboard(event_0)
    elif event_0.type == pygame.MOUSEMOTION:
        player_tank.targetting(event_0)
    elif event_0.type == pygame.MOUSEBUTTONDOWN:
        player_tank.power_up()
    elif event_0.type == pygame.MOUSEBUTTONUP:
        bullets_array = player.fire(bullets_array)
    return game_finish, pturs_array, bullets_array


def initialize(surface):
    return [], [], [], [], [], [], [], PlayerTank(surface, PLAYER_START_POS_X, PLAYER_START_POS_Y), Landshaft(surface)





def merge_process(surface, game_finish, player_tank, tanks_array, bombers_array, firebombers_array, times_class):
    if not player_tank.alive():
        game_finish = 1
    for tank in tanks_array:
        if tank.x < DEFEAT_X_POS:
            game_finish = 1
    if len(tanks_array) < ENEMY_TANKS_NUM:
        tanks_array.append(Tank(surface, WIDTH + randint(30, 100), PLAYER_START_POS_Y, v=randint(-3, -1)))
    if len(firebombers_array) < 1 and time.time() - times_class.firebomber_time > FIREBOMBERS_RESPAWN:
        firebombers_array.append(FiringBomber(surface, WIDTH + 100, -50, randint(750, 900), randint(250, 350)))
        times_class.firebomber_time = time.time()
    if len(bombers_array) < 1 and time.time() - times_class.bomber_time > BOMBERS_RESPAWN:
        bombers_array.append(Bomber(surface, WIDTH // 2, -50, player_tank.x, randint(100, 200)))
        times_class.bomber_time = time.time()
    return game_finish


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + INTERFACE_HEIGHT))
clock = pygame.time.Clock()
finished = False

bullets, enemy_tanks, explosions, pturs, bombs, bombers, firebombers, player, landshaft = initialize(screen)
times = Times()
interface = Interface(screen, player)

while not finished:
    clock.tick(FPS)
    screen.fill(LIGHT_BLUE)
    bullets, enemy_tanks, bombers, firebombers, bombs, pturs = merge_objects(player, bullets, enemy_tanks, explosions,
                                                                             pturs, landshaft, bombs, bombers,
                                                                             firebombers)
    interface.draw()
    explosions = merge_explosions(explosions)
    pygame.display.update()
    for event in pygame.event.get():
        finished, pturs, bullets = event_merger(event, finished, player, pturs, bullets)
    finished = merge_process(screen, finished, player, enemy_tanks, bombers, firebombers, times)


pygame.quit()
