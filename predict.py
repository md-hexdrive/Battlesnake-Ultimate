# predict.py, predict the enemy's future moves
import util

class Predict:
    
    def __init__(self, board, depth=2):
        self.board = board
        self.me = board.me
        self.snakes = board.get_enemy_snakes()
        self.depth = depth # set the search depth
        
        self.prediction_board = board.board.copy()
        
    
    def predict_snake(self, snake):
        pos = util.get_pos(snake.head)
        x, y = pos
        
        minX, minY = x-self.depth, y-self.depth
        maxX, maxY = x+self.depth, y+self.depth
        
        for X in range(minX, maxX+1):
            for Y in range(minY, maxY+1):
                if board.in_bounds(X,Y) and is_snake_move(snake, x, y):
                    self.
    
    def place_move(self, snake, head, pos):
        head = util.get_pos(head)
        pos = util.get_pos(head)
        dist = util.distance(head, pos)
        
        self.prediction_board[x,y] = 
    # can a snake move to this Position?
    def is_snake_move(self, snake, x, y=None):
        x, y = get_pos(x,y)
        return True # TODO: Make this more intelligent?
        
        