import numpy as np
import requests
import time
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus, chess_notation_to_array, array_to_chess_notation

import random
class RandomAgent:
    def __init__(self, player=PLAYER1):
        self.player = player
    
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

TIMEOUT = 4 # time for each move

class Agent:
    def __init__(self, participant, agent_name):
        self.participant = participant
        self.agent_name = agent_name
        self.latency = None

class Judge:
    def __init__(self, p1_url, p2_url):
        self.p1_url = p1_url
        self.p2_url = p2_url
        self.game = Game()
        self.p1_agent = None
        self.p2_agent = None
        self.game_str = ""

    def check_latency(self):
        """Check latency for both players and create their agents"""
        # Check P1
        try:
            start_time = time.time()
            response = requests.get(self.p1_url, timeout=TIMEOUT)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                self.p1_agent = Agent("Participant1", "Agent1")
                self.p1_agent.latency = (end_time - start_time)
            else:
                return False
                
        except (requests.RequestException, requests.Timeout):
            return False

        # Check P2
        try:
            start_time = time.time()
            response = requests.get(self.p2_url, timeout=TIMEOUT)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                self.p2_agent = Agent("Participant2", "Agent2")
                self.p2_agent.latency = (end_time - start_time)
            else:
                return False
                
        except (requests.RequestException, requests.Timeout):
            return False

        return True

    def start_game(self):
        """ Start the game for both players """
        starting_data = {
            "game": self.game.to_dict(),
            "board": self.game.board.tolist(),
            "max_latency": TIMEOUT,
        }
        # Start p1
        try:
            starting_data['first_turn'] = True
            response = requests.post(f"{self.p1_url}/start", json=starting_data, timeout=TIMEOUT)

        except (requests.RequestException, requests.Timeout):
            return False

        # Start p2
        try:
            starting_data['first_turn'] = False
            response = requests.post(f"{self.p2_url}/start", json=starting_data, timeout=TIMEOUT)
            return True

        except (requests.RequestException, requests.Timeout):
            return False

    def receive_move(self, attempt_number, p1_random, p2_random):
        """ Receive moves from each player """
        move_data = {
                    "game": self.game.to_dict(),
                    "board": self.game.board.tolist(),
                    "turn_count": self.game.turn_count,
                    "attempt_number": attempt_number,
                }
        try:
            if self.game.current_player == PLAYER1:
                move_data["random_attempts"] = p1_random
                start_time = time.time()
                response = requests.post(f"{self.p1_url}/move", json=move_data, timeout=TIMEOUT)
                end_time = time.time()
                self.p1_agent.latency = (end_time-start_time)
            else:
                move_data["random_attempts"] = p2_random
                start_time = time.time()
                response = requests.post(f"{self.p2_url}/move", json=move_data, timeout=TIMEOUT)
                end_time = time.time()
                self.p2_agent.latency = (end_time-start_time)

            # receiving the move
            if response.status_code == 200:
                move = response.json()
                handled_move = self.handle_move(self.game, move['move'])

                # if self.handle_move(self.game, move['move']):
                if handled_move == "forfeit":
                    return "forfeit"
                elif handled_move:
                    return True
                else:
                    return False

                # return True
            else:
                return False 
        except (requests.RequestException, requests.Timeout):
            return False

    def end_game(self, winner):
        """ End the game for both players """
        end_data = {
                    "game": self.game.to_dict(),
                    "board": self.game.board.tolist(),
                    "turn_count": self.game.turn_count,
                    "winner": int(winner)
                }
        try:
            response = requests.post(f"{self.p1_url}/end", json=end_data, timeout=TIMEOUT)
            response = requests.post(f"{self.p2_url}/end", json=end_data, timeout=TIMEOUT)
            print(f"Winner: {'PLAYER1' if winner == PLAYER1 else 'PLAYER2'}")
        except (requests.RequestException, requests.Timeout):
            return False

    def handle_move(self, game, move):
        """ Places the move if valid and returns True or False """

        if not isinstance(move, (list, tuple)) or len(move) < 2:
                print(f"Invalid move format by Player {'P1' if game.current_player == PLAYER1 else 'P2'}")
                # return False
                return "forfeit"

        if len(move) != 2 and len(move) != 4:
            print(f"Invalid move format by Player {'P1' if game.current_player == PLAYER1 else 'P2'}")
            # return False
            return "forfeit"

        chess_move = array_to_chess_notation(move)
        print(f"{game.current_player}'s move is: {move} or {chess_move}")

        try:
            # Convert move elements to integers if they aren't already
            move = [int(x) if isinstance(x, (int, str)) else x for x in move]

            if game.turn_count < 17:
                if game.is_valid_placement(move[0], move[1]):
                    game.place_checker(move[0], move[1])
                else:
                    print(f"Invalid placement by {game.current_player}")
                    # return False
                    return "forfeit"
            else:
                if game.is_valid_move(move[0], move[1], move[2], move[3]):
                    game.move_checker(move[0], move[1], move[2], move[3])
                else:
                    print(f"Invalid move by {game.current_player}")
                    # return False
                    return "forfeit"

            player = 1 if self.game.current_player == 1 else 2
            self.game_str += f"-{chess_move}"
            return True
        except (requests.RequestException, requests.Timeout):
            return False
            

def main():
    # creating judge
    print("Creating judge...")

    judge = Judge("http://ad5761ab88b687.lhr.life:80", "http://127.0.0.1:5008")
    
    # creating game link
    if not judge.check_latency():
        print("Failed to connect to one or both players")
        return
        
    print(f"Player 1: {judge.p1_agent.agent_name} ({judge.p1_agent.participant})")
    print(f"Player 2: {judge.p2_agent.agent_name} ({judge.p2_agent.participant})")
    print(f"Initial latencies - P1: {judge.p1_agent.latency:.3f}s, P2: {judge.p2_agent.latency:.3f}s")
    
    # sending out start information
    print("Starting game...")
    if not judge.start_game():
        print("Failed to start game")
        return

    # random moves left for p1 and p2
    p1_random = 5
    p2_random = 5
        
    # game loop
    while True:
        judge.game.turn_count += 1
        print(f"Turn {judge.game.turn_count}")

        # movement
        print("Sending move to:", judge.game.current_player)

        # first move attempt
        print("First move attempt")
        first_attempt = judge.receive_move(1, p1_random, p2_random)

        # checks if the first attempt was a forfeit
        if first_attempt == "forfeit":
            player = 1 if judge.game.current_player == 1 else 2

            judge.game_str += f"-q"

            winner = 1 if player == 2 else -1

            judge.end_game(winner)
            print("Game String:", judge.game_str)
            break

        # if not judge.send_move(1, p1_random, p2_random):
        if not first_attempt:
            print("Second move attempt")

            second_attempt = judge.receive_move(2, p1_random, p2_random)
            if second_attempt == "forfeit":
                player = 1 if judge.game.current_player == 1 else 2
                # indicates forfeit
                judge.game_str += f"-q"

                winner = 1 if player == 2 else -1

                judge.end_game(winner)
                print("Game String:", judge.game_str)
                break

            # second move attempt
            if not second_attempt:
                # plays a random move
                print(f"Player {'PLAYER1' if judge.game.current_player == PLAYER1 else 'PLAYER2'} failed to make a valid move.")

                current_random_moves = p1_random if judge.game.current_player == PLAYER1 else p2_random
                
                if current_random_moves > 0:
                    random = RandomAgent(player=judge.game.current_player)
                    move = random.get_best_move(judge.game)
                    # judge.handle_move(judge.game, move)

                    move = array_to_chess_notation(move)
                    judge.handle_move(judge.game, move)
                    # tag that it was random
                    judge.game_str += 'r'

                    if judge.game.current_player == PLAYER1:
                        p1_random -= 1
                        print(f"P1 has {p1_random} random moves left")
                    else:
                        p2_random -= 1
                        print(f"P2 has {p2_random} random moves left")
                else:
                    # current player forfeits
                    print(f"Player {judge.game.current_player} has no random moves left. Forfeiting.")
                    if judge.game.current_player == PLAYER1:
                        judge.end_game(PLAYER2)
                    else:
                        judge.end_game(PLAYER1)

                    player = 1 if judge.game.current_player == 1 else 2
                    # indicates forfeit
                    judge.game_str += f"-q"
                    
                    print("Game String:", judge.game_str)
                    break

        judge.game.display_board()
            
        # check for a winner
        winner = judge.game.check_winner()
        if winner != EMPTY:
            judge.end_game(winner)
            print("Game String:", judge.game_str)
            break

        # swaps player
        judge.game.current_player *= -1

        print()

        # draw after certain number of moves???
        # if judge.game.total_moves >= 32:
        #     print("Game ended in a draw")
        #     judge.end_game(EMPTY)
        #     break


if __name__ == "__main__":
    main()
