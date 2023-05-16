# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Pedro M. P. Curvo
# 00000 Nome2

import itertools
import sys
import time
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
            Bimaru.fill_water_rows_cols(board)
            Bimaru.fill_water_around_ship(board)
            self.ships = Bimaru.count_ships(board)
        else:
            self.ships = [0, 0, 0, 0]
        self.board = board
        self.id = BimaruState.state_id
        self.expectated_ships = [4, 3, 2, 1]
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def print(self):
        self.board.print()

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board: np.ndarray, col_number = None, row_number = None):
        """Construtor da classe. Recebe um array bidimensional
        (matriz) numpy com o conteúdo do tabuleiro."""
        self.board = board
        self.col_number = col_number 
        self.row_number = row_number
    
    def __add__(self, other):
        """Soma de dois tabuleiros."""
        """Soma de dois tabuleiros."""
        new_board = np.where(self.board == '', other.board, self.board)
        return Board(new_board, self.col_number, self.row_number)


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.board[row][col] == '':
            return None
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            if self.board[row + 1][col] == '':
                return None, None
            return None, self.board[row + 1][col]
        elif row == 9:
            if self.board[row - 1][col] == '':
                return None, None
            return self.board[row - 1][col], None
        else:
            if self.board[row - 1][col] == '':
                if self.board[row + 1][col] == '':
                    return None, None
                return None, self.board[row + 1][col]
            elif self.board[row + 1][col] == '':
                return self.board[row - 1][col], None
            return self.board[row - 1][col], self.board[row + 1][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            if self.board[row][col + 1] == '':
                return None, None
            return None, self.board[row][col + 1]
        elif col == 9:
            if self.board[row][col - 1] == '':
                return None, None
            return self.board[row][col - 1], None
        else:
            if self.board[row][col - 1] == '':
                if self.board[row][col + 1] == '':
                    return None, None
                return None, self.board[row][col + 1]
            elif self.board[row][col + 1] == '':
                return self.board[row][col - 1], None
            return self.board[row][col - 1], self.board[row][col + 1]

    def print(self):
        """Imprime o tabuleiro."""
        self.board = np.where(self.board == 'w', '.', self.board)
        for row in self.board:
            print("".join(row))

    @staticmethod
    def match_boards(board1, board2):
        """Verifies if two boards match."""
        for row in range(10):
            for col in range(10):
                if board1.board[row][col].upper() != board2.board[row][col].upper():
                    if board1.board[row][col] != '' and board2.board[row][col] != '':
                        return False
        matrix = np.zeros((10, 10))
        for row in range(10):
            for col in range(10):
                if board1.board[row][col] not in ['', 'w', 'W']:
                    matrix[row][col] = 1
                if board2.board[row][col] not in ['', 'w', 'W']:
                    matrix[row][col] = 1
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)
        
        for i in range(10):
            if int(col_compare[i]) > board1.col_number[i] or int(row_compare[i]) > board1.row_number[i]:
                return False
        # Other conditions
        for row in range(10):
            for col in range(10):
                if board1.board[row][col] in {'t', 'T'} and row + 2 < 9:
                    if board2.board[row + 2][col] in ('c', 'C', 'l', 'L', 'R', 'r', 't', 'T'):
                        return False
                if board.board[row][col] in {'b', 'B'} and row - 2 > 0 and board2.board[row - 2][col] in {'c', 'C', 'l', 'L', 'R', 'r', 'b', 'B'}:
                    return False
                if board.board[row][col] in {'l', 'L'} and col + 2 < 9:
                    if board2.board[row][col + 2] in ('c', 'C', 't', 'T', 'B', 'b', 'l', 'L'):
                        return False
                if board.board[row][col] in {'r', 'R'} and col - 2 > 0:
                    if board2.board[row][col - 2] in ('c', 'C', 't', 'T', 'B', 'b', 'r', 'R'):
                        return False
        aim = 0
        for row in range(10):
            for col in range(10):
                if board2.board[row][col].upper() in {'C', 'T', 'B', 'L', 'R'}:
                    if board2.board[row][col].upper() != board1.board[row][col].upper():
                        aim += 1
        if aim == 0 : return False

        return True
    

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        # Creates the np array
        board = np.zeros((10, 10), dtype=str)
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
                board[int(line[1])][int(line[2])] = line[3]
        return Board(board, col, row)

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        Bimaru.fill_water_rows_cols(board)
        Bimaru.fill_water_around_ship(board)
        Bimaru.fill_water(board)
        self.board = board
        self.expected_ships = [4, 3, 2, 1]
        self.ships = Bimaru.count_ships(board)
        self.first_options = Bimaru.create_all_first_options(board)

    
    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.ships[3] != state.expectated_ships[3]:
            return self.first_options[4]
        if state.ships[2] != state.expectated_ships[2]:
            lista = [option for option in self.first_options[3] if Board.match_boards(state.board, option)]
            return lista
        if state.ships[1] != state.expectated_ships[1]:
            lista = [option for option in self.first_options[2] if Board.match_boards(state.board, option)]
            return lista
        if state.ships[0] != state.expectated_ships[0]:
            lista = [option for option in self.first_options[1] if Board.match_boards(state.board, option)]
            return lista

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # Keep the action ? 
        new_board = state.board + action
        Bimaru.fill_water(new_board)
        new_state = BimaruState(new_board)
        new_state.ships = [state.ships[i] + Bimaru.count_ships(action)[i] for i in range(4)]
        return new_state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.ships != self.expected_ships:
            return False
        matrix = np.zeros((10, 10))
        for row, col in itertools.product(range(10), range(10)):
            if state.board.board[row][col] not in {'', 'w', 'W'}:
                matrix[row][col] = 1
                matrix[row][col] = 1
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)
        for i in range(10):
            if col_compare[i] != state.board.col_number[i]:
                return False
            if row_compare[i] != state.board.row_number[i]:
                return False

        # All checks passed, it's a solution!
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    @staticmethod
    def fill_water_rows_cols(board: Board):
        """Preenche com água as linhas e colunas que não contêm barcos."""
        for row in range(10):
            if board.row_number[row] == 0:
                for col in range(10):
                    board.board[row][col] = 'w'
        for col in range(10):
            if board.col_number[col] == 0:
                for row in range(10):
                    board.board[row][col] = 'w'

    @staticmethod
    def fill_water_around_ship(board: Board):
        """Preenche com água as posições em redor de um barco."""
        for row in range(10):
            for col in range(10):
                # Fill around C 
                if board.board[row][col] in ('c', 'C'):
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('c', 'C'):
                                    board.board[i][j] = 'w'
                # Fill around M
                if board.board[row][col] in ('m', 'M'):
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('c', 'C') and j != col and i != row:
                                    board.board[i][j] = 'w'

                # Fill around B
                if board.board[row][col] in ('b', 'B'):
                    for i in range(row - 2, row + 2):
                        for j in range(col - 1, col + 2):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('b', 'B') and j != col or i > row:
                                    board.board[i][j] = 'w'
                # Fill around T
                if board.board[row][col] in ('t', 'T'):
                    for i in range(row - 1, row + 3):
                        for j in range(col - 1, col + 2):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('t', 'T') and j != col or i < row:
                                    board.board[i][j] = 'w'
                # Fill around L
                if board.board[row][col] in ('l', 'L'):
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 3):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('l', 'L') and i != row or j < col:
                                    board.board[i][j] = 'w'
                # Fill around R
                if board.board[row][col] in ('r', 'R'):
                    for i in range(row - 1, row + 2):
                        for j in range(col - 2, col + 2):
                            if i >= 0 and i < 10 and j >= 0 and j < 10:
                                if board.board[i][j] not in ('r', 'R') and i != row or j > col:
                                    board.board[i][j] = 'w'
                    
    @staticmethod
    def count_ships(board: Board):
        """Conta o número de barcos de cada tipo presentes no tabuleiro."""
        ships = [0, 0, 0, 0]
        for row in range(10):
            for col in range(10):
                # Count Single Ships
                if board.board[row][col] in ('c', 'C'):
                    ships[0] += 1
                # Count Vertical Ships
                if board.board[row][col] in ('t', 'T'):
                    ship_length = 1
                    for i in range(row + 1, row + 4):
                        if i < 10 and board.board[i][col] in ('m', 'M'):
                            ship_length += 1
                        if i < 10 and board.board[i][col] in ('b', 'B'):
                            ship_length += 1
                            ships[ship_length - 1] += 1
                            break
                        if i < 10 and board.board[i][col] not in ('m', 'M', 'b', 'B'):
                            break
                # Count Horizontal Ships
                if board.board[row][col] in ('l', 'L'):
                    ship_length = 1
                    for i in range(col + 1, col + 4):
                        if i < 10 and board.board[row][i] in ('m', 'M'):
                            ship_length += 1
                        if i < 10 and board.board[row][i] in ('r', 'R'):
                            ship_length += 1
                            ships[ship_length - 1] += 1
                            break
                        if i < 10 and board.board[row][i] not in ('m', 'M', 'r', 'R'):
                            break
        return ships

    @staticmethod
    def fill_water(board: Board):
        matrix = np.zeros((10, 10))
        for row in range(10):
            for col in range(10):
                if board.board[row][col] not in {'', 'w', 'W'}:
                    matrix[row][col] = 1
        col_compare = matrix.sum(axis=0)
        row_compare = matrix.sum(axis=1)
        for row in range(10):
            for col in range(10):
                if board.board[row][col] == '':
                    if col_compare[col] == board.col_number[col] or row_compare[row] == board.row_number[row]:
                        board.board[row][col] = 'w'



    @staticmethod
    def create_all_first_options(board: Board):
        """Cria todas as opções iniciais possíveis."""
        def matching_rows(row1, row2):
            # add que se for tudo igual quero que de falso logo 
            for i in range(10):
                if row1[i].upper() != row2[i].upper():
                    if row1[i] != '' and row2[i] != '':
                        return False
                elif row1[i].upper() == 'C':
                    return False
            return True

        options = {1: [], 2: [], 3: [], 4: []}
        # Horizontals 
        for row in range(10):
            for ship_length in range(1, 5):
                if board.row_number[row] >= ship_length:
                    for i in range(11 - ship_length):
                        np_row = np.zeros((1, 10), dtype=str)
                        if ship_length == 1:
                            np_row[0][i] = 'c'
                        else:
                            np_row[0][i] = 'l'
                            for k in range(1, ship_length - 1):
                                np_row[0][i+k] = 'm'
                            np_row[0][i+ship_length-1] = 'r'
                        if matching_rows(board.board[row], np_row[0]):
                            np_matrix = np.zeros((10, 10), dtype=str)
                            np_matrix[row] = np_row[0]
                            obj = Board(np_matrix)
                            Bimaru.fill_water_around_ship(obj)
                            if Board.match_boards(board, obj):
                                options[ship_length].append(obj)
        # Verticals
        for col in range(10):
            for ship_length in range(2, 5):
                if board.col_number[col] >= ship_length:
                    for i in range(11 - ship_length):
                        np_row = np.zeros((1, 10), dtype=str)
                        np_row[0][i] = 't'
                        for j in range(ship_length - 2):
                            np_row[0][i+j+1] = 'm'
                        np_row[0][i+ship_length-1] = 'b'
                        if matching_rows(board.board.transpose()[col], np_row[0]):
                            np_matrix = np.zeros((10, 10), dtype=str)
                            np_matrix[col] = np_row[0]
                            obj = Board(np_matrix.transpose())
                            Bimaru.fill_water_around_ship(obj)
                            if Board.match_boards(board, obj):
                                options[ship_length].append(obj)
        return options




if __name__ == "__main__":
    # Ler a instância a partir do ficheiro 'i1.txt' (Figura 1): # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    problem = Bimaru(board)
    start_time = time.time()
    goal_node = depth_first_tree_search(problem)
    end_time = time.time()


    print('Is goal?', problem.goal_test(goal_node.state))
    print('Path cost:', goal_node.path_cost)
    print('Solution: \n')
    goal_node.state.board.print()
    print('Time:', end_time - start_time)

    

    '''
    initial_state = problem.initial
    print(initial_state.ships)
    s2 = problem.result(initial_state, problem.actions(initial_state)[2])
    print(s2.ships)
    s3 = problem.result(s2, problem.actions(s2)[2])
    s3.board.print()
    print(s3.ships)
    problem.actions(s3)[0].print()
    s4 = problem.result(s3, problem.actions(s3)[0])
    s4.board.print()
    print(s4.ships)
    print(Bimaru.count_ships(s4.board))
    '''
    #Bimaru.create_all_first_options(problem.board)
    
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
