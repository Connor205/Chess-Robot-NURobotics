import pygame
import piece
import chess_game

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
(w, h) = size = (1000, 1000)

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess Position")
board = pygame.transform.smoothscale(
    pygame.image.load("chess_sprites/board.png"), size)

game = chess_game.Chess_Game(screen)

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
    game.blitme()

    clock.tick(60)

    # This guy actually draws the screen
    pygame.display.flip()
