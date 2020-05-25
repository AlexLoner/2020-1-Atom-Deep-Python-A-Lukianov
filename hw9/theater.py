import numpy as np


# ------------------------------------------------------------------------------------------------
from gen_theater_date import gen_board


class Scoreboard:

    # --------------------------------------------------------------------------------------------
    def __init__(self, file):
        self.file = file
        self.board = self.build_board()

    # --------------------------------------------------------------------------------------------
    def __str__(self):
        return self.board.__str__()

    # --------------------------------------------------------------------------------------------
    def build_board(self):
        ar = []
        with open(self.file, 'r') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                ar.append([int(i) for i in line.strip().split()])
        return np.array(ar, dtype=np.int8)

    # --------------------------------------------------------------------------------------------
    def empty_places(self):
        return len(np.where(self.board == 0)[0])

    # --------------------------------------------------------------------------------------------
    def check_place(self, row, column):
        return "Empty" if self.board[row, column] == 0 else "Engaged"


if __name__ == "__main__":

    gen_board((4, 4))
    file = 'data/theater/test.txt'
    my_board = Scoreboard(file)

    print(my_board)
    print(my_board.empty_places())
    print(my_board.check_place(1, 1))
    print(my_board.check_place(2, 2))
