import chess
from math import log, sqrt, e, inf
from numpy import flip

class Node:
    def __init__(self, state=None):
        self.state = state if state is not None else chess.Board()
        self.children = set()
        self.parent = None
        self.N = 0  # Total number of visits to this node
        self.n = 0  # Number of visits to this node from current traversal
        self.v = 0  # Value of the node

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


def ucb1(curr_node):
    # Upper Confidence Bound calculation for node selection
    return curr_node.v + 2 * (sqrt(log(curr_node.N + e + (10 ** -6)) / (curr_node.n + (10 ** -10))))


def evaluate_board(board):
    totalEvaluation = 0
    i = 0
    s = -1
    # while s >= 63:
    while i <= 7:
        j = 0
        while j <= 7:
            s += 1
            totalEvaluation += (getPieceValue(str(board.piece_at(s)), i, j))
            j += 1

        i += 1

    # print('The number is: ',s)
    return totalEvaluation

def getPieceValue(piece, x, y):
    if (piece == None or piece == 'None'):
        return 0

    absoluteValue = 0

    if (piece == 'P'):
        absoluteValue = 10 + pawnEvalWhite[x][y]
        return absoluteValue

    if (piece == 'p'):
        absoluteValue = 10 + pawnEvalBlack[x][y]
        return absoluteValue * -1

    if (piece == 'n'):
        absoluteValue = 30 + knightEval[x][y]
        return absoluteValue * -1

    if (piece == 'N'):
        absoluteValue = 30 + knightEval[x][y]
        return absoluteValue

    if (piece == 'b'):
        absoluteValue = 30 + bishopEvalBlack[x][y]
        return absoluteValue * -1

    if (piece == 'B'):
        absoluteValue = 30 + bishopEvalWhite[x][y]
        return absoluteValue

    if (piece == 'r'):
        absoluteValue = 50 + rookEvalBlack[x][y]
        return absoluteValue * -1

    if (piece == 'R'):
        absoluteValue = 50 + rookEvalWhite[x][y]
        return absoluteValue

    if (piece == 'q'):
        absoluteValue = 90 + queenEval[x][y]
        return absoluteValue * -1

    if (piece == 'Q'):
        absoluteValue = 90 + queenEval[x][y]
        return absoluteValue

    if (piece == 'k'):
        absoluteValue = 9000 + kingEvalBlack[x][y]
        return absoluteValue * -1

    if (piece == 'K'):
        absoluteValue = 9000 + kingEvalWhite[x][y]
        return absoluteValue

    print(f'unknow pice: {piece} in the interval: [{x}],[{y}]')
    return absoluteValue

def heuristic_moves(board):
    # This function filters and prioritizes moves that capture or give check
    moves = list(board.legal_moves)
    # Prioritize moves that result in capture or check
    # prioritized_moves = [move for move in moves if board.is_capture(move) or board.gives_check(move)]
    # Return prioritized moves first, if none, return all legal moves
    return moves

def mcts_pred(curr_node, is_over, is_white_turn):
    if is_over:
        return None  # Indicate that no move should be made because the game is over

    for move in curr_node.state.legal_moves:
        new_board = curr_node.state.copy()
        new_board.push(move)
        child_node = Node(new_board)
        child_node.parent = curr_node
        curr_node.children.add(child_node)

    for _ in range(1000):  # Adjust iterations based on performance needs
        child = expand(curr_node, is_white_turn)
        reward, state = heuristic_rollout(child)
        rollback(state, reward)

    best_child = max(curr_node.children, key=lambda x: x.v if is_white_turn else -x.v)

    if best_child.state.peek() in curr_node.state.legal_moves:
        return curr_node.state.san(best_child.state.peek())
    else:
        curr_node.children.remove(best_child)  # Remove the illegal move from consideration
        return mcts_pred(curr_node, is_over, is_white_turn)  # Recurse to find a legal move

def expand(curr_node, is_white_turn):
    # Use heuristic to limit moves during expansion
    if not curr_node.children:
        return curr_node

    heuristic_legal_moves = heuristic_moves(curr_node.state)
    for move in heuristic_legal_moves:
        new_board = curr_node.state.copy()
        new_board.push(move)
        child_node = Node(new_board)
        child_node.parent = curr_node
        curr_node.children.add(child_node)

    selected_node = max(curr_node.children, key=lambda x: ucb1(x) if is_white_turn else -ucb1(x))
    return expand(selected_node, not is_white_turn)

def heuristic_rollout(curr_node):
    while not curr_node.state.is_game_over():
        best_move = None
        best_value = float('-inf')
        for move in curr_node.state.legal_moves:
            curr_node.state.push(move)
            move_value = evaluate_board(curr_node.state)
            if move_value > best_value:
                best_move = move
                best_value = move_value
            curr_node.state.pop()
        curr_node.state.push(best_move)

    result = curr_node.state.result()
    if result == '1-0':
        return (1, curr_node)
    elif result == '0-1':
        return (-1, curr_node)
    else:
        return (0, curr_node)

def rollback(node, reward):
    # Backpropagation phase of MCTS, propagate the results back up the tree
    while node is not None:
        node.N += 1
        node.n += 1
        node.v += reward
        node = node.parent