from .robottype import RobotType

class Robot:
    def __init__(self, row, col, team, id, type=RobotType.PAWN):
        self.row = row
        self.col = col
        self.team = team
        self.id = id
        self.type = type
