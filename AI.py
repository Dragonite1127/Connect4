import Color
import Board
import random

"""An automated player that uses the minimax algorithm to make a move."""


class AI:
    MAX_DEPTH = 2
    INFINITY = 10000000000000000000000000

    def __init__(self, game: Board, color: Color.Colors):
        self.game = game
        self.color = color
        self.found_move = (-1, 0)
        self.moves = {}

    def get_move(self):
        """Returns the move that the AI will make in
        this Connect 4 game."""
        assert self.color == self.game.whose_move()
        self.moves = {}
        choice = self.search_for_move()
        return choice

    def search_for_move(self):
        """Searches for a move using the minimax algorithm."""
        assert self.game.whose_move() == self.color
        board = self.game.deep_copy()
        self.found_move = random.choice(board.legal_moves())
        self.moves[self.found_move] = -100
        value = -1
        value = \
            self.minimax(board, AI.MAX_DEPTH, True, -AI.INFINITY, AI.INFINITY)
        legal_moves = self.game.legal_moves()
        moves_to_delete = []
        for elem in self.moves.keys():
            if elem not in legal_moves:
                moves_to_delete.append(elem)
        for elem in moves_to_delete:
            del self.moves[elem]
        return max(self.moves, key=self.moves.get)

    def minimax(self, board: Board, depth: int, maximizing_player: bool, alpha: int, beta: int):
        """Find a move from position BOARD and return its value, recording the
        move found in self.found_move iff save_move. The move should have
        maximal value or have value > BETA if maximizing_player,
        and minimal value or value < ALPHA if minimizing_player. Searches up
        to DEPTH levels. Searching at level 0 simply returns a static estimate
        of the board value and does not set found_move. If the game is over on
        board, does not set found_move. """
        win = board.check_win()
        if win == False or win.value != 0 or depth == 0 \
                or len(board.legal_moves()) == 0:
            return self.static_eval(board, win)
        elif maximizing_player:
            value = -AI.INFINITY
            moves = board.legal_moves()
            for move in moves:
                board_copy = board.deep_copy()
                board_copy.make_move(move[0], move[1], self.color)
                score = self.minimax(board_copy, depth - 1, False, alpha, beta)
                if score > value:
                    value = score
                    self.moves[move] = score
                    self.found_move = move
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = AI.INFINITY
            moves = board.legal_moves()
            for move in moves:
                board_copy = board.deep_copy()
                if not board_copy.is_empty(move[0], move[1]):
                    continue
                board_copy.make_move(move[0], move[1], Color.Colors.opposite(self.color))
                score = self.minimax(board_copy, depth - 1, True, alpha, beta)
                if score < value:
                    value = score
                    # self.moves[move] = score
                    self.found_move = move
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value

    def static_eval(self, board, win):
        """Returns a heuristic estimate of the value
        of board position B. """
        if isinstance(win, bool):  # game ends in a draw
            return 0
        elif win.value == self.color.value:
            return 1000000000000000000000
        elif win.value == Color.Colors.opposite(self.color).value:
            return -100000000000000000000
        else:
            score = self.score_position(board, self.color)
            return score

    def score_position(self, board: Board, player: Color.Colors):
        """Returns the score of the current BOARD position for
        player PLAYER. """
        width = 7
        height = 6
        score = 0

        # center score
        center_array = [col[3].color for col in board.board]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal Score
        for r in range(height):
            row_array = [elem.color for elem in board.board[r]]
            for c in range(width - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, player)

        # Vertical Score
        for col in range(7):
            col_array = [elem[col].color for elem in board.board]
            for row in range(6 - 3):
                window = col_array[row: row + 4]
                score += self.evaluate_window(window, player)

        # Positive sloped diagonal score and # Negatively sloped diagonal
        for row in range(6 - 3):
            for col in range(7 - 3):
                window = [board.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)
                window = [board.board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def evaluate_window(self, window: list, player: Color.Colors):
        """Compares the number of pieces between player PLAYER and
        the opponent and delegates the appropriate score. """
        score = 0
        opponent = Color.Colors.opposite(player)
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(Color.Colors.WHITE) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(Color.Colors.WHITE) == 2:
            score += 2
        elif window.count(opponent) == 3 and window.count(Color.Colors.WHITE) == 1:
            score -= 8
        elif window.count(opponent) == 2 and window.count(Color.Colors.WHITE) == 2:
            score -= 12
        return score
