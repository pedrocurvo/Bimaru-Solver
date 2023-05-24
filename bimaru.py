# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 102:
# 102716 Pedro M. P. Curvo
# 00000 Nome2
import itertools
import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        if BimaruState.state_id == 0:
            self.ships = Bimaru.count_ships(board)
        else:
            self.ships = np.array([0, 0, 0, 0])
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def print(self):
        self.board.print()



class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    str_to_int = {'W': 1, 'T': 2, 'B': 4, 'L': 8, 'R': 16, 'M': 32, 'C': 64}
    int_to_str = {0: '.', 1: '.', 2: 't', 4: 'b', 8: 'l', 16: 'r', 32: 'm', 64: 'c'}
    hints = []
    water_hints = []

    def __init__(self, board: np.ndarray, col_number = None, row_number = None):
        """Construtor da classe. Recebe um array bidimensional
        (matriz) numpy com o conteúdo do tabuleiro."""
        self.board = board
        self.col_number = col_number
        self.row_number = row_number
        self.ships = np.array([0, 0, 0, 0])

    def __add__(self, other):
        """Soma de dois tabuleiros."""
        new_board = np.where(self.board != other.board, self.board + other.board, self.board)
        return Board(new_board, self.col_number, self.row_number)

    def __getitem__(self, x):
        return self.board[x]


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return None if self.board[row, col] == 0 else self.board[row, col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            return (
                (None, None)
                if self.board[row + 1][col] == 0
                else (None, self.board[row + 1][col])
            )
        elif row == 9:
            return (
                (None, None)
                if self.board[row - 1][col] == 0
                else (self.board[row - 1][col], None)
            )
        else:
            if self.board[row - 1][col] == 0:
                return (
                    (None, None)
                    if self.board[row + 1][col] == 0
                    else (None, self.board[row + 1][col])
                )
            elif self.board[row + 1][col] == 0:
                return self.board[row - 1][col], None
            return self.board[row - 1][col], self.board[row + 1][col]

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (
                (None, None)
                if self.board[row, col + 1] == 0
                else (None, self.board[row, col + 1])
            )
        elif col == 9:
            return (
                (None, None)
                if self.board[row, col - 1] == 0
                else (self.board[row, col - 1], None)
            )
        else:
            if self.board[row, col - 1] == 0:
                return (
                    (None, None)
                    if self.board[row, col + 1] == 0
                    else (None, self.board[row, col + 1])
                )
            elif self.board[row][col + 1] == 0:
                return self.board[row, col - 1], None
            return self.board[row, col - 1], self.board[row, col + 1]

    def print(self):
        """Imprime o tabuleiro."""
        # Create a NumPy array representing the board
        board_array = np.empty((10, 10), dtype=str)
        for row, col in itertools.product(range(10), range(10)):
            if (row, col) in Board.hints:
                board_array[row, col] = Board.int_to_str[self.board[row, col]].upper()
            elif (row, col) in Board.water_hints:
                board_array[row, col] = 'W'
            else:
                board_array[row, col] = Board.int_to_str[self.board[row, col]]

        # Print the board
        print('\n'.join([''.join(row) for row in board_array]))

    @staticmethod
    def match_boards(board1, board2):
        """Verifies if two boards match."""
        test_board = board1 + board2
        if np.array_equal(test_board.board, board1.board):
            return False  # garante que os dois tabuleiros são diferentes ou que o board1 não contem já o board2

        # Check the number of ships per column and row
        matrix = np.where((test_board.board != 0) & (test_board.board != 1), 1, 0)
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)

        if np.any(col_compare > board1.col_number) or np.any(row_compare > board1.row_number):
            return False

        count_different = np.count_nonzero(~np.isin(test_board.board, [0, 1, 2, 4, 8, 16, 32, 64]))
        if count_different: 
            return False # garante que os valores do tabuleiro são válidos

        # Check below above special conditions
        for i in range(10):
            value_row, value_col = 10 - np.count_nonzero(test_board.board[i] == 1), 10 - np.count_nonzero(test_board.board[:, i] == 1)
            if value_col < board1.col_number[i] or value_row < board1.row_number[i]: return False


        # Other conditions
        coordinate_t = np.argwhere(board1.board == 2) # t
        coordinate_b = np.argwhere(board1.board == 4) # b
        coordinate_l = np.argwhere(board1.board == 8) # l
        coordinate_r = np.argwhere(board1.board == 16) # r
        for coordinate in coordinate_t:
            if coordinate[0] < 7 and board2.board[coordinate[0] + 1, coordinate[1]] == 1: return False
        for coordinate in coordinate_b:
            if coordinate[0] > 2 and board2.board[coordinate[0] - 1, coordinate[1]] == 1: return False
        for coordinate in coordinate_l:
            if coordinate[1] < 7 and board2.board[coordinate[0], coordinate[1] + 1] == 1: return False
        return not any(
            coordinate[1] > 2
            and board2.board[coordinate[0], coordinate[1] - 1] == 1
            for coordinate in coordinate_r
        )
    

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        # Creates the np array
        Board.hints.clear()
        Board.water_hints.clear()
        board = np.zeros((10, 10))
        # Read the first line of txt file
        line = sys.stdin.readline().split()
        row = np.array([int(x) for x in line[1:]])
        # Read the second line of txt file
        line = sys.stdin.readline().split()
        col = np.array([int(x) for x in line[1:]])
        # Number of Hints
        n_hints = int(sys.stdin.readline())
        # Read the hints
        if n_hints > 0:
            for _ in range(n_hints):
                line = sys.stdin.readline().split()
                board[int(line[1]), int(line[2])] = Board.str_to_int[line[3]]
                if line[3] == 'W':
                    Board.water_hints.append( (int(line[1]), int(line[2])))
                else:
                    Board.hints.append( ((int(line[1]), int(line[2]))))
        return Board(board, col, row)


class Bimaru(Problem):
    """ Class that represents the Bimaru Problem.

        Attributes:
        probabilistic_grid: A numpy array representing the probabilistic grid for ship placement. 
    """
    probabilistic_grid = np.array([
            [8.0, 11.5, 14.3, 15.9, 16.7, 16.7, 15.9, 14.3, 11.5, 8.0],
            [11.5, 14.3, 16.6, 17.8, 18.4, 18.4, 17.8, 16.6, 14.3, 11.5],
            [14.3, 16.6, 18.4, 19.4, 19.9, 19.9, 19.4, 18.4, 16.6, 14.3],
            [15.9, 17.8, 19.4, 20.3, 20.8, 20.8, 20.3, 19.4, 17.8, 15.9],
            [16.7, 18.4, 19.9, 20.8, 21.4, 21.4, 20.8, 19.9, 18.4, 16.7],
            [16.7, 18.4, 19.9, 20.8, 21.4, 21.4, 20.8, 19.9, 18.4, 16.7],
            [15.9, 17.8, 19.4, 20.3, 20.8, 20.8, 20.3, 19.4, 17.8, 15.9],
            [14.3, 16.6, 18.4, 19.4, 29.9, 19.9, 19.4, 18.4, 16.6, 14.3],
            [11.5, 14.3, 16.6, 17.8, 18.4, 18.4, 17.8, 16.6, 14.3, 11.5],
            [8.0, 11.5, 14.3, 15.9, 16.7, 16.7, 15.9, 14.3, 11.5, 8.0],
            ])
    


    def __init__(self, board: Board):
        """Creates the Initial State of the problem"""
        Bimaru.initial_fill(board)
        self.initial = BimaruState(board)
        self.expected_ships = np.array([4, 3, 2, 1])
        self.first_options = Bimaru.create_all_first_options(board)


    
    def actions(self, state: BimaruState):
        """It returns a list of actions for the given state. For the 1 and 4 lenght ship the actions are created here,
        since they are few. For the other ships, the actions are created in the creation of the self object, allowing
        for a faster execution. The only thing necessary for that intermidiate ship length is the boards match."""
        
        def matching_rows(row1, row2): 
            new_board= np.where(row1 != row2, row1 + row2, row1)
            if np.array_equal(new_board, row1): return False
            count_different = np.count_nonzero(~np.isin(new_board, [0, 1, 2, 4, 8, 16, 32, 64]))
            return count_different <= 0
        
        if state.ships[3] != self.expected_ships[3]:
            options = []
            for row_or_col in range(10):
                # Horizontals
                if board.row_number[row_or_col] >= 4:
                    for i in range(7):
                        test_row = np.zeros((1, 10))
                        test_row[0][i: 4 + i] = [8, 32, 32, 16]

                        if matching_rows(board.board[row_or_col], test_row[0]):
                            option_for_board = Board(np.zeros((10, 10)))
                            option_for_board.board[row_or_col] = test_row[0]
                            option_for_board.ships[3] += 1
                            Bimaru.fill_around_l(option_for_board, True, row_or_col, i)
                            Bimaru.fill_around_r(option_for_board, True, row_or_col, i + 4 - 1)
                            #Bimaru.fill_water_around_ship(option_for_board)
                            if Board.match_boards(board, option_for_board):
                                options.append(option_for_board)
                # Verticals
                if board.col_number[row_or_col] >= 4:
                    for i in range(7):
                        test_row = np.zeros((1, 10))
                        test_row[0][i: 4 + i] = [2, 32, 32, 4]
                        if matching_rows(board.board[:,row_or_col], test_row[0]):
                            option_for_board = Board(np.zeros((10, 10)))
                            option_for_board.board[:, row_or_col] = test_row[0]
                            option_for_board.ships[3] += 1
                            Bimaru.fill_around_t(option_for_board, True, i, row_or_col)
                            Bimaru.fill_around_b(option_for_board, True, i + 4 - 1, row_or_col)
                            #Bimaru.fill_water_around_ship(option_for_board)
                            if Board.match_boards(board, option_for_board):
                                options.append(option_for_board)
            return options

        if state.ships[2] != self.expected_ships[2]:
            return [
                option
                for option in self.first_options[3]
                if Board.match_boards(state.board, option)
            ]
        
        if state.ships[1] != self.expected_ships[1]:
            return [
                option
                for option in self.first_options[2]
                if Board.match_boards(state.board, option)
            ]

        if state.ships[0] != self.expected_ships[0]:
            options = []
            coordinates = np.argwhere(state.board.board == 0)
            for coordinate in coordinates:
                obj = Board(np.zeros((10, 10)))
                obj.board[coordinate[0], coordinate[1]] = 64
                Bimaru.fill_around_c(obj, True, coordinate[0], coordinate[1])
                obj.ships[0] += 1
                if Board.match_boards(state.board, obj): options.append(obj)
            return options

        

    def result(self, state: BimaruState, action):
        """Joins the action and the state. It adds the action board with the state board and then fills the water
        for the columns that have the maximum number of pieces in that row or column. Depending on the action, it
        also adds the ship of the action to the state ships, allowing for a faster execution."""
        new_board = state.board + action
        Bimaru.fill_water(new_board)
        new_state = BimaruState(new_board)
        new_state.ships = np.add(state.ships, action.ships)
        return new_state


    def goal_test(self, state: BimaruState):
        """Returns True if the state is a goal. It only needs to check if the number of ships is correct, since
        the actions created by the actions function are already valid boards. It allows for a faster execution."""
        return np.array_equal(state.ships, self.expected_ships)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        if not node.action: return 10
        common_values = np.where(node.action.board == node.parent.state.board.board, 1, 0)
        common_values = np.where(node.action.board == 1, 0, common_values) # added last
        h_common_values = np.sum(common_values)
        

        #matrix = np.where(node.state.board == 0, 0, Bimaru.probabilistic_grid)
        #matrix = np.where(node.state.board == 1, 0, matrix)
        matrix2 = np.where(node.action.board == 0, 0, Bimaru.probabilistic_grid)
        matrix2 = np.where(node.action.board == 1, 0, matrix2)
    
        #if h_common_values != 0: return 10 / np.sum(matrix2) / h_common_values
        return (1 + h_common_values) * np.sum(matrix2) * 10 / 100

    @staticmethod
    def initial_fill(board: Board):
        """Preenche com água as linhas e colunas que não contêm barcos."""
        # Fill rows and cols with no ships
        row_coordinates = np.argwhere(board.row_number == 0)
        col_coordinates = np.argwhere(board.col_number == 0)
        for coordinate in row_coordinates: board.board[coordinate[0]] = [1 for _ in range(10)]
        for coordinate in col_coordinates: board.board[:, coordinate[0]] = [1 for _ in range(10)]

        # Fill Waters around ships
        Bimaru.fill_water_around_ship(board)

        # Fill rows and cols with all pieces
        Bimaru.fill_water(board)

        # Terminal Pieces
        Bimaru.terminal_t(board)
        Bimaru.terminal_b(board)
        Bimaru.terminal_l(board)
        Bimaru.terminal_r(board)

        # Terminal Columns
        Bimaru.terminal_cols(board)
        Bimaru.terminal_rows(board)
        
        # Fill Waters around ships
        Bimaru.fill_water_around_ship(board)
        Bimaru.fill_water(board)
        Bimaru.perfect_spaces(board)

                

    @staticmethod
    def fill_water_around_ship(board: Board):
        """Preenche com água as posições em redor de um barco."""
        Bimaru.fill_around_c(board)
        Bimaru.fill_around_m(board)
        Bimaru.fill_around_t(board)
        Bimaru.fill_around_b(board)
        Bimaru.fill_around_l(board)
        Bimaru.fill_around_r(board)

    
    @staticmethod
    def count_ships(board: Board):
        """Conta o número de barcos de cada tipo presentes no tabuleiro."""
        ships = [0, 0, 0, 0]
        # Count Single Ships
        c_coords = np.argwhere(board.board == 64) #C
        ships[0] += len(c_coords)
        # Count Vertical Ships
        t_coords = np.argwhere(board.board == 2) #T
        for coordinate in t_coords:
            row, col = coordinate[0], coordinate[1]
            ship_length = 1
            for i in range(row + 1, row + 4):
                if i < 10 and board.board[i, col] == 32: #M
                    ship_length += 1
                elif i < 10 and board.board[i, col] == 4: #B
                    ship_length += 1
                    ships[ship_length - 1] += 1
                    break
                else: break
        # Count Horizontal Ships
        l_coords = np.argwhere(board.board == 8) #l
        for coordinate in l_coords:
            row, col = coordinate[0], coordinate[1]
            ship_length = 1
            for i in range(col + 1, col + 4):
                if i < 10 and board.board[row, i] == 32: #M
                    ship_length += 1
                elif i < 10 and board.board[row, i] == 16: #R
                    ship_length += 1
                    ships[ship_length - 1] += 1
                    break
                else: break
        return ships


    @staticmethod
    def fill_water(board: Board):
        valid_values = [0, 1]
        matrix = np.where(np.isin(board.board, valid_values), 0, 1)
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)


        columns = np.argwhere(col_compare == board.col_number)
        rows = np.argwhere(row_compare == board.row_number)
        for column in columns:
            col = column[0]
            board.board[:,col] = np.where(board.board[:,col] == 0, 1, board.board[:,col])
        for row in rows:
            row = row[0]
            board.board[row] = np.where(board.board[row] == 0, 1, board.board[row])
            

    @staticmethod
    def create_all_first_options(board: Board):
        """Cria todas as opções iniciais possíveis."""
        def matching_rows(row1, row2): 
            new_board= np.where(row1 != row2, row1 + row2, row1)
            count_different = np.count_nonzero(~np.isin(new_board, [0, 1, 2, 4, 8, 16, 32, 64]))
            return count_different <= 0

        options = { 2: [], 3: []}

        ship_lengths_horizontal = [2, 3]
        for row_or_col in range(10):
            # Horizontals
            for ship_length in ship_lengths_horizontal:
                if board.row_number[row_or_col] >= ship_length:
                    for i in range(11 - ship_length):
                        test_row = np.zeros((1, 10))

                        # Create the row with a ship
                        #if ship_length == 1: test_row[0][i] = 64 #c
                        #else:
                        test_row[0][i] = 8 #l
                        test_row[0][i+1:i+ship_length-1] = 32  # m
                        test_row[0][i+ship_length-1] = 16 #r

                        if matching_rows(board.board[row_or_col], test_row[0]):
                            option_for_board = Board(np.zeros((10, 10)))
                            option_for_board.board[row_or_col] = test_row[0]
                            option_for_board.ships[ship_length - 1] += 1
                            Bimaru.fill_around_l(option_for_board, True, row_or_col, i)
                            Bimaru.fill_around_r(option_for_board, True, row_or_col, i + ship_length - 1)
                            #Bimaru.fill_water_around_ship(option_for_board, activate_dual = True, vertical=False)
                            if Board.match_boards(board, option_for_board):
                                options[ship_length].append(option_for_board)
            # Verticals
                if board.col_number[row_or_col] >= ship_length:
                    for i in range(11 - ship_length):
                        test_row = np.zeros((1, 10))
                        test_row[0][i] = 2 #t
                        test_row[0][i+1:i+ship_length-1] = 32  # m
                        test_row[0][i+ship_length-1] = 4 #b
                        if matching_rows(board.board[:,row_or_col], test_row[0]):
                            option_for_board = Board(np.zeros((10, 10)))
                            option_for_board.board[:, row_or_col] = test_row[0]
                            option_for_board.ships[ship_length - 1] += 1
                            Bimaru.fill_around_t(option_for_board, True, i, row_or_col)
                            Bimaru.fill_around_b(option_for_board, True, i + ship_length - 1, row_or_col)
                           # Bimaru.fill_water_around_ship(option_for_board, activate_dual = True, horizontal= False)
                            if Board.match_boards(board, option_for_board):
                                options[ship_length].append(option_for_board)
        return options


    @staticmethod
    def fill_around_c(board: Board, coordinates = False, x=None, y=None):
        # Find Pieces
        coordinates_c = [(x, y)] if coordinates else np.argwhere(board.board == 64)
        for coordinate in coordinates_c:
            row, col = coordinate[0], coordinate[1]
            r_min, r_max = max(0, row - 1), min(10, row + 2)
            c_min, c_max = max(0, col - 1), min(10, col + 2)
            board.board[r_min:r_max, c_min:c_max] = np.where(board.board[r_min:r_max, c_min:c_max] != 64, 1, board.board[r_min:r_max, c_min:c_max])


    @staticmethod
    def fill_around_t(board: Board, coordinates=False, x=None, y=None):
        # Fill around T
        coordinates_t = [(x, y)] if coordinates else np.argwhere(board.board == 2)
        for coordinate in coordinates_t:
            row, col = coordinate[0], coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 3))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 2 and j != col or i < row): board.board[i, j] = 1 #w


    @staticmethod
    def fill_around_b(board: Board, coordinates=False, x=None, y=None):
        coordinates_b = [(x, y)] if coordinates else np.argwhere(board.board == 4)
        for coordinate in coordinates_b:
                row, col = coordinate[0], coordinate[1]
                row_range = range(max(0, row - 2), min(10, row + 2))
                col_range = range(max(0, col - 1), min(10, col + 2))
                for i, j in itertools.product(row_range, col_range):
                    if (board.board[i, j] != 4 and j != col or i > row): board.board[i, j] = 1 #w


    @staticmethod
    def fill_around_l(board: Board, coordinates=False, x=None, y=None):
        coordinates_l = [(x, y)] if coordinates else np.argwhere(board.board == 8)
        # Fill around L
        for coordinate in coordinates_l:
            row = coordinate[0]
            col = coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 3))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 8 and i != row or j < col): board.board[i, j] = 1 #w


    @staticmethod
    def fill_around_r(board: Board, coordinates = False, x = None, y = None):
        coordinates_r = [(x, y)] if coordinates else np.argwhere(board.board == 16)
        # Fill around R
        for coordinate in coordinates_r:
            row = coordinate[0]
            col = coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 2), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 16 and i != row or j > col): board.board[i, j] = 1 #w


    @staticmethod
    def fill_around_m(board: Board):
        # Find around M
        coordinates_m = np.argwhere(board.board == 32)
        # Fill around M
        for coordinate in coordinates_m:
            row, col = coordinate[0], coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if j != col and i != row: board.board[i, j] = 1 #w

            if row in [0, 9]:
                x = 1 if row == 0 else -1
                board.board[row + x, col] = 1
                if col == 1:
                    board.board[row, col - 1] = 8 # | _ m _ _ -> | l m _ _
                    if board.board[row, col + 2] == 1: board.board[row, col + 1] = 16 # | l m _ _ -> | l m r _

                elif col == 8:
                    board.board[row, col + 1] = 16 # _ _ m _ | -> # _ _ m r
                    if board.board[row, col - 2] == 1: board.board[row, col - 1] = 8 # w _ m _ | -> # w l m r
            if col in [0, 9]:
                x = 1 if col == 0 else -1
                board.board[row, col + x] = 1 
                if row == 1:
                    board.board[row - 1, col] = 2 # _ m _ _ -> t m _ _
                    if board.board[row + 2, col] == 1: board.board[row + 1, col] = 4 # _ m _ w -> t m b w
                elif row == 8:
                    board.board[row + 1, col] = 4 # _ m _ _ -> b m _ _
                    if board.board[row - 2, col] == 1: board.board[row - 1, col] = 2 # _ m _ w _ -> t m b w


    @staticmethod
    def terminal_t(board: Board):
        for row in range(10):
            for col in range(10):
                # Terminal T's
                if board.board[row, col] == 2:
                    two_below = row + 2
                    if two_below < 10:
                        if board.board[two_below, col] == 1:
                            board.board[row + 1][col] = 4 # t _ w -> t b w
                        elif board.board[two_below][col] == 4:
                            board.board[row + 1][col] = 32 # t _ b -> t m b
                        elif two_below + 1 < 10 and board.board[two_below][col] == 32:
                            board.board[row + 1][col] = 32 # t _ m _ -> t m m _
                            board.board[row + 2][col] = 4 # t m m _ -> t m m b
                    else:
                        board.board[row + 1][col] = 4 # t _ |  -> t b |


    @staticmethod
    def terminal_b(board: Board):
        for row in range(10):
            for col in range(10):
                # Terminal B's
                if board.board[row][col] == 4:
                    two_above = row - 2
                    if two_above >= 0:
                        if board.board[two_above][col] == 1:
                            board.board[row - 1][col] = 2 # b _ w -> b t w
                        elif board.board[two_above][col] == 2:
                            board.board[row - 1][col] = 32 # b _ t -> b m t
                        elif two_above - 1 >= 0 and board.board[two_above][col] == 32:
                            board.board[row - 1][col] = 32 # b _ m _ -> b m m _
                            board.board[row - 2][col] = 2 # b m m _ -> b m m t
                    else:
                        board.board[row - 1][col] = 2 # b _ |  -> b t |


    @staticmethod
    def terminal_l(board: Board):
        for row in range(10):
            for col in range(10):
                # Terminal L's
                if board.board[row][col] == 8:
                    two_right = col + 2
                    if two_right < 10:
                        if board.board[row][two_right] == 1:
                            board.board[row][col + 1] = 16 # l _ w -> l r w
                        elif board.board[row][two_right] == 16:
                            board.board[row][col + 1] = 32 # l _ r -> l m r
                        elif two_right + 1 < 10 and board.board[row][two_right] == 32:
                            board.board[row][col + 1] = 32 # l _ m _ -> l m m _
                            board.board[row][col + 2] = 16 # l m m _ -> l m m r
                    else:
                        board.board[row][col + 1] = 16 # l _ |  -> l r |


    @staticmethod
    def terminal_r(board: Board):
        for row in range(10):
            for col in range(10):
                # Terminal R's
                if board.board[row][col] == 16:
                    two_left = col - 2
                    if two_left >= 0:
                        if board.board[row][two_left] == 1:
                            board.board[row][col - 1] = 8 # r _ w -> r l w
                        elif board.board[row][two_left] == 8:
                            board.board[row][col - 1] = 32 # r _ l -> r m l
                        elif two_left - 1 >= 0 and board.board[row][two_left] == 32:
                            board.board[row][col - 1] = 32 # r _ m _ -> r m m _
                            board.board[row][col - 2] = 8 # r m m _ -> r m m l
                    else:
                        board.board[row][col - 1] = 8 # r _ |  -> r l |


    @staticmethod
    def terminal_rows(board: Board):
        # Terminal Rows
        for row in range(1, 9):
            matriz = np.where(board.board[row - 1] == 2, 1, 0)                          # t _ _ _ _ -> 1 0 0 0 0
            matriz = np.where(np.isin(board.board[row], [2, 4, 8, 16, 32, 64]), 1, matriz)  # _ _ _ _ c -> 0 0 0 0 1 -> 1 0 0 0 1
            matriz = np.where(board.board[row + 1] == 4, 1, matriz)                     # _ _ b _ _ -> 0 0 1 0 0 -> 1 0 1 0 1
            valor = np.sum(matriz) # 1 0 1 0 1 -> 3
            # TODO: if we have a left or right in the row 
            if valor == board.row_number[row]: # 3 == 3
                board.board[row] = np.where(matriz == 1, board.board[row], 1)   # t 1 _ _ _ _ _ _ _ _
                                                                                # _ 1 1 _ 1 c 1 _ _ _  -> _ 1 1 _ 1 c 1 1 1 1 
                                                                                # _ 1 1 b 1 1 1 _ _ _


    @staticmethod
    def terminal_cols(board: Board):
        # Terminal Columns
        for col in range(1, 9): 
            matriz = np.where(board.board[:, col - 1] == 8, 1, 0)                               # l _ _ _ _ -> 1 0 0 0 0
            matriz = np.where(np.isin(board.board[:, col], [2, 4, 8, 16, 32, 64]), 1, matriz)   # _ _ c _ _ -> 0 0 1 0 0 -> 1 0 1 0 0
            matriz = np.where(board.board[:, col + 1] == 16, 1, matriz)
            valor = np.sum(matriz)  # 1 0 1 0 1 -> 3

            if valor == board.col_number[col]:
                board.board[:, col] = np.where(matriz == 1, board.board[:, col], 1)


    @staticmethod
    def perfect_spaces(board: Board):

        for row in range(10):
            empty = np.count_nonzero(board.board[row] == 0)
            pieces = empty + np.count_nonzero(board.board[row] == 1)
            if empty == board.row_number[row] and pieces == 0:
                for i in range(7):
                    if np.array_equal(board.board[row][i: i + 4], [0, 0, 0, 0]):
                        print(empty, board.row_number[row])
                        print(board.board[row])
                        board.board[row][i: i + 4] = [8, 32, 32, 16]
                        Bimaru.fill_around_l(board, True, row, i)
                        Bimaru.fill_around_r(board, True, row, i + 3)
                        print(board.board)
                        break
                for i in range(8):
                    if np.array_equal(board.board[row][i: i + 3], np.array([0, 0, 0])):
                        board.board[row][i: i + 3] = [8, 32, 16]
                        Bimaru.fill_around_l(board, True, row, i)
                        Bimaru.fill_around_r(board, True, row, i + 2)
                for i in range(9):
                    if np.array_equal(board.board[row][i:i + 2], np.array([0, 0])):
                        board.board[row][i: i + 2] = [8, 16]
                        Bimaru.fill_around_l(board, True, row, i)
                        Bimaru.fill_around_r(board, True, row, i + 1)

        for col in range(10):
            empty = np.count_nonzero(board.board[:, col] == 0)
            pieces = empty + np.count_nonzero(board.board[:, col] == 1)
            if empty == board.col_number[col] and pieces == 0:
                for i in range(7):
                    if np.array_equal(board.board[:, col][i: i + 4], np.array([0, 0, 0, 0])):
                        board.board[:, col][i: i + 4] = [2, 32, 32, 4]
                        Bimaru.fill_around_t(board, True, i, col)
                        Bimaru.fill_around_b(board, True, i + 3, col)
                        break
                for i in range(8):
                    if np.array_equal(board.board[:, col][i: i + 3], np.array([0, 0, 0])):
                        board.board[:, col][i: i + 3] = [2, 32, 4]
                        Bimaru.fill_around_t(board, True, i, col)
                        Bimaru.fill_around_b(board, True, i + 2, col)
                for i in range(9):
                    if np.array_equal(board.board[:, col][i: i + 2], np.array([0, 0])):
                        board.board[:, col][i: i + 2] = [2, 4]
                        Bimaru.fill_around_t(board, True, i, col)







if __name__ == "__main__":
    board = Board.parse_instance()
    problem = Bimaru(board)
    #goal_node = depth_first_tree_search(problem)
    goal_node = astar_search(problem)
    goal_node.state.print()
