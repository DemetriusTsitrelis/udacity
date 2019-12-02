"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from sample_players import improved_score, open_move_score, null_score


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    return improved_score(game, player)


"""
All game heuristics
"""


def CSM(game, player):
    """
    Calculate a score which checks to see whether the player and
    his opponent share future moves.
    """
    score = custom_score(game, player)

    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    common_moves = set(player_moves) & set(opponent_moves)
    if len(player_moves) == 1:
        if len(common_moves) == 1:  # Opponent could block only available move
            score = -50
    elif len(common_moves) > 0:
        score -= len(common_moves)

    return score


def CCE(game, player):
    """
    Calculate a score which checks to see whether the player or his
    opponent can take the spots on the board which control access to
    the corners.
    """
    score = custom_score(game, player)

    w, h = game.width, game.height
    corner_entry_pos = [(1, 2), (1, h - 3), (2, 1), (2, h - 2), (w - 3, 1), (w - 3, h - 2), (w - 2, 2), (w - 2, h - 3)]
    player_pos = game.get_player_location(player)
    if player_pos in corner_entry_pos:
        score += 50

    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    opponent_corner_moves = set(opponent_moves) & set(corner_entry_pos)
    if len(opponent_corner_moves) > 0:
        score -= 50 * len(opponent_corner_moves)

    return score


def CCM(game, player):
    """
    Calculate a score which rewards players for taking moves near
    the middle of the board and penalizes them when opponents can
    move there.  Special consideration is given for occupying the
    center border position.
    """
    center_x, center_y = game.width // 2, game.height // 2

    def within_middle_square(position, extent):
        x, y = position
        if (x > center_x - extent) and (x < center_x + extent) and (
                    y > center_y - extent) and (y < center_y + extent):
            return True
        return False

    player_pos = game.get_player_location(player)
    if player_pos == (center_x, center_y):
        return 500

    if within_middle_square(player_pos, 2):
        return 50

    score = custom_score(game, player)

    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    for opponent_pos in opponent_moves:
        if opponent_pos == (center_x, center_y):
            return -500
        elif within_middle_square(opponent_pos, 2):
            score -= 50

    return score


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        score, best_move = 0, (-1, -1)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                for i in range(1, 1000000000):
                    if self.method == 'minimax':
                        score, best_move = self.minimax(game, i, maximizing_player=True)
                    elif self.method == 'alphabeta':
                        score, best_move = self.alphabeta(game, i, alpha=float("-inf"),
                                                          beta=float("inf"),
                                                          maximizing_player=True)
            else:
                if self.method == 'minimax':
                    score, best_move = self.minimax(game, self.search_depth, maximizing_player=True)
                elif self.method == 'alphabeta':
                    score, best_move = self.alphabeta(game, self.search_depth, alpha=float("-inf"), beta=float("inf"),
                                                      maximizing_player=True)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        score, best_move = 0, (-1, -1)
        if game.is_loser(game.active_player) or game.is_winner(game.active_player) or (depth == 0):
            return self.score(game, self), best_move

        if maximizing_player:
            score = float("-inf")
            for gbest_move in game.get_legal_moves(game.active_player):
                gscore, _ = self.minimax(game.forecast_move(gbest_move), depth - 1, False)
                if gscore > score:
                    score, best_move = gscore, gbest_move
        else:
            score = float("inf")
            for gbest_move in game.get_legal_moves(game.active_player):
                gscore, _ = self.minimax(game.forecast_move(gbest_move), depth - 1, True)
                if gscore < score:
                    score, best_move = gscore, gbest_move

        return score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        score, best_move = 0, (-1, -1)
        if game.is_loser(game.active_player) or game.is_winner(game.active_player) or (depth == 0):
            return self.score(game, self), best_move

        # alpha is Max's best option on path to root
        # beta is Min's best option on path to root
        if maximizing_player:
            score = float("-inf")
            for gbest_move in game.get_legal_moves(game.active_player):
                gscore, _ = self.alphabeta(game.forecast_move(gbest_move), depth - 1, alpha, beta, False)
                if gscore > score:
                    score, best_move = gscore, gbest_move
                if score >= beta:
                    break
                alpha = max(alpha, score)
        else:
            score = float("inf")
            for gbest_move in game.get_legal_moves(game.active_player):
                gscore, _ = self.alphabeta(game.forecast_move(gbest_move), depth - 1, alpha, beta, True)
                if gscore < score:
                    score, best_move = gscore, gbest_move
                if score <= alpha:
                    break
                beta = min(beta, score)

        return score, best_move
