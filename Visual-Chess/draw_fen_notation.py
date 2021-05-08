""" The goal of this file will be to draw a basic chess board based on a FEN notation. 
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
width = height = 700

pygame.init()

size = (width, height)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess Position")

done = False

clock = pygame.time.Clock()

while not done:
    # Deals with closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            done = True

    # Draw the background(also overwrites all of the previous)
    screen.fill(WHITE)

    clock.tick(60)
    # This guy actually draws the screen
    pygame.display.flip()

pygame.quit()
