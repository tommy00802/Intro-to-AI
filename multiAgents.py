from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        print(newScores)
        return newScores, None

    """
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE

    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """
	
    if(maximizingPlayer):
        return _max(game_state, depth, alpha, beta)
    else:
        return _min(game_state, depth, alpha, beta)

	# return value, best_move
	
# helper function for minimax to find the max value
def _max(game_state: GameStatus, depth: int, alpha: float, beta: float):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        # print(newScores)
        return newScores, None
    
    v = float('-inf')
    move = None
    for a in game_state.get_moves():
        # pretend to make move "a"
        v2, a2 = _min(game_state.get_new_state(a), depth - 1, alpha, beta)
        # print(v2)
        if (v2 > v):
            v = v2
            move = a
        # alpha/beta pruning
        # v = max(v, v2, alpha, beta)
        # if v >= beta: return v, a
        alpha = max(alpha, v)
        if alpha >= beta: break
    return v, move

# helper function for minimax to find the min value
def _min(game_state: GameStatus, depth: int, alpha: float, beta: float):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None
    
    v = float('inf')
    move = None
    for a in game_state.get_moves():
        # pretend to make move "a"
        v2, a2 = _max(game_state.get_new_state(a), depth - 1, alpha, beta)
        # print(v2)
        if (v2 < v):
            v = v2
            move = a
        # alpha/beta pruning
        # v = min(v, v2, alpha, beta)
        # if v <= alpha: return v, a
        beta = min(beta, v)
        if alpha >= beta: break
    return v, move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores * turn_multiplier, None

    """
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE

    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE

    """

    v = float('-inf')
    move = None
    for a in game_status.get_moves():
        v = max(v, -negamax(game_status.get_new_state(a), depth - 1, -turn_multiplier, -beta, -alpha)[0])
        alpha = max(alpha, v)
        if alpha >= beta: break
        move = a
        # value, _ = negamax(game_status.get_new_state(a), depth - 1, -turn_multiplier, -beta, -alpha)
        # value *= turn_multiplier # negate value for opponent
        # print(value)

        # if value > v:
        #     move = a
        # alpha = max(alpha, value)
        # if alpha >= beta:
        #     break # beta cutoff
    return v, move

    #return value, best_move