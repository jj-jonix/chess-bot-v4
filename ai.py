import random
PIECE_VALUE = {'K': 999, 'Q':9, 'R': 5, 'B': 3 , 'N': 3, 'P':1 }
CHECKMATE_SCORE = 1000
STALEMATE_SCORE = 0
DEPTH = 4

def choose_move(gamestate, valid_moves):
    return call_negamax(gamestate,valid_moves)

KNIGHT_TABLE = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
]

BISHOP_TABLE = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
]

ROOK_TABLE = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ 0.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0,  0.0],
]

QUEEN_TABLE = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
]

PAWN_TABLE = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]
 
PIECE_SQUARE_TABLES = {
    'N': KNIGHT_TABLE,
    'B': BISHOP_TABLE,
    'R': ROOK_TABLE,
    'Q': QUEEN_TABLE,
    'P': PAWN_TABLE,
}
 
 
def evaluate(gamestate):
    if gamestate.checkmate:
        return - CHECKMATE_SCORE if gamestate.white_to_move else CHECKMATE_SCORE
    if gamestate.stalemate:
        return STALEMATE_SCORE
    score = 0
    board = gamestate.board
    for row in range(8):
        for col in range(8):
            square = board[row][col]
            if square == '--':
                continue
            color = square[0]
            piece_type = square[1] 
 
            value = 0
            if piece_type in PIECE_VALUE:
                value += PIECE_VALUE[piece_type]
            table = PIECE_SQUARE_TABLES.get(piece_type)
            if table is not None:
                if color == 'w':
                    value += table[row][col] * 0.1
                else:
                    value += table[7 - row][col] * 0.1
            score += value if color == 'w' else -value
    return score
    turn_multiplier = 1 if gs.white_to_move else -1

    opponent_MinMax_score = CHECKMATE_SCORE
    best_player_move = None
    for player_move in valid_moves:
        try: 
            gs.make_move(player_move)
            opponent_moves = gs.get_valid_moves()
            opponent_Max_score= -CHECKMATE_SCORE
            for opponent_move in opponent_moves:
                try:
                    gs.make_move(opponent_move)
                    score = -evaluate(gs)*turn_multiplier
                    if score > opponent_Max_score:
                        opponent_Max_score = score
                finally:
                    gs.undo_move()
            if opponent_MinMax_score>opponent_Max_score:
                opponent_MinMax_score = opponent_Max_score
                best_player_move = player_move
                
        finally:
            gs.undo_move()

    return best_player_move


def call_negamax(gs,valid_moves): #helper method for minmax(verstappen)
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    # minmax(gs,valid_moves,DEPTH,gs.white_to_move)
    negamax_alpha_beta(gs,valid_moves,DEPTH,-CHECKMATE_SCORE,CHECKMATE_SCORE,1 if gs.white_to_move else -1)
    return next_move

def minmax(gs,valid_moves,depth,white_to_move):
    global next_move
    if depth == 0:
        return evaluate(gs)
    if white_to_move:
        max_score = -CHECKMATE_SCORE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = minmax(gs,next_moves,depth-1,False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE_SCORE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = minmax(gs,next_moves,depth-1,True)
            if score<min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

def negamax(gs,valid_moves,depth,turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * evaluate(gs)
    
    max_score = -CHECKMATE_SCORE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score  = -negamax(gs,next_moves,depth-1,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score

def negamax_alpha_beta(gs,valid_moves,depth,alpha,beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * evaluate(gs)
    #implement move ordering 
    max_score = -CHECKMATE_SCORE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score  = -negamax_alpha_beta(gs,next_moves,depth-1,-beta,-alpha,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move

        gs.undo_move()
        if max_score > alpha: #pruning
            alpha = max_score
        if alpha >= beta:
            break
    return max_score
