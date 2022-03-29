from random import randint
import pygame.draw as dr
import pygame.surface
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
        self.height = 30
        self.width = 50
        self.r = 10
        self.caliber = 3
        self.color = GREEN
        self.f2_on = 0

    def draw(self):
        dr.polygon(self.surface, self.color, [(self.x - self.width / 2, self.y - self.height / 2),
                                         (self.x + self.width / 2, self.y - self.height / 2),
                                         (self.x + self.width / 2, self.y + self.height / 2),
                                         (self.x - self.width / 2, self.y + self.height / 2),
                                         (self.x - self.width / 2, self.y - self.height / 2)])
        dr.circle(self.surface,self.color, (self.x, self.y + self.height / 2), self.width / 4)
        dr.line(self.surface, BLACK, (self.x, self.y + self.height / 2),
                (self.x + math.cos(self.fire_angle) * self.width / 2, self.y + self.height / 2), width=self.caliber)

    def fire2_start(self):
        self.f2_on = 1

    def targetting(self, event_o):
        """Прицеливание. Зависит от положения мыши."""
        if event_o:
            if event_o.pos[0] - 20 != 0:
                self.fire_angle = math.atan((event_o.pos[1] - 450) / (event_o.pos[0] - 20))
            else:
                self.fire_angle = math.copysign(math.pi / 2, event_o.pos[1] - 450)
