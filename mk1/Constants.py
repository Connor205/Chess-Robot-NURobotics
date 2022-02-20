import pygame as pg
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
BOARD_WIDTH = SCREEN_HEIGHT
BOARD_HEIGHT = SCREEN_HEIGHT
SQUARE_SIZE = BOARD_WIDTH // 8

PIECE_DICTIONARY = {
    "p": {
        "black": True,
        "white": False,
        "starting_squares": None,
        "image": "chess_sprites/b_pawn.png"
    },
    "r": {
        "black": True,
        "white": False,
        "starting_squares": ["a8", "h8"],
        "image": "chess_sprites/b_rook.png"
    },
    "n": {
        "black": True,
        "white": False,
        "starting_squares": ["b8", "g8"],
        "image": "chess_sprites/b_knight.png"
    },
    "b": {
        "black": True,
        "white": False,
        "starting_squares": ["c8", "f8"],
        "image": "chess_sprites/b_bishop.png"
    },
    "q": {
        "black": True,
        "white": False,
        "starting_squares": ["d8"],
        "image": "chess_sprites/b_queen.png"
    },
    "k": {
        "black": True,
        "white": False,
        "starting_squares": ["e8"],
        "image": "chess_sprites/b_king.png"
    },
    "P": {
        "black": False,
        "white": True,
        "starting_squares": None,
        "image": "chess_sprites/w_pawn.png"
    },
    "R": {
        "black": False,
        "white": True,
        "starting_squares": ["a1", "h1"],
        "image": "chess_sprites/w_rook.png"
    },
    "N": {
        "black": False,
        "white": True,
        "starting_squares": ["b1", "g1"],
        "image": "chess_sprites/w_knight.png"
    },
    "B": {
        "black": False,
        "white": True,
        "starting_squares": ["c1", "f1"],
        "image": "chess_sprites/w_bishop.png"
    },
    "Q": {
        "black": False,
        "white": True,
        "starting_squares": ["d1"],
        "image": "chess_sprites/w_queen.png"
    },
    "K": {
        "black": False,
        "white": True,
        "starting_squares": ["e1"],
        "image": "chess_sprites/w_king.png"
    }
}

for k, v in PIECE_DICTIONARY.items():
    v["image"] = pg.image.load(v["image"])
    v["image"] = pg.transform.scale(v["image"], (SQUARE_SIZE, SQUARE_SIZE))