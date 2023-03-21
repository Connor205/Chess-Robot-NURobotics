from CapturedPieceManagementV2 import CapturedPieceMangementV2
import chess


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

    def __str__(self) -> str:
        return str(self.board) + "\n" + str(self.captured)
