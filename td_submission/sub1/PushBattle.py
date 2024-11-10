import numpy as np

# GLOBAL VARIABLES
EMPTY = 0       # Empty space board value
PLAYER1 = 1     # First player board value
PLAYER2 = -1    # Second player board value

BOARD_SIZE = 8  # Size of the board
NUM_PIECES = 8  # Number of pieces each player is allowed to place of their own color

##################

def _torus(r, c):
    rt = (r + BOARD_SIZE) % BOARD_SIZE
    ct = (c + BOARD_SIZE) % BOARD_SIZE
    return rt, ct

def array_to_chess_notation(move: list[int]) -> str:
    """
    Convert array coordinates (0-7, 0-7) to chess notation (a1-h8).
    """
    def to_notation(row, col):
        return f"{chr(ord('a') + col)}{8 - row}"

    # Single move (2 elements) or full move (4 elements)
    return to_notation(move[0], move[1]) + (to_notation(move[2], move[3]) if len(move) == 4 else "")

def chess_notation_to_array(notation: str) -> list[int]:
    """
    Convert chess notation (a1-h8) to array coordinates (0-7, 0-7).
    """
    def to_array(pos):
        return [8 - int(pos[1]), ord(pos[0]) - ord('a')]

    # Single move (2 characters) or full move (4 characters)
    return to_array(notation[:2]) + (to_array(notation[2:]) if len(notation) == 4 else [])

class Game:
    def __init__(self):
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), 0)   # Board represented as a np array of empty spaces (0s)
        self.current_player = PLAYER1                       # Player that has the current move
        self.turn_count = 0                                 # Number of turns elapsed in the game
        self.p1_pieces = 0                                  # Number of pieces that Player1 has placed on the board
        self.p2_pieces = 0                                  # Number of pieces that Player2 has placed on the board

    # Converts all variables of the game to a dictionary
    def to_dict(self):
        return {
            "board": self.board.tolist(),
            "current_player": self.current_player,
            "turn_count": self.turn_count,
            "p1_pieces": self.p1_pieces,
            "p2_pieces": self.p2_pieces,
        }
    
    # Creates a Game object given a dictionary of variables from the game
    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.board = np.array(data["board"])
        game.current_player = data["current_player"]
        game.turn_count = data["turn_count"]
        game.p1_pieces = data["p1_pieces"]
        game.p2_pieces = data["p2_pieces"]
        return game

    # Displays the board
    def display_board(self):
        tile_symbols = {
            EMPTY: '.',
            PLAYER2: 'B',
            PLAYER1: 'W'
        }
        for row in self.board:
            print(' '.join(tile_symbols[tile] for tile in row))

    # Checks if the potential PLACEMENT of the piece is valid
    def is_valid_placement(self, row, col):
        if self.current_player == PLAYER1 and self.p1_pieces >= NUM_PIECES:
            print("White has moved all pieces. Must move an existing piece")
            return False
        if self.current_player == PLAYER2 and self.p2_pieces >= NUM_PIECES:
            print("Black has moved all pieces. Must move an existing piece")
            return False
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY

    # Checks if the potential MOVEMENT of the piece is valid
    def is_valid_move(self, r0, c0, r1, c1):
        # in bounds
        if not (0 <= r0 < BOARD_SIZE and 0 <= c0 < BOARD_SIZE and 
                0 <= r1 < BOARD_SIZE and 0 <= c1 < BOARD_SIZE):
            return False
        
        # is your piece
        if self.board[r0][c0] != self.current_player:
            print("You can only move your own pieces!")
            return False
            
        # is an empty spot
        if self.board[r1][c1] != EMPTY:
            print("Destination square must be empty!")
            return False
            
        return True
     
    # Handles the PLACEMENT of the checker
    def place_checker(self, r, c):
        self.board[r][c] = self.current_player
        if self.current_player == PLAYER1:
            self.p1_pieces += 1
        else:
            self.p2_pieces += 1
        self.push_neighbors(r, c)

    # Handles the MOVEMENT of the checker
    def move_checker(self, r0, c0, r1, c1):
        self.board[r0][c0] = EMPTY
        self.board[r1][c1] = self.current_player
        self.push_neighbors(r1, c1)

    # Push mechanic - Pushes all pieces away
    def push_neighbors(self, r0, c0):
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for dr, dc in dirs:
            # (r1, c1) is a 1-tile (immediate) neighbor of (r0, c0) in the direction (dr, dc)
            r1, c1 = _torus(r0 + dr, c0 + dc)
            if self.board[r1][c1] != EMPTY:
                # (r2, c2) is a 2-tile (secondary) neighbor of (r0, c0) in the direction (dr, dc)
                r2, c2 = _torus(r1 + dr, c1 + dc)
                if self.board[r2][c2] == EMPTY:
                    self.board[r2][c2], self.board[r1][c1] = self.board[r1][c1], self.board[r2][c2]

    # checks for a winner - 3 in a row
    def check_winner(self):
        player1_wins = False
        player2_wins = False
        # check rows
        for row in range(0, BOARD_SIZE):
            cnt = 0
            tile = EMPTY
            for col in range(-2, BOARD_SIZE+2):
                r, c = _torus(row, col)
                curr_tile = self.board[r][c]
                if curr_tile == EMPTY:
                    cnt = 0
                elif curr_tile != tile:
                    cnt = 1
                else:
                    cnt += 1
                    if (cnt == 3):
                        if tile == PLAYER1:
                            player1_wins = True
                        elif tile == PLAYER2:
                            player2_wins = True
                tile = self.board[r][c]

        # check cols
        for col in range(0, BOARD_SIZE):
            cnt = 0
            tile = EMPTY
            for row in range(-2, BOARD_SIZE+2):
                r, c = _torus(row, col)
                curr_tile = self.board[r][c]
                if curr_tile == EMPTY:
                    cnt = 0
                elif curr_tile != tile:
                    cnt = 1
                else:
                    cnt += 1
                    if (cnt == 3):
                        if tile == PLAYER1:
                            player1_wins = True
                        elif tile == PLAYER2:
                            player2_wins = True
                tile = self.board[r][c]

        # check negative diagonals
        for col_start in range(0, BOARD_SIZE):
            cnt = 0
            tile = EMPTY
            for i in range(-2, BOARD_SIZE+2):
                r, c = _torus(i, col_start + i)
                curr_tile = self.board[r][c]
                if curr_tile == EMPTY:
                    cnt = 0
                elif curr_tile != tile:
                    cnt = 1
                else:
                    cnt += 1
                    if (cnt == 3):
                        if tile == PLAYER1:
                            player1_wins = True
                        elif tile == PLAYER2:
                            player2_wins = True
                tile = self.board[r][c]

        # check positive diagonals
        for col_start in range(0, BOARD_SIZE):
            cnt = 0
            tile = EMPTY
            for i in range(-2, BOARD_SIZE+2):
                r, c = _torus(i, col_start - i)
                curr_tile = self.board[r][c]
                if curr_tile == EMPTY:
                    cnt = 0
                elif curr_tile != tile:
                    cnt = 1
                else:
                    cnt += 1
                    if (cnt == 3):
                        if tile == PLAYER1:
                            player1_wins = True
                        elif tile == PLAYER2:
                            player2_wins = True
                tile = self.board[r][c]

        if player1_wins and player2_wins:
            return self.current_player
        # If only one player has 3 in a row, they win
        elif player1_wins:
            return PLAYER1
        elif player2_wins:
            return PLAYER2

        return EMPTY # no one has won the game

    # Play the game
    def play(self):
        while True:
            self.display_board()
            print(f"Player turn: {'W' if self.current_player == PLAYER1 else 'B'}")
            
            # Show the current piece count
            print(f"White pieces: {self.p1_pieces}/{NUM_PIECES}")
            print(f"Black pieces: {self.p2_pieces}/{NUM_PIECES}")

            # Determine if the current player should place or move
            current_pieces = self.p1_pieces if self.current_player == PLAYER1 else self.p2_pieces
            
            if current_pieces < NUM_PIECES:
                print("Place a new piece:")
                try:
                    row, col = map(int, input("Enter row and column: ").split())
                except ValueError:
                    print("Invalid input. Please enter two numbers.")
                    continue

                if not self.is_valid_placement(row, col):
                    print("Invalid move. Try again.")
                    continue

                self.place_checker(row, col)
            else:
                print("Move an existing piece:")
                try:
                    r0, c0, r1, c1 = map(int, input("Enter source (r0, c0) and destination (r1, c1): ").split())
                except ValueError:
                    print("Invalid input. Please enter four numbers.")
                    continue

                if not self.is_valid_move(r0, c0, r1, c1):
                    print("Invalid move. Try again.")
                    continue

                self.move_checker(r0, c0, r1, c1)

            self.turn_count += 1

            winner = self.check_winner()
            if winner != EMPTY:
                self.display_board()
                print(f"{'White' if winner == PLAYER1 else 'Black'} wins!")
                break

            self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

def main():
    poptactoe = Game()
    poptactoe.play()

if __name__ == '__main__':
    main()
