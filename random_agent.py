import random
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus

'''
This is a sample implementation of an agent that just plays a random valid move every turn.
I would not recommend using this lol, but you are welcome to use functions and the structure of this.
'''

class RandomAgent:
    def __init__(self, player=PLAYER1):
        self.player = player
    
    # given the game state, gets all of the possible moves
    def get_possible_moves(self, game):
        """Returns list of all possible moves in current state."""
        moves = []
        current_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces
        
        if current_pieces < NUM_PIECES:
            # placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves
        
    def get_best_move(self, game):
        """Returns a random valid move."""
        possible_moves = self.get_possible_moves(game)
        return random.choice(possible_moves)
