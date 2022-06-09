import numpy as np


class CapturedPieceManagement:
    # init method takes in no arguments
    def __init__(self):
        # zero is empty
        # 1 is filled
        self.black = np.zeros((8, 2))
        self.white = np.zeros((2, 8))
        # X, Y
        self.whiteRooks = [(0, 0), (7, 0)]
        self.blackRooks = [(0, 0), (0, 7)]
        self.whiteKnights = [(1, 0), (6, 0)]
        self.blackKnights = [(0, 1), (0, 6)]
        self.whiteBishops = [(2, 0), (5, 0)]
        self.blackBishops = [(0, 2), (0, 5)]
        self.whiteQueens = [(3, 0), (4, 0)]
        self.blackQueens = [(0, 3), (0, 4)]
        self.whitePawns = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                           (6, 1), (7, 1)]
        self.blackPawns = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                           (1, 6), (1, 7)]
        self.black[3, 0] = 1
        self.white[0, 3] = 1

    def placePiece(self, color: str, piece: str):
        squares = []
        if color == "white":
            if piece == "pawn":
                squares = self.whitePawns
            elif piece == "knight":
                squares = self.whiteKnights
            elif piece == "bishop":
                squares = self.whiteBishops
            elif piece == "rook":
                squares = self.whiteRooks
            elif piece == "queen":
                squares = self.whiteQueens
        elif color == "black":
            if piece == "pawn":
                squares = self.blackPawns
            elif piece == "knight":
                squares = self.blackKnights
            elif piece == "bishop":
                squares = self.blackBishops
            elif piece == "rook":
                squares = self.blackRooks
            elif piece == "queen":
                squares = self.blackQueens
        if squares == []:
            raise Exception("Invalid piece: {}, {}".format(color, piece))

        for square in squares:
            x, y = square
            if color == "white":
                if self.white[y, x] == 0:
                    self.white[y, x] = 1
                    return x, y
            elif color == "black":
                if self.black[y, x] == 0:
                    self.black[y, x] = 1
                    return x, y
        raise Exception("No more space for {} {}".format(color, piece))
