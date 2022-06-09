from Arduino import Arduino
from GameLogic import GameLogic
import stockfish as sf
import logging
from loggingConstants import handler
import time
import chess
from visionUtilities import save_split_images, get_perspective_image_gray, split_image_into_squares, save_image


def convertSquareToCoordinates(square: str):
    return [ord(square[0]) - ord('a'), 8 - int(square[1])]


class PlayerVStockfishManual(GameLogic):

    def __init__(self, port, rating=800) -> None:
        super().__init__()
        self.stockfish = sf.Stockfish()
        self.stockfish.set_elo_rating(rating)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Stockfish Players Initialized")
        self.arduino = Arduino(port)
        self.logger.info("Waiting For Arduin to be in ready state")
        self.arduino.waitForReady()
        self.board = chess.Board()
        self.board.set_fen(
            "r1bqkbnr/pp1p1ppp/2n5/2p1p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR")
        self.stockfish.set_fen_position(self.board.fen())

    def checkIfSquareIsOccupied(self, position: str):
        fen = self.getCurretFenString()
        board = chess.Board()
        board.set_fen(fen)
        return board.piece_at(chess.parse_square(position.lower())) is not None

    def takePieceOnSquare(self, square: str):
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(square)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("pickup", [])
        self.arduino.waitForReady()
        # TODO:: Needs to get updated with the whole taking onto a specific square
        self.arduino.sendCommand("remove", [])
        self.arduino.waitForReady()

    def movePieceFromSquareToSquare(self, startSquare, endSquare):
        startCoords = convertSquareToCoordinates(startSquare)
        endCoords = convertSquareToCoordinates(endSquare)
        # if start or end is the same then we dont need to lift all the way
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(startSquare)])
        self.arduino.waitForReady()
        if startCoords[0] == endCoords[0] or startCoords[1] == endCoords[1]:
            self.arduino.sendCommand("smallPickup", [])
        else:
            self.arduino.sendCommand("pickup", [])
        self.arduino.waitForReady()
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(endSquare)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("drop", [])
        self.arduino.waitForReady()

    def executeMoveOnArduino(self, move):
        m = self.board.parse_uci(move)
        if self.board.is_castling(m):
            print("CASTLING MOVE")
            if m.from_square == chess.E1:
                if m.to_square == chess.G1:
                    self.movePieceFromSquareToSquare("e1", "g1")
                    self.movePieceFromSquareToSquare("h1", "f1")
                elif m.to_square == chess.C1:
                    self.movePieceFromSquareToSquare("e1", "c1")
                    self.movePieceFromSquareToSquare("a1", "d1")
            elif m.from_square == chess.E8:
                if m.to_square == chess.G8:
                    self.movePieceFromSquareToSquare("e8", "g8")
                    self.movePieceFromSquareToSquare("h8", "f8")
                elif m.to_square == chess.C8:
                    self.movePieceFromSquareToSquare("e8", "c8")
                    self.movePieceFromSquareToSquare("a8", "d8")
            return
        if self.board.is_en_passant(m):
            print("EN PASSANT MOVE")
            if chess.square_rank(m.to_square) == 2:
                self.takePieceOnSquare(chess.square_name(m.to_square + 8))
            if chess.square_rank(m.to_square) == 5:
                self.takePieceOnSquare(chess.square_name(m.to_square - 8))
            self.movePieceFromSquareToSquare(chess.square_name(m.from_square),
                                             chess.square_name(m.to_square))

            return

        startSquare = move[0:2]
        endSquare = move[2:4]
        self.logger.info("Moving from {} to {}".format(startSquare, endSquare))
        if self.checkIfSquareIsOccupied(endSquare):
            self.takePieceOnSquare(endSquare)
        self.movePieceFromSquareToSquare(startSquare, endSquare)

    def getCurretFenString(self):
        self.logger.debug("Returned Current FEN: {}".format(self.board.fen()))
        return self.board.fen()

    def getPlayerMove(self) -> str:
        # Grabbing Move From Stockfish
        move = input("Enter your move: ")
        self.logger.info("Player move: {}".format(move))
        return move

    def processPlayerMove(self, move):
        try:
            m = self.board.parse_uci(move)
        except ValueError:
            self.logger.error("Invalid Move: {}".format(move))
            return False
        if self.board.is_legal(m):
            self.board.push(m)
            return True
        return False

    def generateComputerMove(self) -> str:
        self.stockfish.set_fen_position(self.getCurretFenString())
        return self.stockfish.get_best_move()

    def makeComputerMove(self, move) -> bool:
        self.logger.info("Computer Going To Move: {}".format(move))
        _ = input("Click Enter To Being Moving Robot")
        self.executeMoveOnArduino(move)
        self.arduino.sendCommand("home", [])
        self.arduino.waitForHome()
        self.stockfish.make_moves_from_current_position([move])
        self.board.push_uci(move)
        image = get_perspective_image_gray()
        images = split_image_into_squares(image)
        num = 0
        for i, img in enumerate(images):
            if self.board.color_at(i) == chess.WHITE:
                save_image(
                    img, "training-data/white/{}_{}_{}.png".format(
                        chess.square_name(i), self.board.piece_at(i),
                        time.time()))
                num = num + 1
            if self.board.color_at(i) == chess.BLACK:
                save_image(
                    img, "training-data/black/{}_{}_{}.png".format(
                        chess.square_name(i), self.board.piece_at(i),
                        time.time()))
                num = num + 1
            if self.board.piece_at(i) is None:
                save_image(
                    img, "training-data/blank/{}_{}.png".format(
                        chess.square_name(i), time.time()))
                num = num + 1
        self.logger.info("Saved {} images".format(num))
        return True

    def getLogicName(self):
        return "Stockfish V Player with Arduino And Image Saving"
