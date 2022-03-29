import math
from random import choice
from random import randint
import pygame.draw as dr
import pygame.surface
from math import copysign

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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, surface: pygame.Surface, lifetime, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = surface
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(1, len(GAME_COLORS) - 1)]
        self.live = FPS * lifetime

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vy += 10 / FPS
        if self.x + self.vx > WIDTH - self.r or self.x + self.vx < self.r:
            self.vx = -self.vx
        if self.y + self.vy > HEIGHT - self.r or self.y + self.vy < self.r:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy
        self.live -= 1

    def get_life(self):
        return self.live



    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 < (self.r + obj.r) ** 2


class Gun:
    def __init__(self, surface):
        self.screen = surface
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event_o):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        # FIXME globalov bit ne dolzhno
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, 5)
        new_ball.r += 5
        self.an = math.atan2((event_o.pos[1] - new_ball.y), (event_o.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 5

    def targetting(self, event_o):
        """Прицеливание. Зависит от положения мыши."""
        if event_o:
            if event_o.pos[0] - 20 != 0:
                self.an = math.atan((event_o.pos[1] - 450) / (event_o.pos[0] - 20))
            else:
                self.an = copysign(math.pi / 2, event_o.pos[1] - 450)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        dr.line(self.screen, self.color, (20, 450),
                (20 + math.cos(self.an) * self.f2_power, 450 + math.sin(self.an) * self.f2_power), width=4)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 30:
                self.f2_power += 0.5
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, surface):
        self.points = 0
        self.live = 1
        self.new_target()
        self.screen = surface
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 40)
        self.color = RED
        self.vx = randint(3, 10)
        self.vy = randint(3, 10)

    # FIXME: don't work!!! How to call this functions when object is created?

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 40)

    def hit(self, point=1):
        """Попадание шарика в цель."""
        self.points += point

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        if self.x + self.vx > WIDTH - self.r or self.x + self.vx < self.r:
            self.vx = -self.vx
        if self.y + self.vy > HEIGHT - self.r or self.y + self.vy < self.r:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
targets.append(Target(screen))
targets.append(Target(screen))
finished = False

while not finished:
    clock.tick(FPS)
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.move()
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    survived_balls = []
    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                t.new_target()
        if b.get_life() >= 0:
            survived_balls.append(b)
    balls = survived_balls
    gun.power_up()

pygame.quit()
