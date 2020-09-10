import moves
from util import get_pos

# TODO: Track all the snakes on the board from here rather than directly in Board.py
class SnakeTracker:
    def __init__(self, data):
        self.me = Snake(data['you'], is_you=True)
        self.snakes = []
        self.snakes.append(self.me)
        for snk in data['board']['snakes']:
            snake = Snake(snk)
            if snake != self.me:
                self.snakes.append(snake)
        
        self.teams = dict()
        for snake in self.snakes:
            squad = snake.squad
            if squad != "":
                if squad not in self.teams:
                    self.teams[squad] = []
                self.teams[squad].append(snake)
    
    # Is this snake my teammate?
    def are_teammates(self, snake1, snake2):
        if snake1.squad != "":
            return snake1.squad == snake2.squad
        else:
            return False
    
    def get_teammates(self, snake1):
        team = self.get_team(snake.squad)
        returned_snakes = []
        for snake2 in team:
            if snake1 != snake2:
                returned_snakes.append(snake2)
        return returned_snakes
    # return the snakes that are members of team: team_id
    def get_team(self, team_id):
        return list(self.teams[team_id])
    
    # get the snake with id: snake_id
    def get_snake(self, snake_id):
        for snake in snakes:
            if snake.snake_id == snake_id:
                return snake

# Snake: a class that represents a snake on the board
class Snake:
    def __init__(self, data, is_you=False, is_alive=True):
        self.snake_id = data['id']
        self.name = data['name']
        self.health = data['health']

        self.head = get_pos(data['head'])
        self.body = []
        for pos in data['body']:
            self.body.append(get_pos(pos))
        self.tail = get_pos(data['body'][-1])
        self.length = data['length']
        self.shout = data['shout']
        self.is_you = is_you
        self.is_alive = is_alive

        self.squad = ""
        self.is_squad_game = False
        if "squad" in data:
            self.squad = data['squad']
            if self.squad != "":
                self.is_squad_game = True
        self.move_hist = []

        # TODO: maybe make this more situation specific?
        # i.e., eliminate moves this snake can't possibly make,
        self.possible_moves = moves.get_moves(self.head)

        self.last_move = ""  # the last move this snake made
        self.last_pos = self.body[1]
        for name, move in moves.get_moves(self.last_pos).items():
            if move == self.head:
                self.last_move = name

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.body)

    def __eq__(self, other):
        if self.snake_id == other.snake_id:
            return True
        else:
            return False

    def me(self):
        return self.is_you

    def alive(self):
        return self.is_alive

    def on_my_team(self, snake):
        if not self.is_squad_game:
            return False
        if snake.squad == self.squad:
            return True
        else:
            return False
