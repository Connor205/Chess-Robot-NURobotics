import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame.locals import *
from GameLogic import GameLogic
from BasicStockfishPlayers import BasicStockfishPlayers
import logging
from loggingConstants import formatter, handler
from Constants import *

RED = (255, 0, 0)
# Lets go ahead and grab the logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

frame = 0

# Initialize pygame
pg.init()
logger.info('Initialized pygame')

g = BasicStockfishPlayers()
logger.info('Initialized GameLogic: {}'.format(g.getLogicName()))

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pg.font.SysFont(None, 24)

# Variable to keep the main loop running
running = True
playerMove = True
currentFenString = g.getCurretFenString()
board = pg.Surface((BOARD_WIDTH, BOARD_HEIGHT))
board.fill((255, 255, 255))
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        pg.draw.rect(
            board, color,
            (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

modifiedFen = currentFenString.replace(' ', '/', 1)
ranks = currentFenString.split('/')
ranks = ranks[0:8]
for rankI, rank in enumerate(ranks):
    file = 0
    index = 0
    while file < 8:
        char = rank[index]
        if char.isdigit():
            file += int(char)
        else:
            board.blit(PIECE_DICTIONARY[char]['image'],
                       (file * SQUARE_SIZE, rankI * SQUARE_SIZE))
            file += 1
        index += 1


def isEventPlayerSwitch(event):
    return event.type == pg.KEYDOWN and event.key == pg.K_SPACE


# Main loop
# This loop garners everything
while running:
    # We need to get a list of all the things that have happened
    # since the last time we checked
    events = pg.event.get()
    newBoardRender = False
    # # wait for user to press button
    if playerMove:
        # We go ahead and wait for the user to press the button on screen, but we do not block since everything needs to run in parallel
        if any([isEventPlayerSwitch(event) for event in events]):
            # Takes care of validating moves
            validMove = False
            while not validMove:
                move = g.getPlayerMove()
                validMove = g.processPlayerMove(move)
            currentFenString = g.getCurretFenString()
            playerMove = False
            logger.info("Finished Player Move")
            newBoardRender = True
    else:
        # We can go ahead and generate our move
        move = g.generateComputerMove()
        g.makeComputerMove(move)
        currentFenString = g.getCurretFenString()
        newBoardRender = True
        playerMove = True

    if newBoardRender:
        board = pg.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        board.fill((255, 255, 255))
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                pg.draw.rect(board, color, (i * SQUARE_SIZE, j * SQUARE_SIZE,
                                            SQUARE_SIZE, SQUARE_SIZE))

        modifiedFen = currentFenString.replace(' ', '/', 1)
        ranks = currentFenString.split('/')
        ranks = ranks[0:8]
        for rankI, rank in enumerate(ranks):
            file = 0
            index = 0
            while file < 8:
                char = rank[index]
                if char.isdigit():
                    file += int(char)
                else:
                    board.blit(PIECE_DICTIONARY[char]['image'],
                               (file * SQUARE_SIZE, rankI * SQUARE_SIZE))
                    file += 1
                index += 1
        logger.info("Finished board render")

    screen.blit(board, (0, 0))

    img = font.render(str(frame), True, RED)
    screen.blit(img, (20, 20))
    pg.display.flip()
    if newBoardRender:
        logger.info("Finished board flip on newBoardRender")

    # Lets think about the initial game loop
    # We need to know whose turn it is
    # Then we are either waiting for the user to make their move, or the computer is making its move
    # The player making a move goes as such: Computer informs player it is making a move, player moves pieces, player presses button, computer deciphers the move, computer updates current stockfish instance
    # The computer making its move breaks down into: Computer decides move, Computer creates robot motions, computer pushes them to arduino in sequence, computer returns motors to calibration point, computer "clicks button"
    # This happens over and over again until one player is the victor
    # We can update the game every tick with a clock, then we need to have the board display the current fen string as reported by stockfish
    # It really isn't that unique, but since we will need to be procesing using input and displaying the time on the screen we wil need to maintain some sort of state machine that garners the current state of the entire system. This state machine will rely on a huge number of factors but generally follow the path above. There are some wacky edge cases taht will need to be hard coded. We can pretty much define an interface so to speak that will allow us to generate whatever agents we would like.

    # Look at every event in the queue
    for event in events:
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    frame += 1