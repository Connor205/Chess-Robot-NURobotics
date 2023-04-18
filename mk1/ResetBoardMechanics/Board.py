from CapturedPieceManagementV2 import CapturedPieceMangementV2
import chess
import numpy as np


class Board:
    # This class will handle the current representaton of all of the pieces on the board, including the two extra areas
    # for the pieces that are not currently on the board
    def __init__(self):
        # We can use our capturedPieceManagement class to handle the pieces that are not currently on the board
        self.captured: CapturedPieceMangementV2 = CapturedPieceMangementV2()

        # Lets go ahead and fill the board with the starting chess position using the FEN notation
        self.board: chess.Board = chess.Board()

    def get_piece(self, file: int, rank: int):
        # This function will return the piece at the given rank and file
        return self.board.piece_at(chess.square(file, rank))

    def get_captured_piece(self, x: int, y: int, color: str):
        # This function will return the piece at the given rank and file
        return self.captured.get_piece(x, y, color)

    def make_move(self, move):
        # generate the move from uci
        move = chess.Move.from_uci(move)
        if self.board.piece_at(move.to_square) is not None:
            # We need to capture the piece
            self.captured.placePiece(
                self.board.piece_at(move.to_square).symbol())
        self.board.push(move)

    def get_full_board(self):
        # We want to generate a full board with 8 rows and 14 columns which includes both piece generation and the actual boardstate
        # We can represent this as a 2d array of characters
        currentInPlayBoard = np.zeros((8, 8), str)
        for file in range(8):
            for rank in range(8):
                # Lets get the piece
                piece = self.board.piece_at(chess.square(file, rank))
                if piece is not None:
                    currentInPlayBoard[rank][file] = piece.symbol()
                else:
                    currentInPlayBoard[rank][file] = ""
        black, white = self.captured.board_representation()
        newArray = []
        for h in range(8):
            newArray.append(black[h] + [""] +
                            list(list(currentInPlayBoard)[h]) + [""] +
                            white[h])
        return newArray

    def set_square(self, square, p):
        self.board.set_piece_at(square, chess.Piece.from_symbol(p))

    def remove_piece(self, x, y) -> str:
        # print(f"Attempting to remove piece at x: {x}, y: {y}")
        if x < 2 or x > 11:
            return self.captured.remove_piece(x, y)
        else:
            # print(self.board)
            # print(chess.square_name(chess.square(x - 3, y)))
            return self.board.remove_piece_at(chess.square(x - 3, y)).symbol()

    def __str__(self) -> str:
        return str(self.board) + "\n" + str(self.captured)
