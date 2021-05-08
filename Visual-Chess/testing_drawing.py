# This file is to be used for testing the sprite sheet and drawing onto a basic pygame

import pygame
import piece

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
(w, h) = size = (1000, 1000)

pygame.init()


def scale_image(surface, percent):
    rect = surface.get_rect()
    height = rect[3] - rect[1]
    width = rect[2] - rect[0]

    height = height * percent // 100
    width = width * percent // 100
    return pygame.transform.smoothscale(surface, (width, height))


screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess Position")
board = pygame.transform.smoothscale(
    pygame.image.load("chess_sprites/board.png"), size)
king = pygame.image.load("chess_sprites/b_queen.png")
king = scale_image(king, 90)
image_rect = king.get_rect()
image_rect.centerx = 62.5 * 5
image_rect.centery = 62.5
print(image_rect)

#image = pygame.image.load("chess_pieces_no_background.png").convert_alpha()

done = False

clock = pygame.time.Clock()

while not done:
    # Deals with closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            done = True

    screen.fill(WHITE)
    # Draw the background(also overwrites all of the previous)
    # pygame.draw.rect(screen, RED, [55, 50, 20, 25])
    screen.blit(board, (0, 0))
    screen.blit(king, image_rect)

    clock.tick(60)

    # This guy actually draws the screen
    pygame.display.flip()
