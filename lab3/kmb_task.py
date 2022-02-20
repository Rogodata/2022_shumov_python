import pygame
import pygame.draw as dr
import math
from random import randint


def igla(x1, y1, x2, y2, l, screen_canvas):
    k = (y2 - y1) / (x2 - x1)
    dr.polygon(screen_canvas, (44, 20, 26), [(x1, y1), (x2, y2),
                                             ((x1 + x2) / 2 - l * math.copysign(1, - 1 / k) * math.cos(
                                                 math.atan((-1 / k))),
                                              y1 - (x2 - x1) / 2 * k - abs(l * math.sin(math.atan(abs(-1 / k))))),
                                             (x1, y1)])
    dr.polygon(screen_canvas, (0, 0, 0), [(x1, y1), (x2, y2),
                                          (
                                              (x1 + x2) / 2 - l * math.copysign(1, - 1 / k) * math.cos(
                                                  math.atan((-1 / k))),
                                              y1 - (x2 - x1) / 2 * k - abs(l * math.sin(math.atan(abs(-1 / k))))),
                                          (x1, y1)],
               width=1)


pygame.init()

FPS = 30
screen = pygame.display.set_mode((650, 900))

dr.rect(screen, (32, 153, 82), (0, 0, 650, 550))
dr.rect(screen, (86, 76, 70), (0, 550, 650, 350))
dr.rect(screen, (206, 156, 30), (0, 0, 50, 600))
dr.rect(screen, (206, 156, 30), (90, 0, 150, 850))
dr.rect(screen, (206, 156, 30), (470, 0, 50, 600))
dr.rect(screen, (206, 156, 30), (590, 0, 40, 700))
dr.ellipse(screen, (63, 45, 31), (310, 700, 260, 100))
dr.ellipse(screen, (104, 102, 103), (310, 700, 260, 100), width=1)
dr.ellipse(screen, (63, 45, 31), (300, 760, 32, 17))
dr.ellipse(screen, (104, 102, 103), (300, 760, 32, 17), width=1)
dr.ellipse(screen, (63, 45, 31), (330, 780, 30, 15))
dr.ellipse(screen, (104, 102, 103), (330, 780, 30, 15), width=1)
dr.ellipse(screen, (63, 45, 31), (520, 780, 30, 15))
dr.ellipse(screen, (104, 102, 103), (520, 780, 30, 15), width=1)
dr.ellipse(screen, (63, 45, 31), (545, 760, 25, 15))
dr.ellipse(screen, (104, 102, 103), (545, 760, 25, 15), width=1)
dr.ellipse(screen, (63, 45, 31), (540, 730, 50, 30))
dr.ellipse(screen, (104, 102, 103), (540, 730, 50, 30), width=1)
dr.ellipse(screen, (63, 45, 31), (589, 744, 5, 5))
dr.ellipse(screen, (104, 102, 103), (589, 744, 5, 5), width=1)
dr.ellipse(screen, (0, 0, 0), (560, 730, 7, 7))
dr.ellipse(screen, (104, 102, 103), (560, 730, 7, 7), width=1)
dr.ellipse(screen, (0, 0, 0), (550, 740, 7, 7))
dr.ellipse(screen, (104, 102, 103), (550, 740, 7, 7), width=1)
igla(500, 720, 510, 721, 70, screen)
igla(510, 721, 520, 722, 70, screen)
igla(520, 722, 530, 724, 70, screen)
igla(530, 724, 540, 726, 70, screen)
igla(540, 726, 550, 729, 70, screen)
igla(490, 721, 500, 720, 70, screen)
igla(480, 722, 490, 721, 70, screen)
igla(475, 721, 480, 722, 70, screen)
igla(465, 722, 470, 721, 70, screen)
igla(455, 721, 460, 722, 70, screen)
igla(445, 722, 450, 721, 70, screen)
igla(435, 721, 440, 722, 70, screen)
igla(425, 721, 430, 722, 64, screen)
igla(415, 722, 420, 720, 70, screen)
igla(405, 720, 410, 722, 66, screen)
igla(395, 720, 400, 721, 69, screen)
igla(385, 721, 390, 723, 70, screen)
igla(375, 721, 380, 722, 64, screen)
igla(365, 722, 370, 720, 70, screen)
igla(355, 720, 360, 722, 66, screen)
igla(345, 720, 350, 721, 69, screen)
igla(335, 721, 340, 723, 70, screen)

for i in range(100):
    x1 = randint(310, 550)
    y1 = randint(710, 760)
    igla(x1, y1, randint(x1 + 5, x1 + 10), y1 + int(math.copysign(randint(1, 3), randint(-1, 1))), randint(50, 90),
         screen)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
