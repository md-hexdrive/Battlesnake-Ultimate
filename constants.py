import util

"""
Constants used to define what is located at a particular
position on the board
"""
FREE_SPACE      = 0
FOOD            = 1
SAFE_SPACE      = 2
HAZARD          = 3

MY_HEAD         = 4
MY_BODY         = 5
MY_TAIL         = 6

ENEMY_HEAD      = 7
ENEMY_BODY      = 8
ENEMY_TAIL      = 9
ENEMY_NEXT_MOVE = 10

ENEMY_MOVE_2    = 11
ENEMY_MOVE_3    = 12
ENEMY_MOVE_4    = 14

# Put all enemy move constants in an array to keep track of them all in one place
ENEMY_MOVES = [ENEMY_NEXT_MOVE, ENEMY_MOVE_2, ENEMY_MOVE_3, ENEMY_MOVE_4]

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

