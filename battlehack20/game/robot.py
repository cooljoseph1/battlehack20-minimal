from .robottype import RobotType

class Robot:
    def __init__(self, row, col, team, type=RobotType.PAWN):
        self.type = type
        self.row = row
        self.col = col
        self.team = team
