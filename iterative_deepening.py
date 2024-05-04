import datetime
from numpy import flip
import chess

class IterativeDeepening:

    def reverseArray(array): 
        return flip(array)

    pawnEvalWhite = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [ 1.0,  1.0,  2.0,  3.0,  6.0,  2.0,  1.0,  1.0],
    [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [ 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]

    pawnEvalBlack = reverseArray(pawnEvalWhite)

    knightEval = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]

    bishopEvalWhite = [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ]

    bishopEvalBlack = reverseArray(bishopEvalWhite)

    rookEvalWhite = [
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
    ]

    rookEvalBlack = reverseArray(rookEvalWhite)

    queenEval = [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ]

    kingEvalWhite = [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
        [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
    ]

    kingEvalBlack = reverseArray(kingEvalWhite)

    def iterative_deepening(board: chess.Board, depth, maximizingPlayer, max_time):
        best_move = None
        best_value = float('-inf') if maximizingPlayer else float('inf')
        start_time = datetime.datetime.now()

        for current_depth in range(1, depth + 1):
            value, move = IterativeDeepening.depth_limited_search(board, current_depth, maximizingPlayer, start_time, max_time)
            if (maximizingPlayer and value > best_value) or (not maximizingPlayer and value < best_value):
                best_value = value
                best_move = move
            if (datetime.datetime.now() - start_time).total_seconds() > max_time:
                break

        return best_move

    def depth_limited_search(board, depth, maximizing_player, start_time, max_time):
        if depth == 0 or (datetime.datetime.now() - start_time).total_seconds() > max_time or board.is_game_over():
            return IterativeDeepening.evaluate_board(board), None

        best_value = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in board.legal_moves:
            board.push(move)
            eval, _ = IterativeDeepening.depth_limited_search(board, depth - 1, maximizing_player, start_time, max_time)
            board.pop()

            if maximizing_player:
                if eval > best_value:
                    best_value = eval
                    best_move = move
            else:
                if eval < best_value:
                    best_value = eval
                    best_move = move

        return best_value, best_move


    def evaluationBoard(board):
        totalEvaluation = 0
        i = 0
        s = -1
        #while s >= 63:
        while  i <= 7 :
            j = 0
            while j <= 7:
                s += 1
                totalEvaluation += (IterativeDeepening.getPieceValue(str(board.piece_at(s)), i, j))
                j += 1

            i += 1
        
        #print('The number is: ',s)
        return totalEvaluation
    
    def evaluate_board(board: chess.Board):
        if board.is_game_over():
            return float('-inf') if board.turn else float('inf')
        
        node_evaluation = 0
        node_evaluation += IterativeDeepening.check_status(board, board.turn)
        node_evaluation += IterativeDeepening.evaluationBoard(board)
        node_evaluation += IterativeDeepening.checkmate_status(board, board.turn)
        node_evaluation += IterativeDeepening.good_square_moves(board, board.turn)
        return node_evaluation

    def getPieceValue(piece, x, y):
        if (piece == None or piece == 'None'):
            return 0
    
        absoluteValue = 0

        if (piece == 'P'):
            absoluteValue = 10 + IterativeDeepening.pawnEvalWhite[x][y]
            return  absoluteValue
        
        if (piece == 'p'):
            absoluteValue = 10 + IterativeDeepening.pawnEvalBlack[x][y]
            return  absoluteValue * -1
        
        if (piece == 'n'):
            absoluteValue = 30 + IterativeDeepening.knightEval[x][y]
            return  absoluteValue * -1
        
        if (piece == 'N'):
            absoluteValue = 30 + IterativeDeepening.knightEval[x][y]
            return  absoluteValue

        if (piece == 'b'):
            absoluteValue = 30 + IterativeDeepening.bishopEvalBlack[x][y]
            return  absoluteValue * -1

        if (piece == 'B'):
            absoluteValue = 30 + IterativeDeepening.bishopEvalWhite[x][y]
            return  absoluteValue

        if (piece == 'r'):
            absoluteValue = 50 + IterativeDeepening.rookEvalBlack[x][y]
            return  absoluteValue * -1

        if (piece == 'R'):
            absoluteValue = 50 + IterativeDeepening.rookEvalWhite[x][y]
            return  absoluteValue

        if (piece == 'q'):
            absoluteValue = 90 + IterativeDeepening.queenEval[x][y]
            return  absoluteValue * -1

        if (piece == 'Q'):
            absoluteValue = 90 + IterativeDeepening.queenEval[x][y]
            return  absoluteValue

        if (piece == 'k'):
            absoluteValue = 9000 + IterativeDeepening.kingEvalBlack[x][y]
            return  absoluteValue * -1

        if (piece == 'K'):
            absoluteValue = 9000 + IterativeDeepening.kingEvalWhite[x][y]
            return  absoluteValue

        print(f'unknow pice: {piece} in the interval: [{x}],[{y}]')
        return absoluteValue

    def checkmate_status(board: chess.Board, turn):
        if board.is_checkmate():
            # Return positive 'infinity' if opponent is checkmated, negative if the current player is checkmated
            return float('inf') if not turn else float('-inf')
        return 0

    def check_status(board: chess.Board, turn):
        black_evaluation = 0
        is_check = board.is_check()
        #turn = "black" if currently_player == False else "white"

        if turn:
            if (is_check):
                #print('check status white: True')
                black_evaluation += 10 #* node_evaluation
        else:
            if (is_check):
                #print('check status black: True')
                black_evaluation -= 10 #* node_evaluation

        return black_evaluation
    
    def good_square_moves(board: chess.Board, turn):
        node_evaluation = 0
        #turn = "black" if currently_player == False else "white"
        square_values = {"e4": 1, "e5": 1, "d4": 1, "d5": 1, "c6": 0.5, "d6": 0.5, "e6": 0.5, "f6": 0.5,
                        "c3": 0.5, "d3": 0.5, "e3": 0.5, "f3": 0.5, "c4": 0.5, "c5": 0.5, "f4": 0.5, "f5": 0.5}

        possible_moves = board.legal_moves
        for possible_move in possible_moves:
            move = str(possible_move)
            if turn:
                if move[2:4] in square_values:
                    node_evaluation += square_values[move[2:4]]
            else:
                if move[2:4] in square_values:
                    node_evaluation -= square_values[move[2:4]]
                    
        return node_evaluation