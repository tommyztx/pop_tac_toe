from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus

class MinimaxAgent:
    def __init__(self, player=PLAYER1, depth=5):
        self.player = player  # Current player for the agent
        self.opponent = PLAYER2 if player == PLAYER1 else PLAYER1
        self.depth = depth  # Maximum depth for minimax search

    def get_possible_moves(self, game, board):
        """Returns list of all possible moves in the current state."""
        moves = []
        current_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces

        if current_pieces < NUM_PIECES:
            # Placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # Movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves

    def apply_move(self, game, move):
        """
        Simulates applying a move on a copy of the game state.
        Returns a new game state with the move applied.
        """
        new_game = Game.from_dict(game.to_dict())  # Assume PushBattle's Game class supports copying states
        if len(move) == 2:  # Placement move
            r, c = move
            new_game.place_checker(r,c)
        elif len(move) == 4:  # Movement move
            r0, c0, r1, c1 = move
            new_game.move_checker(r0,c0,r1,c1)
        return new_game

    def evaluate(self, game):
        """
        Evaluates the game state and returns a heuristic value.
        Positive values favor the agent, negative values favor the opponent.
        """
        # Example heuristic: Count the agent's and opponent's pieces on the board
        agent_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces
        opponent_pieces = game.p2_pieces if game.current_player == PLAYER1 else game.p1_pieces
        return agent_pieces - opponent_pieces

    def minimax(self, game, board, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or game.check_winner() != 0:
            return self.evaluate(game)

        possible_moves = self.get_possible_moves(game, board)
        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_game = self.apply_move(game, move)
                eval = self.minimax(new_game, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_game = self.apply_move(game, move)
                eval = self.minimax(new_game, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, game, board):
        """
        Returns the best move based on the minimax algorithm.
        """
        possible_moves = self.get_possible_moves(game, board)
        best_move = None
        best_value = float('-inf') if game.current_player == self.player else float('inf')

        # We assume that the MinimaxAgent is called only during the agent's turn
        for move in possible_moves:
            new_game = self.apply_move(game, move)
            move_value = self.minimax(new_game, board, self.depth, maximizing_player=True)  # Since it's the agent's turn, we maximize

            if move_value > best_value:
                best_value = move_value
                best_move = move

        print(best_move)
        return best_move
