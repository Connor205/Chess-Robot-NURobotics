from operator import truediv
from Arduino import Arduino
from GameLogic import GameLogic
import stockfish as sf
import logging
from loggingConstants import handler
import time
import chess


def convertSquareToCoordinates(square: str):
    return [ord(square[0]) - ord('a'), 8 - int(square[1])]


class MovementStockfishPlayers(GameLogic):

    def __init__(self, port) -> None:
        super().__init__()
        self.stockfish = sf.Stockfish()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.arduino = Arduino(port)
        self.logger.info("Waiting For Arduin to be in ready state")
        self.arduino.waitForReady()
        self.board = chess.Board()
        self.logger.info("Stockfish Players Initialized")

    def checkIfSquareIsOccupied(self, position: str):
        return self.board.piece_at(chess.parse_square(
            position.lower())) is not None

    def takePieceOnSquare(self, square):
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(square)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("pickup", [])
        self.arduino.waitForReady()
        self.arduino.sendCommand("remove", [])
        self.arduino.waitForReady()

    def movePieceFromSquareToSquare(self, startSquare, endSquare):
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(startSquare)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("pickup", [])
        self.arduino.waitForReady()
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(endSquare)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("drop", [])
        self.arduino.waitForReady()

    def executeMoveOnArduino(self, move: chess.Move):
        # Need to handle castles and promotions
        startSquare = move.from_square
        endSquare = move.to_square
        self.logger.info("Moving from {} to {}".format(startSquare, endSquare))
        # Assuming move is something like d2d4
        # Lets check for a castle move
        fen = self.getCurretFenString()
        board = chess.Board()
        board.set_fen(fen)
        if startSquare == "e1":
            if board.piece_at(chess.parse_square(startSquare)) is "K":
                if endSquare == "g1":
                    self.logger.info("Castling King Side")
                    self.movePieceFromSquareToSquare("e1", "g1")
                    self.movePieceFromSquareToSquare("h1", "f1")
                elif endSquare == "c1":
                    self.logger.info("Castling Queen Side")
                    self.movePieceFromSquareToSquare("e1", "c1")
                    self.movePieceFromSquareToSquare("a1", "d1")
        if startSquare == "e8":
            if board.piece_at(chess.parse_square(startSquare)) is "k":
                if endSquare == "g8":
                    self.logger.info("Castling King Side")
                    self.movePieceFromSquareToSquare("e8", "g8")
                    self.movePieceFromSquareToSquare("h8", "f8")
                elif endSquare == "c8":
                    self.logger.info("Castling Queen Side")
                    self.movePieceFromSquareToSquare("e8", "c8")
                    self.movePieceFromSquareToSquare("a8", "d8")

        if self.checkIfSquareIsOccupied(endSquare):
            self.takePieceOnSquare(endSquare)
        self.movePieceFromSquareToSquare(startSquare, endSquare)

    def getCurretFenString(self):
        self.logger.debug("Returned Current FEN: {}".format(
            self.stockfish.get_fen_position()))
        return self.stockfish.get_fen_position()

    def getPlayerMove(self) -> str:
        self.logger.info("Player Move Selected: {}".format(
            self.stockfish.get_best_move()))
        startingFen = self.getCurretFenString()
        # Grabbing Move From Stockfish
        move = self.stockfish.get_best_move()
        return move

    def processPlayerMove(self, move):
        self.logger.info("Playing Going to Move: {}".format(move))
        a = input("Click Enter To Being Moving Robot")
        self.executeMoveOnArduino(move)
        self.stockfish.make_moves_from_current_position([move])
        return True

    def generateComputerMove(self) -> str:
        return self.stockfish.get_best_move()

    def makeComputerMove(self, move) -> bool:
        self.logger.info("Computer Going To Move: {}".format(move))
        a = input("Click Enter To Being Moving Robot")
        self.executeMoveOnArduino(move)
        self.stockfish.make_moves_from_current_position([move])
        return True

    def getLogicName(self):
        return "Stockfish V Stockfish with Arduino"
