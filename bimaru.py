# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 102:
# 00000 Pedro M. P. Curvo
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
        new_board= np.where(self.board != other.board, self.board + other.board, self.board)
        return Board(new_board, self.col_number, self.row_number)


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
            if self.board[row, col + 1] == 0:
                return None, None
            return None, self.board[row, col + 1]
        elif col == 9:
            if self.board[row, col - 1] == 0:
                return None, None
            return self.board[row, col - 1], None
        else:
            if self.board[row, col - 1] == 0:
                if self.board[row, col + 1] == 0:
                    return None, None
                return None, self.board[row, col + 1]
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
        if np.array_equal(test_board.board, board1.board): return False #garante que os dois tabuleiros são diferentes ou que o board1 não contem já o board2


        values = [0, 1, 2, 4, 8, 16, 32, 64]
        count_different = np.count_nonzero(~np.isin(test_board.board, values))
        if count_different > 0: return False #garante que os valores do tabuleiro são válidos

        # Check the number of ships per column and row
        matrix = np.where((test_board.board != 0) & (test_board.board != 1), 1, 0)
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)

        if np.any(col_compare > board1.col_number) or np.any(row_compare > board1.row_number): return False

        # Other conditions
        coordinate_t = np.argwhere(board1.board == 2) #t
        coordinate_b = np.argwhere(board1.board == 4) #b
        coordinate_l = np.argwhere(board1.board == 8) #l
        coordinate_r = np.argwhere(board1.board == 16) #r
        for i in range(len(coordinate_t)):
            if coordinate_t[i][0] < 7 and board2.board[coordinate_t[i][0] + 1, coordinate_t[i][1]] == 1: return False
        for i in range(len(coordinate_b)):
            if coordinate_b[i][0] > 2 and board2.board[coordinate_b[i][0] - 1, coordinate_b[i][1]] == 1: return False
        for i in range(len(coordinate_l)):
            if coordinate_l[i][1] < 7 and board2.board[coordinate_l[i][0], coordinate_l[i][1] + 1] == 1: return False
        return not any(
            coordinate_r[i][1] > 2
            and board2.board[coordinate_r[i][0], coordinate_r[i][1] - 1] == 1
            for i in range(len(coordinate_r))
        )
    
        #for i in range(len(coordinate_r)):
        #    if coordinate_r[i][1] > 2 and board2.board[coordinate_r[i][0]][coordinate_r[i][1] - 1] == 1: return False

        #return True
    

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
    normalization = np.sum(probabilistic_grid)
    


    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        Bimaru.fill_water_rows_cols(board)
        Bimaru.fill_water_around_ship(board)
        Bimaru.fill_water(board)
        self.initial = BimaruState(board)
        self.expected_ships = np.array([4, 3, 2, 1])
        #self.ships = Bimaru.count_ships(board)
        self.first_options = Bimaru.create_all_first_options(board)
        '''
        for row in self.initial.board.row_number:
            if row != 0 : Bimaru.probabilistic_grid[row] /= row
            else: Bimaru.probabilistic_grid[row] *= 0 
        for col in self.initial.board.col_number:
            if col != 0 : Bimaru.probabilistic_grid[col] /= col
            else: Bimaru.probabilistic_grid[col] *= 0
        '''



    
    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.ships[3] != self.expected_ships[3]:
            return self.first_options[4]
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
                matrix = np.zeros((10, 10))
                matrix[coordinate[0], coordinate[1]] = 64
                obj = Board(matrix)
                Bimaru.fill_water_around_ship(obj, activate_c = True)
                obj.ships[0] += 1
                if Board.match_boards(state.board, obj): options.append(obj)
            #np.random.shuffle(options)
            return options

            '''for option in self.first_options[1]:
                coordinate = np.argwhere(option.board == 64)[0]
                if state.board.board[coordinate[0], coordinate[1]] == 0:
                    options.append(option)
            '''

            return [
                option
                for option in options
                if Board.match_boards(state.board, option)
            ]

        

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = state.board + action
        Bimaru.fill_water(new_board)
        new_state = BimaruState(new_board)
        new_state.ships = np.add(state.ships, action.ships)
        return new_state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return np.array_equal(state.ships, self.expected_ships)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        if not node.action: return 10
        common_values = np.where(node.action.board == node.parent.state.board.board, 1, 0)
        h_common_values = np.sum(common_values)
        

        #matrix = np.where(node.state.board == 0, 0, Bimaru.probabilistic_grid)
        #matrix = np.where(node.state.board == 1, 0, matrix)
        matrix2 = np.where(node.action.board == 0, 0, Bimaru.probabilistic_grid)
        matrix2 = np.where(node.action.board == 1, 0, matrix2)
    
        #if h_common_values != 0: return 10 / np.sum(matrix2) / h_common_values
        return (1 + h_common_values) * np.sum(matrix2) * 10 / Bimaru.normalization
        return abs(100 - np.sum(matrix2) * 10)
        return 10 / np.sum(matrix2) / h_common_values
        return abs(100 - np.sum(matrix2) * 10)
        value = round(((np.sum(matrix) * 0.3 + np.sum(matrix2) * 0.7) * 10 / Bimaru.normalization - 3) * 100 )
        return 10 - (np.sum(matrix) * 0.3 + np.sum(matrix2) * 0.7) * 10 / Bimaru.normalization
        return 10 - value 

    @staticmethod
    def fill_water_rows_cols(board: Board):
        """Preenche com água as linhas e colunas que não contêm barcos."""
        row_coordinates = np.argwhere(board.row_number == 0)
        col_coordinates = np.argwhere(board.col_number == 0)
        for coordinate in row_coordinates:
            board.board[coordinate[0]] = [1 for _ in range(10)]
        for coordinate in col_coordinates:
            board.board[:, coordinate[0]] = [1 for _ in range(10)]


    @staticmethod
    def fill_water_around_ship(board: Board, activate_c = False, activate_dual = False):
        """Preenche com água as posições em redor de um barco."""
        # Find Pieces
        coordinates_c = np.argwhere(board.board == 64)
        if not activate_c:
            if not activate_dual:
                coordinates_m = np.argwhere(board.board == 32)
            coordinates_b = np.argwhere(board.board == 4)
            coordinates_t = np.argwhere(board.board == 2)
            coordinates_l = np.argwhere(board.board == 8)
            coordinates_r = np.argwhere(board.board == 16)
        # Fill around C
        for coordinate in coordinates_c:
            row, col = coordinate[0], coordinate[1]
            '''row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if board.board[i][j] != 64: board.board[i][j] = 1
            '''
            r_min, r_max = max(0, row - 1), min(10, row + 2)
            c_min, c_max = max(0, col - 1), min(10, col + 2)
            board.board[r_min:r_max, c_min:c_max] = np.where(board.board[r_min:r_max, c_min:c_max] != 64, 1, board.board[r_min:r_max, c_min:c_max])
        if activate_c: return

            

        
        # Fill around B
        for coordinate in coordinates_b:
            row, col = coordinate[0], coordinate[1]
            row_range = range(max(0, row - 2), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 4 and j != col or i > row): board.board[i, j] = 1 #w

        # Fill around T
        for coordinate in coordinates_t:
            row, col = coordinate[0], coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 3))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 2 and j != col or i < row): board.board[i, j] = 1 #w
        # Fill around L
        for coordinate in coordinates_l:
            row = coordinate[0]
            col = coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 3))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 8 and i != row or j < col): board.board[i, j] = 1 #w
        # Fill around R
        for coordinate in coordinates_r:
            row = coordinate[0]
            col = coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 2), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if (board.board[i, j] != 16 and i != row or j > col): board.board[i, j] = 1 #w
        if activate_dual: return
        # Fill around M
        for coordinate in coordinates_m:
            row, col = coordinate[0], coordinate[1]
            row_range = range(max(0, row - 1), min(10, row + 2))
            col_range = range(max(0, col - 1), min(10, col + 2))
            for i, j in itertools.product(row_range, col_range):
                if j != col and i != row: board.board[i, j] = 1 #w

            # Terminal M
            if row == 0: board.board[row + 1, col] = 1
            elif row == 9: board.board[row - 1, col] = 1
            if col == 0: board.board[row, col + 1] = 1
            elif col == 9: board.board[row, col - 1] = 1

    
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
            if np.array_equal(new_board, row1): return False
            values = [0, 1, 2, 4, 8, 16, 32, 64]
            count_different = np.count_nonzero(~np.isin(new_board, values))
            return count_different <= 0

        options = {1: [], 2: [], 3: [], 4: []}

        ship_lengths_horizontal = range(2, 5)
        for row_or_col in range(10):
            # Horizontals
            for ship_length in ship_lengths_horizontal:
                if board.row_number[row_or_col] >= ship_length:
                    for i in range(11 - ship_length):
                        if ship_length == 2: x = True
                        else: x = False
                        test_row = np.zeros((1, 10))

                        # Create the row with a ship
                        #if ship_length == 1: test_row[0][i] = 64 #c
                        #else:
                        test_row[0][i] = 8 #l
                        test_row[0][i+1:i+ship_length-1] = 32  # m
                        test_row[0][i+ship_length-1] = 16 #r

                        if matching_rows(board.board[row_or_col], test_row[0]):
                            np_matrix = np.zeros((10, 10))
                            np_matrix[row_or_col] = test_row[0]
                            option_for_board = Board(np_matrix)
                            option_for_board.ships[ship_length - 1] += 1
                            Bimaru.fill_water_around_ship(option_for_board, activate_dual=x)
                            if Board.match_boards(board, option_for_board):
                                options[ship_length].append(option_for_board)
            # Verticals
            #for ship_length in ship_lengths_vertical:
                if board.col_number[row_or_col] >= ship_length and ship_length > 1:
                    for i in range(11 - ship_length):
                        if ship_length == 2: x = True
                        else: x = False
                        test_row = np.zeros((1, 10))
                        test_row[0][i] = 2 #t
                        test_row[0][i+1:i+ship_length-1] = 32  # m
                        test_row[0][i+ship_length-1] = 4 #b
                        if matching_rows(board.board[:,row_or_col], test_row[0]):
                            np_matrix = np.zeros((10, 10))
                            np_matrix[:, row_or_col] = test_row[0]
                            option_for_board = Board(np_matrix)
                            option_for_board.ships[ship_length - 1] += 1
                            Bimaru.fill_water_around_ship(option_for_board, activate_dual=x)
                            if Board.match_boards(board, option_for_board):
                                options[ship_length].append(option_for_board)
        for ship_length in range(2, 5):
            np.random.shuffle(options[ship_length])
        #np.random.shuffle(options[4])
        return options




if __name__ == "__main__":
    board = Board.parse_instance()
    problem = Bimaru(board)
    if len(problem.initial.board.hints) > 2:
        goal_node = depth_first_tree_search(problem)
    else:
        goal_node = greedy_search(problem)
        #goal_node = astar_search(problem)

    #goal_node = astar_search(problem)
    goal_node.state.print()