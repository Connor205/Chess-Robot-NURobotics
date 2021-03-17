import pygame
import piece


class Chess_Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = []
        self.board.append([
            piece.Piece("b_rook", "a8", self),
            piece.Piece("b_knight", "b8", self),
            piece.Piece("b_bishop", "c8", self),
            piece.Piece("b_queen", "d8", self),
            piece.Piece("b_king", "e8", self),
            piece.Piece("b_bishop", "f8", self),
            piece.Piece("b_knight", "g8", self),
            piece.Piece("b_rook", "h8", self)
        ])
        self.board.append([
            piece.Piece("b_pawn", "a7", self),
            piece.Piece("b_pawn", "b7", self),
            piece.Piece("b_pawn", "c7", self),
            piece.Piece("b_pawn", "d7", self),
            piece.Piece("b_pawn", "e7", self),
            piece.Piece("b_pawn", "f7", self),
            piece.Piece("b_pawn", "g7", self),
            piece.Piece("b_pawn", "h7", self)
        ])
        self.board.append([None] * 8)
        self.board.append([
            piece.Piece("w_pawn", "a2", self),
            piece.Piece("w_pawn", "b2", self),
            piece.Piece("w_pawn", "c2", self),
            piece.Piece("w_pawn", "d2", self),
            piece.Piece("w_pawn", "e2", self),
            piece.Piece("w_pawn", "f2", self),
            piece.Piece("w_pawn", "g2", self),
            piece.Piece("w_pawn", "h2", self)
        ])

    def blitme(self):
        for rank in self.board:
            for item in rank:
                if item:
                    item.blitme()
