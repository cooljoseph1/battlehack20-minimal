from .robottype import RobotType

class Robot:
    def __init__(self, row, col, team, id, type, runner):
        self.row = row
        self.col = col
        self.team = team
        self.id = id
        self.type = type
        self.runner = runner
