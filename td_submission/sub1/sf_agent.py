import random 
import pyffish as sf
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus
from fairyfishtest import Engine

'''
This is a sample implementation of an agent that just plays a random valid move every turn.
I would not recommend using this lol, but you are welcome to use functions and the structure of this.
'''

class SFAgent:
    def __init__(self, firstturn, max):
        self.max = max
        self.player = "w" if firstturn else "b"
        self.engine = Engine(["./stockfish", "load", "./variants.ini"], "")
        self.engine.initialize("poptactoe")
    
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

    def convert_to_fen(self, game):
        board = game.board.tolist()
        FEN = "/".join(["".join([str(y) for y in x]) for x in board]).replace("-1","p").replace("1", "P").replace("0", "1")
        # FEN += f"[{"P"*(2 - FEN.count('P')) + "p"*(2 - FEN.count('p'))}]"
        FEN += f"[{'P'*(8) + 'p'*(8)}]"
        return FEN
    
    def chess_notation_to_array(self, notation):
        """
        Convert chess notation (a1-h8) to array coordinates (0-7, 0-7).
        """
        def to_array(pos):
            return [8 - int(pos[1]), ord(pos[0]) - ord('a')]

        # Single move (2 characters) or full move (4 characters)
        return to_array(notation[:2]) + (to_array(notation[2:]) if len(notation) == 4 else [])

        
    def get_best_move(self, game):
        """Returns a random valid move."""

        our_pawns = 0
        if(self.player == "w"):
            ps = [(x,y) for x in range(8) for y in range(8) if game.board.tolist()[x][y] == 1]
            
        else:
            ps = [(x,y) for x in range(8) for y in range(8) if game.board.tolist()[x][y] == -1]

                
        x = self.engine.get_best_move(self.convert_to_fen(game) + " " + self.player, self.max).split("@")[-1]
        move = self.chess_notation_to_array(x)
        out = move

        if(len(ps) == 8):
            sorted(ps, key= lambda x : min( abs(x[0] - move[0]),abs(8-x[0]-move[0]))+
                min(abs(x[0] - move[0]),abs(8-x[0]-move[0])))
            out = list(ps[0]) + move
        print(out)
        return out
