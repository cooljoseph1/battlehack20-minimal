from .robottype import RobotType

class Robot:
    def __init__(self, row, col, team, id, type, runner):
        self.row = row
        self.col = col
        self.team = team
        self.id = id
        self.type = type
        self.runner = runner

    def __str__(self):
        team = 'B' if self.team.value else 'W'
        return '%s%3d' % (team, self.id)

    def __repr__(self):
        team = 'BLACK' if self.team.value else 'WHITE'
        return f'<ROBOT {self.id} {team}>'
