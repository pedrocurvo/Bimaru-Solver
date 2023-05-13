# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Pedro M. P. Curvo
# 00000 Nome2

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
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1
        self.grids = [board]

    def __lt__(self, other):
        return self.id < other.id
    
    def print(self):
        self.board.print()

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board: np.ndarray, col_number: np.ndarray, row_number: np.ndarray):
        """Construtor da classe. Recebe um array bidimensional
        (matriz) numpy com o conteúdo do tabuleiro."""
        self.board = board
        self.col_number = col_number 
        self.row_number = row_number


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
        for row in self.board:
            print(" ".join(row))

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        # Creates the np array
        board = np.zeros((10, 10), dtype=str)
        # Read the first line of txt file
        line = sys.stdin.readline().split()
        col = np.array([int(x) for x in line[1:]])
        # Read the second line of txt file
        line = sys.stdin.readline().split()
        row = np.array([int(x) for x in line[1:]])
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
        self.board = board
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # Keep the action ? 
        c = np.char.add(state.board.board, action)
        board = Board(c, state.board.col_number, state.board.row_number)
        d = BimaruState(board)
        d.grids.append(action)
        return d


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler a instância a partir do ficheiro 'i1.txt' (Figura 1): # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    board.print()
    # Imprimir valores adjacentes
    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))
    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))
    problem = Bimaru(board)
    s0 = BimaruState(board)
    test = np.zeros((10, 10), dtype=str)
    test[0][1] = 'w'
    test[0][2] = 'w'
    s1 = problem.result(s0, test)
    s1.print()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
