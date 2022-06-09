from curses import newwin
from multiprocessing.sharedctypes import Value
from operator import truediv

from numpy import full
from Arduino import Arduino
from GameLogic import GameLogic
import stockfish as sf
import logging
from loggingConstants import handler
import time
import chess
from visionUtilities import get_perspective_image, save_split_images, get_perspective_image_gray, split_image_into_squares, save_image
from CapturedPieceManagement import CapturedPieceManagement
import tensorflow as tf
import cv2
from skimage.metrics import structural_similarity as ssim


def convertSquareToCoordinates(square: str):
    return [ord(square[0]) - ord('a'), 8 - int(square[1])]


def getImagesFromBoard():
    images = split_image_into_squares(get_perspective_image_gray())
    images = [x[40:80, 40:80] for x in images]
    return images


class PlayerVsStockfishVision(GameLogic):

    def __init__(self, port, NNPath, rating=800) -> None:
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
        self.previousImages = getImagesFromBoard()
        self.board = chess.Board()
        # self.board.set_fen(
        #     "r1bqkbnr/pp1p1ppp/2n5/2p1p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR")
        # self.stockfish.set_fen_position(self.board.fen())
        self.pieceManagement = CapturedPieceManagement()

    def checkIfSquareIsOccupied(self, position: str):
        fen = self.getCurretFenString()
        board = chess.Board()
        board.set_fen(fen)
        return board.piece_at(chess.parse_square(position.lower())) is not None

    def takePieceOnSquare(self, square: str):
        color = self.board.color_at(chess.parse_square(square.lower()))
        if color == chess.WHITE:
            color = "white"
        else:
            color = "black"
        x, y = self.pieceManagement.placePiece(
            color,
            chess.piece_name(
                self.board.piece_at(chess.parse_square(square)).piece_type))
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(square)])
        self.arduino.waitForReady()
        self.arduino.sendCommand("pickup", [])
        self.arduino.waitForReady()
        if color == "white":
            self.arduino.sendCommand("moveWhiteTaken", [x, y])
        if color == "black":
            self.arduino.sendCommand("moveBlackTaken", [x, y])
        self.arduino.waitForReady()
        self.arduino.sendCommand("dropTaken", [])
        self.arduino.waitForReady()

    def returnPieceFromSquare(self, color: str, x: int, y: int):
        if color == "black" and x == -1 and y == 3:
            raise ValueError("Cannot Return Default Black Queen")
        if color == "white" and x == 3 and y == 0:
            raise ValueError("Cannot Return Default White Queen")
        if color == "black":
            if x == 1:
                targetY = 1
                targetX = 7 - y
            if x == -1:
                targetY = 0
                targetX = y
            self.arduino.sendCommand("moveBlackTaken", [x, y])
            self.arduino.waitForReady()
            self.arduino.sendCommand("pickupTaken", [])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [targetX, targetY])
            self.arduino.waitForReady()
            self.arduino.sendCommand("drop", [])
            self.arduino.waitForReady()
        if color == "white":
            if y == 1:
                targetY = 6
                targetX = x
            if y == 0:
                targetY = 7
                targetX = x
            self.arduino.sendCommand("moveWhiteTaken", [x, y])
            self.arduino.waitForReady()
            self.arduino.sendCommand("pickupTaken", [])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [targetX, targetY])
            self.arduino.waitForReady()
            self.arduino.sendCommand("drop", [])
            self.arduino.waitForReady()

    def movePieceFromSquareToSquare(self,
                                    startSquare,
                                    endSquare,
                                    fullPickup=False):
        startCoords = convertSquareToCoordinates(startSquare)
        endCoords = convertSquareToCoordinates(endSquare)
        # if start or end is the same then we dont need to lift all the way
        self.arduino.sendCommand(
            "move", [str(x) for x in convertSquareToCoordinates(startSquare)])
        self.arduino.waitForReady()
        if (startCoords[0] == endCoords[0]
                or startCoords[1] == endCoords[1]) and not fullPickup:
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
                    self.movePieceFromSquareToSquare("h1",
                                                     "f1",
                                                     fullPickup=True)
                elif m.to_square == chess.C1:
                    self.movePieceFromSquareToSquare("e1", "c1")
                    self.movePieceFromSquareToSquare("a1",
                                                     "d1",
                                                     fullPickup=True)
            elif m.from_square == chess.E8:
                if m.to_square == chess.G8:
                    self.movePieceFromSquareToSquare("e8", "g8")
                    self.movePieceFromSquareToSquare("h8",
                                                     "f8",
                                                     fullPickup=True)
                elif m.to_square == chess.C8:
                    self.movePieceFromSquareToSquare("e8", "c8")
                    self.movePieceFromSquareToSquare("a8",
                                                     "d8",
                                                     fullPickup=True)
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
        _ = input("Click Enter To Complete Your Move")
        newImages = getImagesFromBoard()
        newWhites = []
        movedWhites = []
        for i in range(0, 64):
            prevSquare = self.previousImages[i]
            newSquare = newImages[i]
            similarity = ssim(prevSquare, newSquare)
            if similarity < 0.7:
                if self.board.color_at(i) == chess.WHITE:
                    movedWhites.append(i)
                else:
                    newWhites.append(i)
            print("{} {}".format(i, similarity))
        print("NewWhites", newWhites)
        print("MovedWhites", movedWhites)
        self.previousImages = newImages

        # for i, img in enumerate(images):
        #     c = self.board.color_at(i)
        #     im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     img_array = tf.expand_dims(im_rgb, axis=0)  # Create a batch
        #     probs = self.nn(img_array)
        #     probs = tf.nn.softmax(probs[0])
        #     probs = probs.numpy()
        #     print(i, probs)
        #     if probs[2] > 0.05 and c != chess.WHITE:
        #         newWhites.append(i)
        #     if probs[1] > .9 and c == chess.WHITE:
        #         movedWhites.append(i)
        # print("New White Squares: {}".format(newWhites))
        # print("Moved White Squares: {}".format(movedWhites))
        # for i, img in enumerate(images):
        #     if self.board.color_at(i) == chess.WHITE:
        #         save_image(
        #             img,
        #             "recentImages/{}_{}_{}.png".format(chess.square_name(i),
        #                                                self.board.piece_at(i),
        #                                                time.time()))
        #     if self.board.color_at(i) == chess.BLACK:
        #         save_image(
        #             img,
        #             "recentImages/{}_{}_{}.png".format(chess.square_name(i),
        #                                                self.board.piece_at(i),
        #                                                time.time()))
        #     if self.board.piece_at(i) is None:
        #         save_image(
        #             img,
        #             "recentImages/{}_{}.png".format(chess.square_name(i),
        #                                             time.time()))
        # time.sleep(1)

        if len(newWhites) == 0:
            raise Exception("No new white squares")
        if len(movedWhites) == 0:
            raise Exception("No missing white pieces")
        if len(newWhites) == len(movedWhites) == 2:
            self.logger.debug("Caste Move Detected")
            if 2 in newWhites:
                self.logger.debug("Castling Queenside")
                return "e1c1"
            if 6 in newWhites:
                self.logger.debug("Castling Kingside")
                return "e1g1"
            raise Exception(
                "No Castling Move Did Not Have Move Ending in c1 or g1")
        if len(newWhites) == len(movedWhites) == 1:
            return chess.square_name(movedWhites[0]) + chess.square_name(
                newWhites[0])
        raise Exception("No Move Found")

    def processPlayerMove(self, move):
        try:
            m = self.board.parse_uci(move)
        except ValueError:
            self.logger.error("Invalid Move: {}".format(move))
            return False

        if self.board.is_capture(m):
            if self.board.is_en_passant(m):
                self.pieceManagement.placePiece("black", "pawn")
            else:
                self.pieceManagement.placePiece(
                    "black",
                    chess.piece_name(
                        self.board.piece_at(m.to_square).piece_type))
        if self.board.is_legal(m):
            self.board.push(m)
            return True
        return False

    def resetBoard(self):

        for i in range(0, 64):
            p = self.board.piece_at(i)
            if p is not None and chess.piece_name(p.piece_type) != "king":
                self.takePieceOnSquare(chess.square_name(i))
        # Now we need to move the kings to their proper starting positions
        self.movePieceFromSquareToSquare(
            chess.square_name(self.board.king(chess.WHITE)), "e1")
        self.movePieceFromSquareToSquare(
            chess.square_name(self.board.king(chess.BLACK)), "e8")
        whiteToReturn = []
        blackToReturn = []
        for y in range(2):
            for x in range(8):
                whiteToReturn.append((x, y))

        for x in [-1, 1]:
            for y in range(8):
                blackToReturn.append((x, y))

        for x, y in whiteToReturn:
            self.returnPieceFromSquare("white", x, y)
        for x, y in blackToReturn:
            self.returnPieceFromSquare("black", x, y)

        self.board = chess.Board()

    def playerWin(self):
        w = self.board.is_checkmate()
        s = self.board.is_stalemate()
        if w:
            self.logger.info("Player Has Won")
            self.arduino.sendCommand("move", [7, 0])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [0, 0])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [7, 0])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [0, 0])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [4, 4])
            self.arduino.waitForReady()
            self.arduino.sendCommand("grab", [])
            self.arduino.waitForReady()
            self.arduino.sendCommand("ungrab", [])

        if s:
            self.logger.info("Game Is A Draw")

        if s or w:
            self.logger.info("Game is Over")
            self.resetBoard()
            return False

        return True

    def generateComputerMove(self) -> str:
        self.stockfish.set_fen_position(self.getCurretFenString())
        return self.stockfish.get_best_move()

    def makeComputerMove(self, move) -> bool:
        self.logger.info("Computer Going To Move: {}".format(move))
        # _ = input("Click Enter To Being Moving Robot")
        self.executeMoveOnArduino(move)
        self.arduino.sendCommand("home", [])
        self.arduino.waitForHome()
        self.stockfish.make_moves_from_current_position([move])
        self.board.push_uci(move)
        image = get_perspective_image_gray()
        images = split_image_into_squares(image)
        num = 0
        self.previousImages = getImagesFromBoard()
        # for i, img in enumerate(images):
        #     if self.board.color_at(i) == chess.WHITE:
        #         save_image(
        #             img, "training-data/white/{}_{}_{}.png".format(
        #                 chess.square_name(i), self.board.piece_at(i),
        #                 time.time()))
        #         num = num + 1
        #     if self.board.color_at(i) == chess.BLACK:
        #         save_image(
        #             img, "training-data/black/{}_{}_{}.png".format(
        #                 chess.square_name(i), self.board.piece_at(i),
        #                 time.time()))
        #         num = num + 1
        #     if self.board.piece_at(i) is None:
        #         save_image(
        #             img, "training-data/blank/{}_{}.png".format(
        #                 chess.square_name(i), time.time()))
        #         num = num + 1
        # self.logger.info("Saved {} images".format(num))
        return True

    def computerWin(self):
        w = self.board.is_checkmate()
        s = self.board.is_stalemate()
        if w:
            self.logger.info("Computer Has Won")
            self.arduino.sendCommand("move", [0, 0])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [7, 7])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [0, 7])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [7, 7])
            self.arduino.waitForReady()
            self.arduino.sendCommand("move", [4, 4])
            self.arduino.waitForReady()
            self.arduino.sendCommand("grab", [])
            self.arduino.waitForReady()
            self.arduino.sendCommand("ungrab", [])

        if s:
            self.logger.info("Game Is A Draw")

        if s or w:
            self.resetBoard()
            return False
        return True

    def getLogicName(self):
        return "Stockfish V Player with Arduino And Image Saving"
