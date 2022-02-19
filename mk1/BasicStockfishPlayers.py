from operator import truediv
from GameLogic import GameLogic
import stockfish as sf
import logging
from loggingConstants import handler
import time


class BasicStockfishPlayers(GameLogic):

    def __init__(self) -> None:
        super().__init__()
        self.stockfish = sf.Stockfish()
        self.stockfish.set_fen_position(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Stockfish Players Initialized")

    def getCurretFenString(self):
        self.logger.debug("Returned Current FEN: {}".format(
            self.stockfish.get_fen_position()))
        return self.stockfish.get_fen_position()

    def getPlayerMove(self) -> str:
        self.logger.info("Best Moves: {}".format(
            self.stockfish.get_best_move()))
        startingFen = self.getCurretFenString()
        move = input("Enter your move: ")
        self.logger.info("Player move: {}".format(move))
        # move = self.stockfish.get_best_move()
        return move

    def processPlayerMove(self, move):
        previousPos = self.stockfish.get_fen_position()

        self.stockfish.make_moves_from_current_position([move])
        newPos = self.stockfish.get_fen_position()
        if newPos == previousPos:
            self.logger.error("Invalid Move: {}".format(move))
            return False
        return True

    def generateComputerMove(self) -> str:
        return self.stockfish.get_best_move()

    def makeComputerMove(self, move) -> bool:
        time.sleep(2)
        self.logger.info("Computer moved: {}".format(move))
        self.stockfish.make_moves_from_current_position([move])
        return True

    def getLogicName(self):
        return "Basic Stockfish Players"
