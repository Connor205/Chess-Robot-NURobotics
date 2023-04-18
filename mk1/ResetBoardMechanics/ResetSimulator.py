import pygame as pg
from typing import Final
import chess
from CapturedPieceManagementV2 import BLACK_DEFAULT, WHITE_DEFAULT
import Constants
import chess.pgn
from BoardGenerator import BoardGenerator
from Board import Board
from Grabber import Grabber
from ResetMoves import VerticalMove, HorizontalMove, PieceMove
from ResetMoveGenerator import generateAllResetMoves
import random
from ResetAgent import ClosestAgent, AStartAgent, FeatureAgent

# Lets define some constants for the size of the board
SQUARE_SIZE: Final[int] = 80

PIECE_OFFSET: Final[int] = (SQUARE_SIZE - Constants.PIECE_SIZE) // 2

BOARD_GEN = BoardGenerator("magnus.pgn")
TEST_BOARDS = BOARD_GEN.get_boards()
EDITABLE_BOARDS = BOARD_GEN.get_boards()


def square_from_xy(x: int, y: int):
    return chess.square(x - 3, y)


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

        self.currentMove = None
        self.currentPosition = None
        self.heldPiece = ""

    def events(self):
        # We dont have any user input so we just need to make sure we can exit the simulation
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                self.running = False

    # This function will get called 60 times per second
    def update(self):
        # Get all keystrokes
        # keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]:
        #     self.currentBoardIndex += 1
        #     self.board = TEST_BOARDS[self.currentBoardIndex]
        self.grabber.update()
        if not self.grabber.in_motion():
            if self.currentMove is not None and self.currentMove.isHorizontal(
            ):
                self.currentPosition = self.currentMove.end
            # We want to consume the next event
            if len(self.moves) > 0:
                self.currentMove = self.moves.pop(0)
                print(f"Current Move: {self.currentMove}")
                if self.currentMove.isHorizontal():
                    self.grabber.set_target(
                        self.currentMove.end[1] * SQUARE_SIZE,
                        self.currentMove.end[0] * SQUARE_SIZE)
                if self.currentMove.isPiece():
                    if self.currentMove.isPlace():
                        print(
                            f"Attempting to Place a -{self.heldPiece}- at: x: {self.currentPosition[1]}, y: {self.currentPosition[0]},"
                        )
                        self.board.set_square(
                            square_from_xy(self.currentPosition[1],
                                           self.currentPosition[0]),
                            self.heldPiece)
                    if self.currentMove.isPickup():
                        self.heldPiece = self.board.remove_piece(
                            self.currentPosition[1], self.currentPosition[0])
                if self.currentMove.isVertical():
                    if self.currentMove.direction == "up":
                        self.grabber.set_vertical_target(100)
                    if self.currentMove.direction == "down":
                        self.grabber.set_vertical_target(0)
            else:
                self.moves = self.resetMovements.pop(0)._moves
                print(f"Added Moves: {self.moves}")

    def draw_board(self):
        # This function will draw the board
        # First we need to draw the squares
        for file in range(8):
            for rank in range(8):
                # Lets get the color of the square
                if (file + rank) % 2 == 1:
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
        if self.grabber.vz == 0:
            color = (112, 128, 144)
        elif self.grabber.vz > 0:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pg.draw.rect(
            self.screen, color,
            (self.grabber.x, self.grabber.y, SQUARE_SIZE, SQUARE_SIZE))
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

        if not self.heldPiece == "":
            self.screen.blit(
                Constants.PIECE_DICTIONARY[self.heldPiece]["image"],
                (600, 700), (0, 0, SQUARE_SIZE, SQUARE_SIZE))
        else:
            pg.draw.rect(
                self.screen,
                (105, 105, 105),
                (600, 700, SQUARE_SIZE, SQUARE_SIZE),
            )
        # We can draw some text to show the current move
        self.screen.blit(self.font.render(f"Current Piece: ", True, (0, 0, 0)),
                         (475, 720))
        # We can draw the fps in the bottom right
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        pg.display.flip()

    def run(self):
        self.board = TEST_BOARDS[0]
        agent = FeatureAgent(
            EDITABLE_BOARDS[0],
            [-2.0155024622168303, 0.79, -1.67, 0.2025769406194175, -1.4])
        self.resetMovements = agent.generateSeriesOfResetMoves()
        self.moves = []
        while self.running:
            self.clock.tick(240)
            self.events()
            self.update()
            self.draw()


if __name__ == "__main__":
    rs = ResetSimulator()
    rs.run()
