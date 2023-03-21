import pygame as pg
from typing import Final
import chess
from CapturedPieceManagementV2 import BLACK_DEFAULT, WHITE_DEFAULT
import Constants
import chess.pgn
from BoardGenerator import BoardGenerator
from Board import Board
from Grabber import Grabber

# Lets define some constants for the size of the board
SQUARE_SIZE: Final[int] = 80

PIECE_OFFSET: Final[int] = (SQUARE_SIZE - Constants.PIECE_SIZE) // 2

BOARD_GEN = BoardGenerator("magnus.pgn")
TEST_BOARDS = BOARD_GEN.get_boards()


class ResetSimulator:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        self.clock = pg.time.Clock()
        self.board = Board()
        self.running = True
        self.currentBoardIndex = 0
        self.grabber = Grabber()
        self.font = pg.font.SysFont("Arial", 20)

    def events(self):
        # We dont have any user input so we just need to make sure we can exit the simulation
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                self.running = False

    # This function will get called 60 times per second
    def update(self):
        # Get all keystrokes
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.currentBoardIndex += 1
            self.board = TEST_BOARDS[self.currentBoardIndex]
        self.grabber.update()

    def draw_board(self):
        # This function will draw the board
        # First we need to draw the squares
        for file in range(8):
            for rank in range(8):
                # Lets get the color of the square
                if (file + rank) % 2 == 0:
                    # The square is white
                    color = (232, 209, 185)
                else:
                    # The square is black
                    color = (156, 106, 91)
                # Lets draw the square
                pg.draw.rect(self.screen, color,
                             (file * SQUARE_SIZE + 3 * SQUARE_SIZE,
                              rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Now we can draw the side areas
        # First we need to draw the white side
        pg.draw.rect(self.screen, (220, 220, 220),
                     (0, 0, 2 * SQUARE_SIZE, 8 * SQUARE_SIZE))
        # Now we can draw the black side
        pg.draw.rect(self.screen, (220, 220, 220),
                     (12 * SQUARE_SIZE, 0, 2 * SQUARE_SIZE, 8 * SQUARE_SIZE))
        # Now we can draw the boxes for the captured pieces
        # First we need to draw the white side
        for i in range(2):
            for j in range(8):
                pg.draw.rect(self.screen, (0, 0, 0),
                             (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE,
                              SQUARE_SIZE), 1)
                # Now we can draw the black side
                pg.draw.rect(self.screen, (0, 0, 0),
                             (12 * SQUARE_SIZE + i * SQUARE_SIZE,
                              j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

        # Now we can draw the pieces
        for file in range(8):
            for rank in range(8):
                # Lets get the piece
                piece = self.board.get_piece(file, rank)
                if piece is not None:
                    self.screen.blit(
                        Constants.PIECE_DICTIONARY[piece.symbol()]["image"],
                        (file * SQUARE_SIZE + 3 * SQUARE_SIZE + PIECE_OFFSET,
                         rank * SQUARE_SIZE + PIECE_OFFSET),
                        (0, 0, SQUARE_SIZE, SQUARE_SIZE))

        # Now we can draw the captured pieces
        for i in range(8):
            for j in range(2):
                b = self.board.get_captured_piece(j, i, "black")
                if b:
                    self.screen.blit(
                        Constants.PIECE_DICTIONARY[BLACK_DEFAULT[i]
                                                   [j]]["image"],
                        (j * SQUARE_SIZE + PIECE_OFFSET, i * SQUARE_SIZE +
                         PIECE_OFFSET, SQUARE_SIZE, SQUARE_SIZE))
                w = self.board.get_captured_piece(j, i, "white")
                if w:
                    self.screen.blit(
                        Constants.PIECE_DICTIONARY[WHITE_DEFAULT[i]
                                                   [j]]["image"],
                        (12 * SQUARE_SIZE + j * SQUARE_SIZE + PIECE_OFFSET,
                         i * SQUARE_SIZE + PIECE_OFFSET, SQUARE_SIZE,
                         SQUARE_SIZE))

    def draw_grabber(self):
        # Draw a rectangle at the grabbers position
        pg.draw.rect(self.screen, (112, 128, 144),
                     (self.grabber.x, self.grabber.y, Constants.SQUARE_SIZE,
                      Constants.SQUARE_SIZE))
        # if the grabber is moving up write up on the grabber
        if self.grabber.vz > 0:
            self.screen.blit(self.font.render("UP", True, (0, 255, 0)),
                             (self.grabber.x, self.grabber.y))
        # if the grabber is moving down write down on the grabber
        elif self.grabber.vz < 0:
            self.screen.blit(self.font.render("Down", True, (255, 0, 0)),
                             (self.grabber.x, self.grabber.y))

    def draw(self):
        # First we want to fill the background
        self.screen.fill((105, 105, 105))
        # Then we can draw the board
        self.draw_board()
        self.draw_grabber()
        # We can draw the fps in the bottom right
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        pg.display.flip()

    def run(self):
        self.board = TEST_BOARDS[0]
        self.grabber.set_target(500, 500)
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()


if __name__ == "__main__":
    rs = ResetSimulator()
    rs.run()
