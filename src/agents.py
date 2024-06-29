import datetime
import random

import chess

import utiles
import math


class Agent:
    """
        Base class for agents.
    """

    def __init__(self, board: chess.Board, next_player) -> None:
        self.board = board
        self.next_player = next_player

    def get_action(self):
        """
            This method receives a GameState object and returns an action based on its strategy.
        """
        pass

    """
            get possible moves : 
                possibleMoves = board.legal_moves

            create a move object from possible move : 
                move = chess.Move.from_uci(str(possible_move))

            push the move : 
                board.push(move)

            pop the last move:
                board.pop(move)
    """


class RandomAgent(Agent):
    def __init__(self, board: chess.Board, next_player):
        super().__init__(board, next_player)

    def get_action(self):
        return self.random()

    def random(self):
        possible_moves_list = list(self.board.legal_moves)

        random_move = random.choice(possible_moves_list)
        return chess.Move.from_uci(str(random_move))


class MinimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        print(self.next_player)
        return self.minimax(depth=0, turn=self.next_player, is_maximizing=True)[0]

    def minimax(self, depth, turn, is_maximizing):
        if depth == self.depth:
            return (None, evaluate_board_state(self.board, turn))

        if is_maximizing == True:
            value = -math.inf
            best_move = None
            possible_moves = list(self.board.legal_moves)

            for move in possible_moves:
                self.board.push(move)
                move_and_value = self.minimax(depth + 1, turn, not is_maximizing)

                if move_and_value[1] > value:
                    value = move_and_value[1]
                    best_move = move_and_value[0]

                self.board.pop()

            return (best_move, value)
        
        if is_maximizing == False:
            value = math.inf
            best_move = None
            possible_moves = list(self.board.legal_moves)

            for move in possible_moves:
                self.board.push(move)
                move_and_value = self.minimax(depth + 1, self.next_player, not is_maximizing)

                if move_and_value[1] < value:
                    value = move_and_value[1]
                    best_move = move_and_value[0]

                self.board.pop()

            return (best_move, value)


class AlphaBetaAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        return self.alpha_beta(0, self.next_player, True, -math.inf, math.inf)[0]

    def alpha_beta(self, depth, turn, is_maximizing, alpha, beta):
        if depth == self.depth:
            return (None, evaluate_board_state(self.board, turn))
        if is_maximizing == True:
            max_move = -math.inf

            legal_moves = self.board.legal_moves
            for move in legal_moves:
                self.board.push(move)
                optimal_move_and_value = self.alpha_beta(depth + 1, turn, not is_maximizing, alpha, beta)
                self.board.pop()

                if optimal_move_and_value[1] > max_move[1]:
                    max_move = (optimal_move_and_value[1], move)
                    alpha = max(alpha, optimal_move_and_value[1])

                if max_move[1] >= beta:
                    return max_move
            return max_move

        if is_maximizing == False:
            min_move = math.inf
            legal_moves = self.board.legal_moves

            for move in legal_moves:
                self.board.push(move)
                optimal_move_and_value = self.alpha_beta(depth + 1, turn, not is_maximizing, alpha, beta)
                self.board.pop()

                if optimal_move_and_value[1] < min_move[1]:
                    min_move = (optimal_move_and_value[1], move)
                    beta = min(beta, optimal_move_and_value[1])
                if min_move[1] <= alpha:
                    return min_move
            return min_move


class ExpectimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        return self.expectimax(0, self.next_player, True)[0]
    
    def expectimax(self, depth, turn, is_maximizing):
        if depth == self.depth:
            return (evaluate_board_state(self.board, turn), None)

        if is_maximizing == True:
            max_move = (None, -math.inf)
            legal_moves = self.board.legal_moves

            for move in legal_moves:
                self.board.push(move)
                best_move_and_its_value = self.expectimax(depth + 1, turn, not is_maximizing)[1]
                self.board.pop()

                if best_move_and_its_value[1] > max_move[1]:
                    max_move = (best_move_and_its_value[1], move)

            return max_move

        if is_maximizing == False:
            value = 0
            legal_moves = self.board.legal_moves
            for move in legal_moves:
                self.board.push(move)
                value += self.expectimax(depth + 1, turn, not is_maximizing)[1]
                self.board.pop()

            value /= self.board.legal_moves.count()
            return (value, None)


def evaluate_board_state(board, turn):
    node_evaluation = 0
    node_evaluation += utiles.check_status(board, turn)
    node_evaluation += utiles.evaluationBoard(board)
    node_evaluation += utiles.checkmate_status(board, turn)
    node_evaluation += utiles.good_square_moves(board, turn)
    if turn == 'white':
        return node_evaluation
    return -node_evaluation
