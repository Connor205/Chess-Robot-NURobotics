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