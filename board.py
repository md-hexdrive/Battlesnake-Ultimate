
import json
import numpy as np 

import moves
from snake import Snake
from util import get_pos, distance, directions
from constants import FREE_SPACE, FOOD, SAFE_SPACE, HAZARD, MY_HEAD, MY_BODY, MY_TAIL, ENEMY_HEAD, ENEMY_TAIL, ENEMY_BODY, ENEMY_NEXT_MOVE

class Board:
    def __init__(self, data):
        
        self.data = data
        
        self.width = data['board']['width']
        self.height = data['board']['height']
        
        
        self.board = np.zeros((self.width, self.height), dtype=np.int16)
        self.hazards = np.zeros((self.width, self.height), dtype=np.int16)
        self.healthmatrix = np.zeros((self.width, self.height), dtype=np.int16)
        self.lengthmatrix = np.zeros((self.width, self.height), dtype=np.int16)
        
        self.snakematrix = np.zeros((self.width, self.height), dtype=object)
        
        self.me = Snake(data['you'], is_you=True)
        self.snakes = dict()
        for snake in data['board']['snakes']:
            snk = Snake(snake)
            if snk == self.me:
                self.snakes[snake['id']] = self.me
            else:
                self.snakes[snake['id']] = snk
        
        self.process_board(data)

    def __getitem__(self, index):
        return self.board[index]
    
    def process_board(self, data):
        # load hazards
        self.load_hazards(data)
        
        # load food data
        for food in data['board']['food']:
            self.board[get_pos(food)] = FOOD
        
        # load enemy snakes
        for snake in self.snakes.values():
            if snake == self.me:
                self.load_me(snake) # load yourself
                continue
            on_same_team = self.me.on_my_team(snake)
            if not on_same_team:
                for pos in snake.body:
                    x, y = get_pos(pos)
                    self.board[x, y] = ENEMY_BODY
                    self.healthmatrix[x, y] = snake.health
                    self.lengthmatrix[x, y] = snake.length
                    self.snakematrix[x, y] = snake
                tail = get_pos(snake.tail)
                self.board[tail] = ENEMY_TAIL
            
            head = get_pos(snake.head)
            self.board[head] = ENEMY_HEAD
            if snake.length >= self.me.length or on_same_team:
                other_snake_moves = self.safe_moves(head)
                for move in other_snake_moves.values():
                    self.board[move] = ENEMY_NEXT_MOVE
            

    # load yourself
    def load_me(self, snake):
        for pos in snake.body:
            x, y = get_pos(pos)
            self.board[x, y] = MY_BODY
            self.healthmatrix[x, y] = snake.health
            self.lengthmatrix[x, y] = snake.length
            self.snakematrix[x, y] = snake.snake_id
        
        head = get_pos(snake.head)
        tail = get_pos(snake.tail)
        self.board[head] = MY_HEAD
        
        if len(snake.body) == snake.length and snake.length > 3 and snake.health < 100:
            return
        else:
            if self.board[tail] == FREE_SPACE:
                self.board[tail] = MY_TAIL
    
    def load_hazards(self, data):
        for hazard in data['board']['hazards']:
            x, y = get_pos(hazard)
            self.hazards[x, y] = HAZARD

    def safe_moves(self, x, y=None, ignored=[]):
        x, y = get_pos(x, y)
        possible_moves = moves.get_moves(x, y)
        returned_moves = dict()
    
        for name, move in possible_moves.items():
            if self.is_safe(move, ignored=ignored):
                returned_moves[name] = move
            else:
                continue
        return returned_moves
    
    def in_bounds(self, x, y=None):
        x, y = get_pos(x, y)
        if x in range(self.width) and y in range(self.height):
            return True
        else:
            return False

    def is_safe(self, x, y=None, ignored=[]):
        x, y = get_pos(x, y)
        
        if self.in_bounds(x, y):
            contents = self[x, y]
            if contents <= SAFE_SPACE or contents in ignored:
                return True
            else:
                return False
        else:
            return False
    

    def is_food(self, x, y=None):
        x, y = get_pos(x, y)
        if self[x, y] == FOOD:
            return True
        else:
            return False
    
    def is_hazard(self, x, y=None):
        x, y = get_pos(x, y)
        if self[x, y] == HAZARD:
            return True
        else:
            return False
    """
    Return the snake at x, y
    """
    def get_snake_at(self, x, y=None):
        x, y = get_pos(x, y)
        return self.snakematrix[x, y]
    
    """ Is there a snake at (x, y) ? """
    def is_snake_at(self, x, y=None):
        x, y = get_pos(x, y)
        if type(self.get_snake_at(x, y)) == type(Snake(self.data['you'])):
            return True
        else:
            return False

if __name__ == "__main__":
  with open("example_move.json") as file:
    data = json.load(file)
    board = Board(data)
    print(board.board)
    print(board.hazards)
    print(board.snakes)
    print(board.is_safe(0,0))
    print(board.snakematrix)
    print(board.is_snake_at(0,0))
    
    
