import constants
from constants import ENEMY_NEXT_MOVE as move_1
import util

def predict_snakes(board, enemy_snakes):
    for snake in enemy_snakes:
        predict_moves(board, snake)

def predict_moves(board, snake, me, depth=2):
    if snake == me:
        return
    curr_pos = snake.head

    moves = board.safe_moves(curr_pos, ignored=[constants.MY_TAIL, constants.ENEMY_TAIL, constants.ENEMY_NEXT_MOVE, constants.ENEMY_MOVE_2])

    for pos in moves.values():
        if should_yield(board, snake, me, pos, 1, util.distance(me.head, pos)):
            board.board[pos] = constants.ENEMY_NEXT_MOVE
        moves2 = board.safe_moves(pos, ignored=[constants.MY_TAIL, constants.ENEMY_TAIL])
        for pos2 in moves2.values():
            if should_yield(board, snake, me, pos2, 2, util.distance(me.head, pos2)):
                board.board[pos2] = constants.ENEMY_MOVE_2

def should_yield(board, snake, me, pos, snake_dist, my_dist):
    """
    Identify if my snake can not get to the specified position before this other snake
    """
    if snake_dist > my_dist:
        return False # Ok, I definitely can get there first
    if snake_dist < my_dist:
        return True # Ok, he can get there first
    if snake_dist == my_dist:
        if snake_dist <= 1:
            return True
        if len(snake) >= len(me):
            return True
    return False
def predict_me(board, me, depth=2):
    start_pos = me.head
    board_copy = board.copy()

    moves = board.safe_moves(start_pos)

# make sure you don't accidentally predict your own snakes moves onto the common game board, or you will be back to moving at random
def predict_snake(board, snake, depth=2):
    """
    Predict where a snake could be depth moves from now
    """
    snake.prediction_board = board.board.copy()
    start = snake.head
    next_move_id = constants.ENEMY_NEXT_MOVE
    
    next_level = board.safe_moves(start, ignored=list(range(next_move_id, next_move_id+depth))) # store the the next

    for level in range(depth):
        curr_level = next_level
        next_level = dict()

        snake.prediction_board

# find the available moves that there is no way yourself or 
# anyone else can get to first
def availible_moves(board, pos, snake, curr_depth, ignored=[]):
    """
    Get the possible moves that are available to a particular snake from a position, ignoring the moves available to everyone else
    """
    return board.safe_moves(pos, ingored=ignored.extend(range(curr_depth, move_1 + board.prediction_depth)))

