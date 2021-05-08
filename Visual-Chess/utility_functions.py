import pygame


def scale_image(surface, percent):
    rect = surface.get_rect()
    height = rect[3] - rect[1]
    width = rect[2] - rect[0]

    height = height * percent // 100
    width = width * percent // 100
    return pygame.transform.smoothscale(surface, (width, height))
