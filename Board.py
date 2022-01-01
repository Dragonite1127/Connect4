import Tile
import Color
from copy import deepcopy

TILE_SIZE = 100
"""A class that represents the board of the game."""


class Board:
    def __init__(self, width: int, height: int, player1: Color.Colors, player2: Color.Colors):
        self.width = width
        self.height = height
        self.board = self.init_board()
        self.moves = 0
        self.player1 = player1
        self.player2 = player2
        self.screen = None  # set manually in main,

    def __str__(self):
        """Returns the string representation of the board."""
        string = ""
        width = 7
        height = 6
        for row in range(height):
            for col in range(width):
                color = self.board[row][col].color
                color = Color.Colors.tostring(color)[0]
                string = string + color + " "
                if col == 6:
                    string = string + "\n"
        return string

    def __eq__(self, other):
        """Returns true iff the inputted Board object equals self."""
        if not isinstance(other, Board):
            return False
        if self.width == other.width and self.height == other.height and self.moves == other.moves \
                and self.player1 == other.player1 and self.player2 == other.player2:
            for row in range(0, 6):
                for col in range(0, 7):
                    if self.board[row][col] != other.board[row][col]:
                        return False
            return True
        return False

    def deep_copy(self):
        """Returns a Board object that copies all the contents from self."""
        height = 6
        width = 7
        board_copy = Board(self.width, self.height, self.player1, self.player2)
        board_copy.moves = self.moves
        for row in range(height):
            for col in range(width):
                board_copy.board[row][col].color = self.board[row][col].color
                board_copy.board[row][col].image = self.board[row][col].image
                board_copy.board[row][col].rect = self.board[row][col].rect
        return board_copy

    def init_board(self):
        """Initializes a game board."""
        width = 7
        height = 6
        board = [None] * height
        for i in range(height):
            board[i] = [None] * width
        for row in range(height):
            for col in range(width):
                board[row][col] = Tile.Tile(row * 100, col * 100)
        return board

    def whose_move(self):
        """Returns whose move it currently is."""
        return self.player1 if self.moves % 2 == 0 else self.player2

    def is_legal(self, row: int, col: int, player: Color.Colors):
        """Returns true iff it is legal for the current
        player to make a move in the game."""
        return self.whose_move() == player and self.board[row][col].color == Color.Colors.WHITE

    def is_empty(self, row: int, col: int):
        """Returns true iff a tile is empty at
        ROW COL. """
        return self.board[row][col].color == Color.Colors.WHITE


    def legal_moves(self):
        """Returns a list of tuples (row, column) containing
        legal moves for the current player.
         A move is valid iff the tile's color is WHITE."""
        player = self.whose_move()
        moves = []
        for col in range(7):
            if self.board[0][col].color != Color.Colors.WHITE:
                continue
            else:
                row = 5
                while row >= 0:
                    if self.board[row][col].color == Color.Colors.WHITE:
                        moves.append((row, col))
                        break
                    elif self.board[row][col].color != Color.Colors.WHITE:
                        while self.board[row][col].color != Color.Colors.WHITE:
                            row -= 1
                        moves.append((row, col))
                        break
                    else:
                        raise RuntimeError
        return moves

    def make_move(self, row: int, col: int, player: Color.Colors):
        """Makes a move in the game."""
        if not self.is_legal(row, col, player):
            return False
        else:
            def swim_down():
                temp_row = 0
                self.board[temp_row][col].change_color(player)
                if self.screen is not None:
                    self.screen.update_tile(temp_row, col)
                temp_row += 1
                while 6 != temp_row and \
                        self.board[temp_row][col].color == Color.Colors.WHITE:
                    self.board[temp_row - 1][col].change_to_white(), self.board[temp_row][col].change_color(player)
                    if self.screen is not None:
                        self.screen.update_tile(temp_row, col), self.screen.update_tile(temp_row - 1, col)
                    temp_row += 1

            swim_down()
            self.moves += 1

    def check_win(self):
        """Checks if either player RED or player YELLOW won the game."""
        width = 7
        height = 6

        def horizontal():
            """Checks if there exists a winning position horizontally."""
            for color in [self.player1, self.player2]:
                for col in range(width):
                    for row in range(height):
                        try:
                            if self.board[row][col].color == color == self.board[row + 1][col].color \
                                    == self.board[row + 2][col].color == self.board[row + 3][col].color:
                                return color
                        except IndexError:
                            pass

            return Color.Colors.WHITE

        def vertical():
            """Checks if there exists a winning position vertically."""
            for color in [self.player1, self.player2]:
                for sublist in self.board:
                    for i in range(len(sublist)):
                        try:
                            if color == sublist[i].color == sublist[i + 1].color == sublist[i + 2].color \
                                    == sublist[i + 3].color:
                                return color
                        except IndexError:
                            break
            return Color.Colors.WHITE

        def diagonal_positive():
            """Checks positively sloped diagonals."""
            for color in [self.player1, self.player2]:
                for col in range(width - 3):
                    for row in range(height - 3):
                        if self.board[row][col].color == color and self.board[row + 1][col + 1].color == color \
                                and self.board[row + 2][col + 2].color == color \
                                and self.board[row + 3][col + 3].color == color:
                            return color
            return Color.Colors.WHITE

        def diagonal_negative():
            """Checks negatively sloped diagonals"""
            for color in [self.player1, self.player2]:
                for col in range(width - 3):
                    for row in range(3, height):
                        if self.board[row][col].color == color and self.board[row - 1][col + 1].color == color \
                                and self.board[row - 2][col + 2].color == color \
                                and self.board[row - 3][col + 3].color == color:
                            return color
            return Color.Colors.WHITE

        horiz_color = horizontal()
        if horiz_color != Color.Colors.WHITE:
            return horiz_color
        vertical_color = vertical()
        if vertical_color != Color.Colors.WHITE:
            return vertical_color
        diagonal_color_pos = diagonal_positive()
        if diagonal_color_pos != Color.Colors.WHITE:
            return diagonal_color_pos
        diagonal_color_neg = diagonal_negative()
        if diagonal_color_neg != Color.Colors.WHITE:
            return diagonal_color_neg
        if self.draw():
            return False
        else:
            return Color.Colors.WHITE

    def draw(self):
        """Returns true iff the whole board is occupied by a
        nonwhite space."""
        occupied = 0
        for row in range(0, 6):
            for col in range(0, 7):
                if self.board[row][col].color != Color.Colors.WHITE:
                    occupied += 1
        return occupied == 42
