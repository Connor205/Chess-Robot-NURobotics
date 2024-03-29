import numpy as np
from typing import Tuple

# We can set the default arrays to use for where the pieces get placed
# This will make it easier to add new pieces
BLACK_DEFAULT = [["r", "p"], ["n", "p"], ["b", "p"], ["q", "p"], ["Q", "p"],
                 ["b", "p"], ["n", "p"], ["r", "p"]]
WHITE_DEFAULT = [["P", "R"], ["P", "N"], ["P", "B"], ["P", "Q"], ["P", "Q"],
                 ["P", "B"], ["P", "N"], ["P", "R"]]


class CapturedPieceMangementV2:

    def __init__(self):
        # We need 2 8 by 2 arrays to maintain the captured pieces
        self.white = np.zeros((8, 2))
        self.black = np.zeros((8, 2))

    def placePiece(self, toPlace: str) -> Tuple[int, int, str]:
        # check if the piece is white or black
        if toPlace.isupper():
            # white piece
            # Check to see the first place in the default array that matches the input piece and where the array is empty
            for i in range(len(WHITE_DEFAULT)):
                for j in range(len(WHITE_DEFAULT[i])):
                    if WHITE_DEFAULT[i][j] == toPlace and self.white[i][j] == 0:
                        # place the piece
                        self.white[i][j] = 1
                        return i, j, "white"
        else:
            # black piece
            # Check to see the first place in the default array that matches the input piece and where the array is empty
            for i in range(len(BLACK_DEFAULT)):
                for j in range(len(BLACK_DEFAULT[i])):
                    if BLACK_DEFAULT[i][j] == toPlace and self.black[i][j] == 0:
                        # place the piece
                        self.black[i][j] = 1
                        return i, j, "black"
        # If we get here, we didn't find a place to put the piece
        raise Exception("Invalid piece: {}".format(toPlace))

    def get_piece(self, x: int, y: int, color: str) -> str:
        if color == "white":
            return self.white[y][x]
        elif color == "black":
            return self.black[y][x]
        else:
            raise Exception("Invalid color: {}".format(color))

    def remove_piece(self, x, y):
        # x and y here are for the entire board
        if x < 2:
            prev = BLACK_DEFAULT[y][x]
            self.black[y][x] = 0
            return prev
        elif x > 11:
            prev = WHITE_DEFAULT[y][x - 12]
            self.white[y][x - 12] = 0
            return prev
        else:
            print("Invalid Params, nothing removed from captured")
            return None

    def board_representation(self):
        white = []
        black = []
        for y in range(8):
            white_row = []
            black_row = []
            for x in range(2):
                if self.white[y][x]:
                    white_row.append(WHITE_DEFAULT[y][x])
                else:
                    white_row.append("")
                if self.black[y][x]:
                    black_row.append(BLACK_DEFAULT[y][x])
                else:
                    black_row.append("")
            white.append(white_row)
            black.append(black_row)
        return black, white

    def __str__(self) -> str:
        # This function will return a string representation of the captured pieces
        # We will use the default arrays to print the pieces
        output = "White Pieces:\n"
        for i in range(len(WHITE_DEFAULT)):
            for j in range(len(WHITE_DEFAULT[i])):
                if self.white[i][j] == 1:
                    output += WHITE_DEFAULT[i][j]
                else:
                    output += " "
            output += "\n"
        output += "Black Pieces:\n"
        for i in range(len(BLACK_DEFAULT)):
            for j in range(len(BLACK_DEFAULT[i])):
                if self.black[i][j] == 1:
                    output += BLACK_DEFAULT[i][j]
                else:
                    output += " "
            output += "\n"
        return output