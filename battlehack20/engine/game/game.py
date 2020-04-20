import random
import traceback
from .constants import GameConstants
from ..container.runner import Runner
from .robot import Robot
from .robottype import RobotType
from .team import Team

class Game:
    def __init__(self, code, board_size=GameConstants.BOARD_SIZE, max_rounds=GameConstants.MAX_ROUNDS, 
                 seed=GameConstants.DEFAULT_SEED, sensor_radius=2, debug=False):
        
        random.seed(seed)

        self.code = code

        self.debug = debug
        self.running = True
        self.winner = None

        self.robot_count = 0
        self.queue = {}
        self.leaders = []

        self.sensor_radius = sensor_radius
        self.board_size = board_size
        self.board = [[None] * self.board_size for _ in range(self.board_size)]
        self.round = 0
        self.max_rounds = max_rounds

        self.robot = None # Robot that is currently doing a turn
        self.shared_methods = {"Team": Team,
                            "RobotType": RobotType,
                            "log": self.log,
                            "get_board_size": self.get_board_size,
                            "get_bytecode": self.get_bytecode,
                            "get_team": self.get_team,
                            "get_type": self.get_type,
                            "check_space": self.check_space}
        self.overlord_methods = {"get_board": self.get_board,
                                 "spawn": self.spawn}
        self.pawn_methods = {"capture": self.capture,
                             "get_location": self.get_location,
                             "move_forward": self.move_forward,
                             "sense": self.sense}
        self.overlord_methods.update(self.shared_methods)
        self.pawn_methods.update(self.shared_methods)

        self.new_robot(None, None, Team.WHITE, RobotType.OVERLORD)
        self.new_robot(None, None, Team.BLACK, RobotType.OVERLORD)

        
        self.board_states = []

    def turn(self):
        self.round += 1

        if self.round > self.max_rounds:
            self.check_over()

        for i in range(self.robot_count):
            if i in self.queue:
                self.robot = self.queue[i]

                try:
                    self.robot.runner.do_turn()
                except Exception as e:
                    if self.debug:
                        traceback.print_exc()
                self.check_over()

        if self.running:
            self.queue[0], self.queue[1] = self.queue[1], self.queue[0] # Alternate spawn order of Overlords
            self.board_states.append([row[:] for row in self.board])

    def new_robot(self, row, col, team, robot_type):
        methods = self.overlord_methods if robot_type == RobotType.OVERLORD else self.pawn_methods
        code = self.code[0] if team == Team.WHITE else self.code[1]
        runner = Runner(code, methods)
        
        robot = Robot(row, col, team, self.robot_count, robot_type, runner)
        
        self.queue[robot.id] = robot
        if robot.type != RobotType.OVERLORD:
            self.board[robot.row][robot.col] = robot
        
        self.robot_count += 1

    def delete_robot(self, i):
        robot = self.queue[i]
        if robot.type != RobotType.OVERLORD:
            self.board[robot.row][robot.col] = None
        del self.queue[i]

    def is_on_board(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def check_over(self):
        white, black = 0, 0
        for col in range(self.board_size):
            if self.board[0][col] and self.board[0][col].team == Team.BLACK: black += 1
            if self.board[self.board_size - 1][col] and self.board[self.board_size - 1][col].team == Team.WHITE: white += 1

        # End the game in the case of three turns where nothing changes
        #if self.round >= 4 and self.board_states[-1] == self.board_states[-2] == self.board_states[-3]:
        #    self.round = self.max_rounds + 1
        
        if self.round > self.max_rounds:
            self.running = False
            i = 0
            while white == black and i < self.board_size - 1:
                i += 1
                white, black = 0, 0
                for col in range(self.board_size):
                    if self.board[i][col] and self.board[i][col].team == Team.BLACK: black += 1
                    if self.board[self.board_size - 1 - i][col] and self.board[self.board_size - 1 - i][col].team == Team.WHITE: white += 1
            if white > black:
                self.winner = Team.WHITE
            elif white < black:
                self.winner = Team.BLACK
            else:
                self.winner = random.choice([Team.WHITE, Team.BLACK])

        if white >= (self.board_size + 1) // 2:
            self.running = False
            self.winner = Team.WHITE

        if black >= (self.board_size + 1) // 2:
            self.running = False
            self.winner = Team.BLACK

        if not self.running:
            self.board_states.append([row[:] for row in self.board])
            self.process_over()

    def process_over(self):
        """
        Helper method to process once a game is finished (e.g. deleting robots)
        """
        for i in range(self.robot_count):
            if i in self.queue:
                self.delete_robot(i)

    ### GENERAL METHODS ###
    def log(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)
    
    def get_board_size(self):
        return self.board_size

    def get_bytecode(self):
        return 1000000

    def get_team(self):
        return self.robot.team

    def get_type(self):
        return self.robot.type
    
    def check_space(self, row, col):
        return self.board[row][col].team if self.board[row][col] else False

    ### OVERLORD METHODS ###
    def get_board(self):
        return [[robot.team if robot else None for robot in row] for row in self.board]
    
    def spawn(self, row, col):
        self.new_robot(row, col, self.robot.team, RobotType.PAWN)
    
    ### PAWN METHODS ###
    
    def capture(self, new_row, new_col):
        self.delete_robot(self.board[new_row][new_col].id)
        self.board[new_row][new_col] = self.robot
        self.board[self.robot.row][self.robot.col] = None
        self.robot.row = new_row
        self.robot.col = new_col

    def get_location(self):
        return self.robot.row, self.robot.col

    def move_forward(self):
        if self.robot.team == Team.WHITE:
            new_row, new_col = self.robot.row + 1, self.robot.col
        else:
            new_row, new_col = self.robot.row - 1, self.robot.col
            
        self.board[new_row][new_col] = self.robot
        self.board[self.robot.row][self.robot.col] = None
        self.robot.row = new_row
        self.robot.col = new_col

    def sense(self):
        robots = []
        for new_row in range(self.robot.row - self.sensor_radius, self.robot.row + self.sensor_radius + 1):
            for new_col in range(self.robot.col - self.sensor_radius, self.robot.col + self.sensor_radius + 1):
                if new_row == self.robot.row and new_col == self.robot.col:
                    continue
                if not self.is_on_board(new_row, new_col):
                    continue
                if self.board[new_row][new_col]:
                    robots.append((new_row, new_col, self.board[new_row][new_col].team))
        return robots
