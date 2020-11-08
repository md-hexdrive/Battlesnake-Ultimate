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

    # follow enemy tail if no other options exist
    if len(possible_moves) == 0:
        returned_moves = search_for_moves(
            board, curr_pos, ignored=[constants.MY_TAIL, constants.ENEMY_TAIL])
        for name, move in returned_moves.values():
            snake = board.get_snake_at(move)
            if snake == None:
                continue
            if snake.is_full_length:  #len(snake.body) == snake.length and
                possible_moves[name] = move

    # move into possible enemy next move if necessary
    if len(possible_moves) == 0:
        possible_moves = search_for_moves(
            board, curr_pos, ignored=[constants.ENEMY_MOVE_2])
        hunt_food = False  # don't hunt for food in this situation
    # move into possible enemy next move if necessary
    if len(possible_moves) == 0:
        possible_moves = search_for_moves(
            board,
            curr_pos,
            ignored=[constants.ENEMY_NEXT_MOVE, constants.ENEMY_MOVE_2])
        hunt_food = False  # don't hunt for food in this situation

    if me.is_full_length: 
        for name, move in moves.get_moves(curr_pos).items():

            if move == me.tail:# and board[move] != constants.ENEMY_NEXT_MOVE:
                possible_moves[name] = move
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
        move = random.choice(moves.all_moves())
        print("No safe move possible, picking random move", move)

    return move


# find possible moves to make from your current position
def search_for_moves(board, curr_pos, ignored=[]):
    possible_moves = board.safe_moves(curr_pos, ignored=ignored)
    print(possible_moves)

    space_per_direction, surroundings_per_direction, available_spaces_per_direction = flood_fill.compare_moves(
        board, curr_pos, possible_moves, ignored)

    if len(possible_moves) > 0:
        roomiest_moves = flood_fill.select_roomiest_moves(
                    board,
                    curr_pos,
                    possible_moves,
                    space_per_direction,
                    surroundings_per_direction,
                    available_spaces_per_direction,
                    ignored=ignored)
            
        if max(space_per_direction.values()) >= len(board.me):
            print("going for roomiest moves", roomiest_moves)
            return roomiest_moves

        tail_chase_moves = tail_chasing.tail_chase(
            board,
            curr_pos,
            possible_moves,
            space_per_direction,
            surroundings_per_direction,
            available_spaces_per_direction,
            ignored=ignored)
        
        
        if len(tail_chase_moves) > 0:
            print("selecting tail-chasing moves", tail_chase_moves)
            return tail_chase_moves
        else:
            print("going for the most space available", roomiest_moves)
            return roomiest_moves
        """
        returned_moves = {}
        for move, pos in possible_moves.items():
            space = space_per_direction[move]
            if board.me.body[-space] in surroundings_per_direction[move]:
                print("tail should be accessible in the future with move", move)
                returned_moves[move] = pos
        
        if len(returned_moves) > 0:
            print("Tail should be accessible in the future if you make one of these moves", returned_moves)
            return returned_moves

    if len(possible_moves) > 0 and constants.ENEMY_NEXT_MOVE not in ignored and max(space_per_direction.values()) < len(board.me):
        print("Not enough room, ignoring", possible_moves)
        return {}
        """
    print("Moves:", possible_moves, "possible when ingnoring", ignored)
    return possible_moves


# Should I eat Food?
def eat_food(board, possible_moves):
    #snakes =
#    for snake in board.get_enemy_snakes():
#        if len(snake) > len(board.me) /2:


    if board.me.health <= 100:
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