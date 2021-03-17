import re
import pygame
import utility_functions

SQUARE_SIZE = 1000 / 8
SQUARE_MIDDLE_OFFSET = SQUARE_SIZE // 2
BOARD_SIZE = 1000

piece_dictionary = {
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


def valid_fen_string(str):
    valid_fen = re.compile(
        "\s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s*"
    )
    return bool(valid_fen.search(str))


def get_indexes_from_coords(coords):
    x = coords[0]
    y = coords[1]
    return (x // SQUARE_SIZE, y // SQUARE_SIZE)


def get_coords_from_position(rank, file):
    return (SQUARE_SIZE * file + SQUARE_MIDDLE_OFFSET,
            SQUARE_SIZE * rank + SQUARE_MIDDLE_OFFSET)


class chess_game:
    """This class is used to represent an entire game and can be rendered using pygame. 
    To create a game pass in a valid fen string. 
    """
    def __init__(
            self,
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.fen = fen
        self.board = [[None for x in range(8)] for y in range(8)]
        self._generate_board()
        self.passant_squares = []

    def _generate_board(self):
        if not valid_fen_string(self.fen):
            raise ValueError("Invalid Fen String")
        rank = 0
        file = 0
        for c in self.fen[:self.fen.index(" ")]:
            if c == '/':
                file = 0
                rank = rank + 1
            elif c.isdigit():
                file = file + int(c)
            else:
                self.board[rank][file] = chess_piece(c)
                file = file + 1

    def print_board(self):
        for rank in self.board:
            for p in rank:
                if p:
                    print(p, end="")
                else:
                    print(".", end="")
            print("")

    def render_to_screen(self, screen):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    self.board[i][j].blitme(i, j, screen)

    def make_move(self, old_pos, new_pos):
        if not old_pos == new_pos:
            self.board[new_pos[0]][new_pos[1]] = self.board[old_pos[0]][
                old_pos[1]]
            self.board[old_pos[0]][old_pos[1]] = None

    def get_piece_at_pos(self, pos):
        return self.board[pos[0]][pos[1]]

    def pos_in_bounds(self, pos):
        return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

    def valid_moves(self, old_pos):
        piece = self.board[old_pos[0]][old_pos[1]]
        rank = old_pos[0]
        file = old_pos[1]
        moves = []
        # Rooks
        if piece.fen == "r" or piece.fen == "R":
            current_pos = (rank - 1, file)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] - 1, current_pos[1])
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank + 1, file)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] + 1, current_pos[1])
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank, file - 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0], current_pos[1] - 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank, file + 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0], current_pos[1] + 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

        # Bishop
        if piece.fen == "b" or piece.fen == "B":
            current_pos = (rank - 1, file - 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] - 1, current_pos[1] - 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank + 1, file + 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] + 1, current_pos[1] + 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank + 1, file - 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] + 1, current_pos[1] - 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)

            current_pos = (rank - 1, file + 1)
            while self.pos_in_bounds(
                    current_pos) and not self.get_piece_at_pos(current_pos):
                moves.append(current_pos)
                current_pos = (current_pos[0] - 1, current_pos[1] + 1)
            if self.pos_in_bounds(current_pos) and self.get_piece_at_pos(
                    current_pos).fen.isupper() != piece.fen.isupper():
                moves.append(current_pos)
        return moves


class chess_piece:
    def __init__(self, fen_abbreviaton):
        self.fen = fen_abbreviaton
        self.sprite = utility_functions.scale_image(
            pygame.image.load(piece_dictionary[self.fen]["image"]), 80)

    def __str__(self):
        return self.fen

    def blitme(self, rank, file, screen):
        x, y = get_coords_from_position(rank, file)
        rect = self.sprite.get_rect()
        rect.centerx = x
        rect.centery = y
        screen.blit(self.sprite, rect)


def main():
    pygame.init()

    game = chess_game(
        "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
    game = chess_game()
    w, h = size = (1000, 1000)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Chess Position")
    board = pygame.transform.smoothscale(
        pygame.image.load("chess_sprites/board.png"), size)

    done = False

    piece_selected = False

    selected_rank = selected_file = None

    clock = pygame.time.Clock()

    game.print_board()

    while not done:
        # Deals with closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_file, clicked_rank = get_indexes_from_coords(
                    pygame.mouse.get_pos())
                clicked_file = int(clicked_file)
                clicked_rank = int(clicked_rank)
                print(clicked_file)
                print(clicked_rank)
                # Checks to see if a piece has already been selected
                if not piece_selected:
                    # Makes sure that the square clicked on contains a piece
                    if game.board[clicked_rank][clicked_file]:
                        piece_selected = True
                        selected_file = clicked_file
                        selected_rank = clicked_rank
                # If it has then we make a move given the coordinates
                else:
                    game.make_move((selected_rank, selected_file),
                                   (clicked_rank, clicked_file))
                    piece_selected = False
                    print(game.valid_moves((clicked_rank, clicked_file)))

        screen.blit(board, (0, 0))
        game.render_to_screen(screen)

        clock.tick(60)

        # This guy actually draws the screen
        pygame.display.flip()


if __name__ == '__main__':
    main()
