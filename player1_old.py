from flask import Flask, request, jsonify
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus

# Import This
from random_agent import RandomAgent

app = Flask(__name__)


@app.route('/start', methods=['POST'])
def start_game():
    """
    This function is sent before the game begins.
    Used to potentially configure your agent based on latency constraints or if you have the first turn

    Values:
    game - Game object - Contains all information about the game
    board - 2D Array - 2D array of the board
    first_turn - Boolean - True if your agent has the first turn; False if your agent has the second turn
    max_latency - Int - Integer representing how many seconds you have to make a move
    """

    ##### DO NOT MODIFY #####
    global agent
    data = request.get_json()
    game_data = data.get('game')
    game = Game.from_dict(game_data)
    board = data.get('board')
    first_turn = data.get('first_turn')
    max_latency = data.get('max_latency')

    ##### MODIFY BELOW #####

    agent = RandomAgent()

    ###################
    
    return jsonify({
        "message": "Game started successfully"
    })

@app.route('/move', methods=['POST'])
def make_move():
    """
    This is the primary function that is being sent during the game to make your move.
    I recommend using some kind of function in your class to evaluate what your agent thinks is the best move

    Values:
    game - Game object - Contains all information about the game
    board - 2D Array - 2D array of the board
    turn_count - Int - How many turns have elapsed in the game, Player1 begins the game on turn 1.
    attempt_number - Int - 2 attempts per move, attempt 1 is the first move attempt, and if this fails then attempt 2 is the second move attempt

    Move Return:
    Your move should be sent as a list of integers.
    If you are PLACING a piece (you have less than 8 pieces currently placed), the move should look like: [r0, c0]
    r0 - row value of the piece to place
    c0 - column value of the piece to place

    If you are MOVING a piece (you have all 8 pieces currently placed), the move should look like: [r0,c0,r1,c1]
    r0 - row value of the piece to move
    c0 - column value of the piece to move
    r1 - row value of the piece to place
    c1 - column value of the piece to place
    """
    data = request.get_json()
    game_data = data.get('game')
    game = Game.from_dict(game_data)
    board = data.get('board')
    turn_count = data.get('turn_count')
    attempt_number = data.get('attempt_number')
    
    ##### MODIFY BELOW #####

    # Move logic should go here
    # This is where you'd call your minimax/MCTS/neural network/etc

    move = agent.get_best_move(game)

    ###################
    
    return jsonify({
        "move": move  # Return your chosen move
    })

# ====================================
# DO NOT MODIFY BELOW THIS LINE
# ====================================

@app.route('/', methods=['GET'])
def hello():
    """Connects to the judge"""
    return jsonify({
        "message": "Successfully Connected",
    })

@app.route('/end', methods=['POST'])
def end_game():
    """Handle game end notification"""
    data = request.get_json()
    # Extract end game data
    print(data)
    
    return jsonify({
        "message": "Game ended successfully"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
