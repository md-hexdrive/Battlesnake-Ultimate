from board import Board
import collision_avoidance
import moves
import random
import flood_fill
import constants
import util
import goto
import tail_chasing


# define the snake's behaviour
def snake_behaviour(data):
    hunt_food = True  # change this back to true later

    # change this depending on how far ahead the snake should look
    prediction_depth = 2

    board = Board(data, prediction_depth)
    me = board.me
    curr_pos = me.head

    possible_moves = search_for_moves(board, curr_pos)

    ignored = []
    # follow enemy tail if no other options exist
    """
    if len(possible_moves) == 0:
        ignored.extend([constants.MY_TAIL, constants.ENEMY_TAIL])
        returned_moves = search_for_moves(
            board, curr_pos, ignored=ignored)
        for name, move in returned_moves.values():
            snake = board.get_snake_at(move)
            if snake == None:
                continue
            if snake.is_full_length:  #len(snake.body) == snake.length and
                possible_moves[name] = move
    """

    # move into possible enemy next move if necessary
    if len(possible_moves) == 0:
        ignored.extend([constants.ENEMY_MOVE_2])
        possible_moves = search_for_moves(
            board, curr_pos, ignored=ignored)
        hunt_food = False  # don't hunt for food in this situation
    # move into possible enemy next move if necessary
    if len(possible_moves) == 0:
        ignored.extend([constants.ENEMY_NEXT_MOVE])
        possible_moves = search_for_moves(
            board,
            curr_pos,
            ignored=ignored)
        hunt_food = False  # don't hunt for food in this situation

    move = None
    # if only one move if possible, return it
    if len(possible_moves) == 1:
        move = moves.pick_move(possible_moves)
        return move
    # look for food, if I should do that now
    if hunt_food and len(possible_moves) > 0 and eat_food(
            board, possible_moves):
        move = goto.find_food(board, curr_pos, possible_moves)
    else:
        possible_moves = avoid_food(board, possible_moves)
    
    # pick a random safe move
    if len(possible_moves) > 0 and move == None:
        move = moves.pick_move(possible_moves)
    # if no safe moves are possible, pick a random move to avoid errors
    if move == None:
        print("No safe move possible, picking random move", move)
        move = random.choice(moves.all_moves())
    return move


# find possible moves to make from your current position
def search_for_moves(board, curr_pos, ignored=[]):
    possible_moves = board.safe_moves(curr_pos, ignored=ignored)
    print(possible_moves)
    space_per_direction, surroundings_per_direction, available_spaces_per_direction = flood_fill.compare_moves(
        board, curr_pos, possible_moves, ignored)

    returned_moves = tail_chasing.tail_chase(
        board,
        curr_pos,
        possible_moves,
        space_per_direction,
        surroundings_per_direction,
        available_spaces_per_direction,
        ignored=ignored)
    if len(returned_moves) > 0:
        return returned_moves

    if len(possible_moves) > 1:
        possible_moves = flood_fill.select_roomiest_moves(
            board,
            curr_pos,
            possible_moves,
            space_per_direction,
            surroundings_per_direction,
            available_spaces_per_direction,
            ignored=ignored)

    return possible_moves


# Should I eat Food?
def eat_food(board, possible_moves):
    #snakes =
#    for snake in board.get_enemy_snakes():
#        if len(snake) > len(board.me) /2:

    if board.me.health < 99:
        return True
    else:
        return False

def avoid_food(board, possible_moves):
    returned_moves = dict()
    if not eat_food(board, possible_moves):
        for name, move in possible_moves.items():
            if not board.is_food(move):
                returned_moves[name] = move
    if len(returned_moves) > 0:
        return returned_moves
    return possible_moves