"""This file will be used for the piece object.
"""
import pygame


def scale_image(surface, percent):
    rect = surface.get_rect()
    height = rect[3] - rect[1]
    width = rect[2] - rect[0]

    height = height * percent // 100
    width = width * percent // 100
    return pygame.transform.smoothscale(surface, (width, height))


piece_dictionary = {
    "b_pawn": {
        "black": True,
        "white": False,
        "starting_squares": None,
        "image": "chess_sprites/b_pawn.png"
    },
    "b_rook": {
        "black": True,
        "white": False,
        "starting_squares": ["a8", "h8"],
        "image": "chess_sprites/b_rook.png"
    },
    "b_knight": {
        "black": True,
        "white": False,
        "starting_squares": ["b8", "g8"],
        "image": "chess_sprites/b_knight.png"
    },
    "b_bishop": {
        "black": True,
        "white": False,
        "starting_squares": ["c8", "f8"],
        "image": "chess_sprites/b_bishop.png"
    },
    "b_queen": {
        "black": True,
        "white": False,
        "starting_squares": ["d8"],
        "image": "chess_sprites/b_queen.png"
    },
    "b_king": {
        "black": True,
        "white": False,
        "starting_squares": ["e8"],
        "image": "chess_sprites/b_king.png"
    },
    "w_pawn": {
        "black": False,
        "white": True,
        "starting_squares": None,
        "image": "chess_sprites/w_pawn.png"
    },
    "w_rook": {
        "black": False,
        "white": True,
        "starting_squares": ["a1", "h1"],
        "image": "chess_sprites/w_rook.png"
    },
    "w_knight": {
        "black": False,
        "white": True,
        "starting_squares": ["b1", "g1"],
        "image": "chess_sprites/w_knight.png"
    },
    "w_bishop": {
        "black": False,
        "white": True,
        "starting_squares": ["c1", "f1"],
        "image": "chess_sprites/w_bishop.png"
    },
    "w_queen": {
        "black": False,
        "white": True,
        "starting_squares": ["d1"],
        "image": "chess_sprites/w_queen.png"
    },
    "w_king": {
        "black": False,
        "white": True,
        "starting_squares": ["e1"],
        "image": "chess_sprites/w_king.png"
    }
}

SQUARE_SIZE = 1000 / 8
SQUARE_MIDDLE_OFFSET = SQUARE_SIZE // 2
BOARD_SIZE = 1000

row_x_coords = {
    "a": 0 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "b": 1 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "c": 2 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "d": 3 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "e": 4 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "f": 5 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "g": 6 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET,
    "h": 7 * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET
}


def get_coords_from_position(position):
    x = row_x_coords[position[0]]
    y = (8 - int(position[1])) * SQUARE_SIZE + SQUARE_MIDDLE_OFFSET
    return (x, y)


class Piece:
    def __init__(self, id, position, chess_game):
        self.white = piece_dictionary[id]["white"]
        self.black = piece_dictionary[id]["black"]
        self.id = id
        self.sprite = piece_dictionary[id]["image"]
        self.position = position
        self.image = scale_image(pygame.image.load(self.sprite), 90)
        self.screen = chess_game.screen
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = get_coords_from_position(
            position)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def move_to(self, position):
        self.position = position
        self.rect.centerx, self.rect.centery = get_coords_from_position(
            position)
