import pygame
import pygame.draw as dr
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (104, 102, 103)
DARK_GRAY = (86, 76, 70)
WHITE_GRAY = (160, 160, 160)
GREEN = (32, 153, 82)
YELLOW = (206, 156, 30)
RED = (212, 50, 19)
BROWN = (63, 45, 31)
ORANGE = (227, 133, 13)

WIDTH = 1

IGLA_COORDINATES = (
    (500, 720, 510, 721, 70),
    (510, 721, 520, 722, 70),
    (520, 722, 530, 724, 70),
    (530, 724, 540, 726, 70),
    (540, 726, 550, 729, 70),
    (490, 721, 500, 720, 70),
    (480, 722, 490, 721, 70),
    (475, 721, 480, 722, 70),
    (465, 722, 470, 721, 70),
    (455, 721, 460, 722, 70),
    (445, 722, 450, 721, 70),
    (435, 721, 440, 722, 70),
    (425, 721, 430, 722, 64),
    (415, 722, 420, 720, 70),
    (405, 720, 410, 722, 66),
    (395, 720, 400, 721, 69),
    (385, 721, 390, 723, 70),
    (375, 721, 380, 722, 64),
    (365, 722, 370, 720, 70),
    (355, 720, 360, 722, 66),
    (345, 720, 350, 721, 69),
    (335, 721, 340, 723, 70),
    (492, 762, 498, 764, 57),
    (412, 767, 417, 765, 82),
    (341, 762, 351, 764, 53),
    (410, 737, 416, 738, 71),
    (458, 722, 465, 723, 56),
    (529, 741, 538, 743, 64),
    (344, 734, 349, 737, 83),
    (520, 736, 526, 737, 61),
    (446, 758, 456, 756, 83),
    (405, 740, 414, 737, 74),
    (470, 763, 479, 765, 66),
    (460, 724, 466, 725, 81),
    (412, 757, 420, 758, 73),
    (369, 722, 379, 724, 82),
    (327, 759, 337, 756, 66),
    (324, 757, 334, 758, 80),
    (336, 763, 343, 760, 86),
    (396, 749, 406, 752, 78),
    (360, 732, 369, 735, 90),
    (394, 769, 402, 772, 62),
    (356, 760, 362, 759, 90),
    (405, 732, 415, 730, 66),
    (385, 765, 391, 762, 89),
    (379, 722, 389, 723, 57),
    (450, 753, 457, 755, 57),
    (460, 755, 469, 753, 77),
    (339, 733, 349, 735, 51),
    (381, 730, 386, 731, 61),
    (366, 740, 372, 738, 53),
    (483, 749, 488, 750, 52),
    (462, 739, 470, 737, 57),
    (414, 736, 423, 739, 50),
    (492, 753, 502, 750, 83),
    (474, 759, 482, 762, 59),
    (512, 732, 520, 731, 58),
    (424, 735, 429, 737, 77),
    (397, 753, 406, 755, 81),
    (346, 747, 351, 749, 64),
    (506, 732, 514, 735, 68),
    (373, 742, 382, 745, 50),
    (435, 742, 445, 745, 54),
    (330, 760, 337, 763, 84),
    (501, 746, 511, 749, 74),
    (422, 742, 429, 745, 57),
    (459, 748, 467, 749, 56),
    (382, 743, 390, 741, 60),
    (457, 732, 467, 733, 50),
    (412, 742, 420, 745, 83),
    (391, 761, 401, 758, 80),
    (472, 757, 482, 755, 73),
    (481, 736, 486, 737, 53),
    (326, 766, 331, 763, 62),
    (510, 758, 515, 761, 78),
    (444, 741, 453, 743, 85),
    (396, 735, 405, 737, 50),
    (394, 736, 403, 739, 90),
    (412, 765, 422, 767, 81),
    (398, 729, 403, 728, 72),
    (451, 740, 456, 738, 63),
    (329, 757, 337, 759, 77),
    (366, 757, 375, 756, 72),
    (382, 758, 387, 760, 79),
    (383, 748, 390, 745, 83),
    (524, 749, 533, 751, 67),
    (397, 741, 403, 742, 58),
    (378, 734, 383, 736, 65),
    (328, 726, 334, 725, 82),
    (524, 752, 534, 754, 80),
    (462, 742, 470, 745, 85),
    (438, 741, 444, 744, 81),
    (343, 755, 350, 756, 56),
    (509, 759, 515, 761, 65),
    (442, 735, 447, 738, 87),
    (378, 757, 386, 754, 73),
    (487, 764, 492, 765, 73),
    (465, 747, 471, 750, 78),
    (395, 756, 402, 759, 85),
    (424, 770, 431, 772, 52),
    (378, 768, 384, 769, 67),
    (456, 770, 464, 767, 77),
    (424, 758, 434, 761, 62),
    (472, 750, 479, 749, 64),
    (496, 755, 503, 757, 88),
    (437, 753, 442, 756, 67),
    (506, 750, 515, 751, 64),
    (480, 753, 489, 752, 51),
    (363, 736, 368, 733, 54),
    (502, 752, 512, 749, 53),
    (453, 725, 463, 728, 84),
    (408, 726, 413, 729, 68),
    (533, 774, 543, 777, 81),
    (380, 780, 385, 783, 80),
    (381, 774, 390, 772, 51),
    (529, 780, 534, 778, 80),
    (348, 776, 353, 778, 50),
    (418, 785, 426, 782, 56),
    (344, 773, 349, 770, 80),
    (529, 781, 538, 779, 65),
    (467, 781, 472, 779, 59),
    (466, 783, 474, 784, 57),
    (463, 780, 468, 778, 51),
    (341, 775, 349, 778, 80),
    (404, 771, 409, 774, 66),
    (440, 780, 448, 779, 83),
    (504, 771, 511, 773, 88),
    (391, 782, 398, 784, 77),
    (440, 775, 445, 776, 70),
    (431, 776, 438, 774, 62),
    (487, 784, 492, 787, 51),
    (516, 771, 524, 772, 85),
    (458, 776, 464, 779, 83),
    (344, 776, 349, 774, 66),
    (377, 775, 385, 774, 86),
    (447, 774, 455, 771, 80),
    (453, 778, 462, 781, 70),
    (330, 774, 338, 775, 53),
    (389, 780, 399, 783, 79),
    (423, 773, 430, 776, 90),
    (481, 774, 487, 776, 55),
    (512, 775, 517, 778, 65),
    (368, 778, 377, 776, 77),
    (497, 783, 504, 786, 80),
    (514, 775, 524, 776, 85),
    (356, 772, 361, 770, 52),
    (400, 785, 406, 788, 57),
    (430, 775, 436, 777, 90),
    (521, 774, 528, 776, 62),
    (528, 772, 538, 771, 71),
    (417, 786, 425, 789, 59),
    (478, 774, 484, 773, 59),
    (459, 781, 466, 784, 87),
    (347, 775, 355, 772, 75),
    (395, 783, 405, 780, 62),
    (422, 777, 427, 774, 86),
    (344, 782, 352, 779, 70),
    (415, 785, 424, 786, 79),
    (419, 777, 426, 775, 82),
    (527, 772, 532, 775, 59),
    (473, 778, 482, 775, 90),
    (509, 773, 518, 775, 51),
    (356, 780, 364, 781, 90),
    (376, 771, 385, 772, 70),
    (364, 779, 370, 782, 50),
    (535, 771, 543, 772, 61),
    (352, 772, 357, 774, 71),
    (434, 775, 440, 777, 53),
    (340, 771, 350, 773, 72),
    (379, 774, 386, 775, 57),
    (447, 777, 453, 778, 59),
    (429, 784, 434, 785, 80),
    (356, 774, 364, 777, 78),
    (514, 778, 523, 776, 68),
    (508, 776, 518, 778, 80),
    (462, 770, 470, 772, 63),
    (403, 777, 408, 780, 85),
    (442, 785, 450, 788, 88),
    (398, 777, 403, 780, 72),
    (331, 776, 340, 779, 60),
    (357, 783, 363, 784, 87),
    (359, 772, 364, 771, 89),
    (367, 777, 375, 779, 67),
    (360, 775, 367, 774, 86),
    (365, 781, 373, 784, 62),
    (473, 783, 482, 782, 52),
    (534, 786, 540, 785, 55),
    (491, 781, 496, 782, 52),
    (363, 779, 373, 778, 51),
    (507, 782, 513, 779, 53),
    (511, 771, 519, 773, 76),
    (466, 786, 476, 785, 52),
    (496, 782, 504, 783, 69),
    (440, 775, 445, 777, 65),
    (497, 773, 503, 776, 50),
    (413, 776, 418, 778, 82),
    (501, 771, 509, 769, 85),
    (441, 777, 449, 776, 80),
    (432, 771, 441, 773, 71),
    (450, 785, 456, 787, 61),
    (496, 778, 505, 779, 53),
    (441, 776, 447, 773, 71)
)

HEDGEHOG_COORDINATES = (
    (310, 700, 260, 100),
    (300, 760, 32, 17),
    (330, 780, 30, 15),
    (520, 780, 30, 15),
    (545, 760, 25, 15),
    (540, 730, 50, 30),
    (589, 744, 5, 5),
    (570, 730, 7, 7),
    (560, 740, 7, 7),
    (470, 670, 50, 50),
    (340, 680, 50, 50),
    (320, 685, 50, 50)
)


# Та же функция
def draw_mukhomor(x, y, lx, ly, angle, screen):
    """
    draws mushroom with (x, y) coordinate with lx and ly size
    :param x: x-coordinate of mushroom
    :param y: y-coordinate of mushroom
    :param lx: x-size of mushroom
    :param ly: y-size of mushroom
    :param angle:
    :param screen:
    :return:
    """
    shape_surf = pygame.Surface([max(lx, ly), max(lx, ly)], pygame.SRCALPHA)

    dr.ellipse(shape_surf, WHITE_GRAY, [lx / 2 - ly / 2, 0, ly, lx])
    dr.ellipse(shape_surf, LIGHT_GRAY, (lx / 2 - ly / 2, 0, ly, lx), width=WIDTH)
    dr.ellipse(shape_surf, RED, [0, 0, lx, ly])
    dr.ellipse(shape_surf, LIGHT_GRAY, (0, 0, lx, ly), width=WIDTH)
    dr.ellipse(shape_surf, WHITE, [lx / 4, ly / 4, lx / 8, ly / 6])
    dr.ellipse(shape_surf, WHITE, [lx / 2, ly / 3, lx / 6, ly / 7])
    dr.ellipse(shape_surf, WHITE, [3 * lx / 4, ly / 4, lx / 6, ly / 7])

    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    screen.blit(rotated_surf, (x, y))


def needle(x1, y1, x2, y2, l, screen_canvas):
    """
    draws needle as triangle for hedgehog
    :param x1: x-coordinate of 1st dot of triangle
    :param y1: y-coordinate of 1st dot of triangle
    :param x2: x-coordinate of 2nd dot of triangle
    :param y2: y-coordinate of 2nd dot of triangle
    :param l: height of triangle
    :param screen_canvas:
    :return:
    """
    k = (y2 - y1) / (x2 - x1)
    x3 = (x1 + x2) / 2 - l * math.copysign(1, - 1 / k) * math.cos(math.atan((-1 / k)))
    y3 = y1 - (x2 - x1) / 2 * k - abs(l * math.sin(math.atan(abs(-1 / k))))

    dr.polygon(screen_canvas, (44, 20, 26), ((x1, y1), (x2, y2), (x3, y3)))
    dr.polygon(screen_canvas, (0, 0, 0), ((x1, y1), (x2, y2), (x3, y3)), width=WIDTH)


def draw_hedgehog(x, y, lx, ly, canvas):
    """
    draws hedgehog
    :param x: x-coordinate of hedgehog
    :param y: y-coordinate of hedgehog
    :param lx: x-size of hedgehog
    :param ly: y-size of hedgehog
    :param canvas:
    :return:
    """
    screen = pygame.Surface([650, 900], pygame.SRCALPHA)
    shape_chop = pygame.Surface([300, 200], pygame.SRCALPHA)

    for coordinate in HEDGEHOG_COORDINATES[:7]:
        dr.ellipse(screen, BROWN, coordinate)
        dr.ellipse(screen, LIGHT_GRAY, coordinate, width=WIDTH)

    for coordinate in HEDGEHOG_COORDINATES[7:9]:
        dr.ellipse(screen, BLACK, coordinate)
        dr.ellipse(screen, LIGHT_GRAY, coordinate, width=WIDTH)

    for coordinate in IGLA_COORDINATES[:113]:
        needle(coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], screen)

    draw_mukhomor(380, 650, 70, 30, -25, screen)

    dr.ellipse(screen, RED, HEDGEHOG_COORDINATES[9])
    dr.ellipse(screen, LIGHT_GRAY, HEDGEHOG_COORDINATES[9], width=WIDTH)

    for coordinate in HEDGEHOG_COORDINATES[10:]:
        dr.ellipse(screen, ORANGE, coordinate)
        dr.ellipse(screen, LIGHT_GRAY, coordinate, width=WIDTH)

    for coordinate in IGLA_COORDINATES[113:]:
        needle(coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], screen)

    shape_chop.blit(screen, area=[300, 600, 300, 200], dest=[0, 0])
    shape_scaled = pygame.transform.scale(shape_chop, [lx, ly])
    canvas.blit(shape_scaled, area=[0, 0, 300, 200], dest=[x, y])


def draw_tree(x1, y1, x2, y2):
    """
    draws tree trunk through two dots (x1, y1) and (x1+x2, y1+y2)
    :param x1: x-coordinate of dot (x1, y1)
    :param y1: y-coordinate of dot (x1, y1)
    :param x2: width
    :param y2: height
    :return:
    """
    dr.rect(screen1, YELLOW, (x1, y1, x2, y2))
    dr.rect(screen1, LIGHT_GRAY, (x1, y1, x2, y2), width=WIDTH)


# Фон
def draw_background():
    """
    draws background
    :return:
    """
    dr.rect(screen1, GREEN, (0, 0, 650, 550))
    dr.rect(screen1, LIGHT_GRAY, (0, 0, 650, 550), width=WIDTH)
    dr.rect(screen1, DARK_GRAY, (0, 550, 650, 350))
    dr.rect(screen1, LIGHT_GRAY, (0, 550, 650, 350), width=WIDTH)


pygame.init()

FPS = 30

screen1 = pygame.display.set_mode((650, 900))

draw_background()

draw_hedgehog(500, 450, 250, 150, screen1)
draw_hedgehog(110, 460, 250, 150, screen1)
draw_tree(0, 0, 50, 600)
draw_tree(90, 0, 150, 850)
draw_hedgehog(310, 600, 300, 200, screen1)
draw_hedgehog(-100, 700, 250, 150, screen1)
draw_tree(470, 0, 50, 600)
draw_tree(590, 0, 40, 700)

draw_mukhomor(270, 800, 140, 30, 0, screen1)
draw_mukhomor(370, 840, 80, 17, 0, screen1)
draw_mukhomor(470, 810, 130, 30, -10, screen1)
draw_mukhomor(540, 800, 140, 30, 20, screen1)
draw_mukhomor(440, 845, 90, 21, 7, screen1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
