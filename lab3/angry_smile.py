import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

dr.circle(screen, (180, 180, 0), (200, 200), 200)
dr.circle(screen, (180, 0, 0), (100, 130), 50)
dr.circle(screen, (180, 0, 0), (300, 130), 40)
dr.circle(screen, (0, 0, 0), (100, 130), 20)
dr.circle(screen, (0, 0, 0), (300, 130), 15)
dr.rect(screen, (0, 0, 0), (50, 220, 300, 40))
dr.polygon(screen, (0, 0, 0), [(200, 100), (200, 70),
                               (330, 20), (330, 40), (200, 100)])
dr.polygon(screen, (0, 0, 0), [(200, 100), (200, 70),
                               (70, 20), (70, 40), (200, 100)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
