from random import randint
import pickle


def swap_rows(field):
    row1 = randint(0, 1)
    row2 = row1 + 1
    k = randint(0, 2)
    row1, row2 = map(lambda x: x + 3 * k, [row1, row2])
    tmp = field[row1]
    field[row1] = field[row2]
    field[row2] = tmp


def swap_cols(field):
    col1 = randint(0, 1)
    col2 = col1 + 1
    k = randint(0, 2)
    col1, col2 = map(lambda x: x + 3 * k, [col1, col2])
    for i in range(9):
        tmp = field[i][col1]
        field[i][col1] = field[i][col2]
        field[i][col2] = tmp


def transposition(field):
    for i in range(9):
        for j in range(9):
            tmp = field[i][j]
            field[i][j] = field[j][i]
            field[j][i] = tmp


class Session:
    def __init__(self):
        self.state = None
        self.stage = None
        self.field = None
        self.n = None

    def set_field(self, n):
        self.n = n
        self.field = [[((j * 3 + j // 3 + i) % 9 + 1) for i in range(9)] for j in range(9)]
        cnt = 0
        while cnt < 81 - n:
            i = randint(0, 8)
            j = randint(0, 8)
            if self.field[i][j] != 0:
                self.field[i][j] = 0
                cnt += 1
        for i in range(randint(15, 30)):
            swap_cols(self.field)
        for i in range(randint(15, 30)):
            swap_rows(self.field)
        for i in range(randint(0, 1)):
            transposition(self.field)

    def print_field(self):
        print("   ", end='')
        for i in range(9):
            print("[{}]".format(i+1)+(" " if (i + 1) % 3 == 0 else ""), end='')
        print("")
        for i in range(9):
            print("[{}]".format(i+1), end=' ')
            for j in range(9):
                print(self.field[i][j], ("|" if (j + 1) % 3 == 0 else ""), end=' ')
            print(('\n    ' + "-" * 28) if (i + 1) % 3 == 0 else "")

    def get_num(self, i, j, n):
        if self.field[i-1][j-1] == 0:
            self.field[i-1][j-1] = n
            return True
        else:
            return False

    def check_sol(self):
        flag = True
        for row in self.field:
            if len(set(row)) != 9:
                flag = False
        for i in range(9):
            set_arr = set([self.field[j][i] for j in range(9)])
            if len(set_arr) != 9:
                flag = False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                set_arr = []
                arr = [row[j:(j+3)] for row in session.field[i:(i+3)]]
                for row in arr:
                    set_arr += list(row)
                if len(set(set_arr)) != 9:
                    flag = False
        return flag

    def empty_cell(self):
        return sum([self.field[i][j] == 0 for i in range(9) for j in range(9)])

    def save_game(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.field, f)

    def load_game(self):
        with open('data.pickle', 'rb') as f:
            self.field = pickle.load(f)

    @staticmethod
    def clear():
        print('\n' * 100)


def find_next(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == 0:
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def is_available(field, i, j, k):
    check_row = all([k != field[i][x] for x in range(9)])
    if check_row:
        check_column = all([k != field[x][j] for x in range(9)])
        if check_column:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            x_sec, y_sec = 3 * (i // 3), 3 * (j // 3)  # floored quotient should be used here.
            for x in range(x_sec, x_sec + 3):
                for y in range(y_sec, y_sec + 3):
                    if field[x][y] == k:
                        return False
            return True
    return False


def sudoku_solver(field, i=0, j=0):
    i, j = find_next(field, i, j)
    if i == -1:
        return True
    for k in range(1, 10):
        if is_available(field, i, j, k):
            field[i][j] = k
            if sudoku_solver(field, i, j):
                return True
            # Undo the current cell for backtracking
            field[i][j] = 0
    return False


session = Session()
session.clear()
session.state = input("Enter 'ai' to solve automatically or\n"
                        "Enter 'play' to start the game:\n")
session.clear()
if session.state == "play":
    session.stage = input("Enter 'new' to start new game or\n"
                          "Enter 'load' to load game:\n")
    session.clear()
    if session.stage == 'new':
        session.set_field(int(input("Enter the number of prompts:\n")))
        session.clear()
        session.print_field()
        print("Amount of empty cells: {}".format(session.empty_cell()))
    elif session.stage == 'load':
        session.load_game()
        session.clear()
        session.print_field()
        print("Game loaded")
        print("Amount of empty cells: {}".format(session.empty_cell()))
    while True:
        inp = input("Enter 'end' to end the game or\n"
                    "Enter 'save' to save the game, or\n"
                    "Enter <<row column number>> to put the number on the field:\n")
        if inp == 'save':
            session.save_game()
            session.clear()
            session.print_field()
            print("Game saved")
            print("Amount of empty cells: {}".format(session.empty_cell()))
        elif inp == 'end':
            session.clear()
            if (input("Game is not finished. Do you want to save the game?\n"
                  "Enter 'yes' to save the game, or\n"
                  "Enter 'no' to end the game:\n") == 'yes'):
                session.clear()
                session.save_game()
                print("Game saved")
                input("Put 'Enter' to end the game:\n")
            break
        else:
            inp = list(map(lambda x: int(x), inp.split(' ')))
            if session.get_num(inp[0], inp[1], inp[2]):
                session.clear()
                session.print_field()
                print("Amount of empty cells: {}".format(session.empty_cell()))
            else:
                session.clear()
                session.print_field()
                print("You can't change the filled cell. Choose not filled cell.")
                print("Amount of empty cells: {}".format(session.empty_cell()))
    session.clear()
    if session.empty_cell() != 0:
        print("Game was not completed")
    else:
        if session.check_sol():
            print("You won the game")
        else:
            print("You lost the game")
elif session.state == "ai":
    session.set_field(int(input("Enter the number of prompts:\n")))
    session.clear()
    session.print_field()
    print("Amount of empty cells: {}".format(session.empty_cell()))
    input("Put 'Enter' to win the game:\n")
    session.clear()
    sudoku_solver(session.field)
    session.print_field()
