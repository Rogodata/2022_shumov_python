import pygame
import pygame.draw as dr

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

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
