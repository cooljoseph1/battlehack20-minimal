import time
import sys
import datetime

from ..game.team import Team

class BasicViewer:
    def __init__(self, board_size, board_states):
        self.board_size = board_size
        self.board_states = board_states

    def play(self, delay=0.5, keep_history=False):
        print('')

        for state_index in range(len(self.board_states)):
            self.view(state_index)
            time.sleep(delay)

        self.view(-1)

    def play_synchronized(self, poison_pill, delay=0.5):
        print('')
        
        state_index = 0
        last_time = datetime.datetime.now().timestamp()
        while state_index < len(self.board_states) or not poison_pill.is_set():
            while len(self.board_states) <= state_index or datetime.datetime.now().timestamp() - last_time < delay:
                time.sleep(0.1)
            self.view(state_index)
            last_time = datetime.datetime.now().timestamp()
            state_index += 1
    
    def view(self, index=-1):
        print(self.view_board(self.board_states[index]))

    def view_board(self, board):
        new_board = ''
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j]:
                    new_board += '[' + str(board[i][j]) + '] '
                else:
                    new_board += '[    ] '
            new_board += '\n'
        return new_board
