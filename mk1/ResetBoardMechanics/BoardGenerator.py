import chess.pgn
from typing import List
from Board import Board


class BoardGenerator:

    def __init__(self, filename: str):
        self.filename = filename
        self.file = open(self.filename)
        self.games: List[chess.pgn.Game] = []
        while True:
            game = chess.pgn.read_game(self.file)
            if game is None:
                break
            self.games.append(game)

    def get_boards(self):
        boards = []
        for game in self.games:
            try:
                board = Board()
                for move in game.mainline_moves():
                    board.make_move(str(move))
                boards.append(board)
            except:
                pass
        return boards


if __name__ == "__main__":
    generator = BoardGenerator("magnus.pgn")
    boards = generator.get_boards()
    for b in boards:
        print(b)
