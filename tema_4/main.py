import copy
from termcolor import colored
from tqdm import tqdm
import prettymatrix
import numpy as np

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"

eps = 10 ** -6


class EqSystem:
    def __init__(self):
        self.n = 0
        self.a = []
        self.b = []
        self.x = []
        self.a_diag = []

    def set_system(self, n, a, b):
        self.n = n
        self.a = a
        self.b = b
        self.x = [0 for _ in range(n)]
        self.a_diag = [get_diagonal_element(self.a, i) for i in range(n)]

    def jacobi(self, x_p):
        x_c = [self.b[i] for i in range(self.n)]
        for line in range(self.n):
            for element in self.a[line]:
                column = element[1]
                if column == line:
                    continue
                value = element[0]
                x_c[line] -= (value * x_p[column])
                x_c[column] -= (value * x_p[line])

        return [x_c[i] / self.a_diag[i] for i in range(self.n)]

    def find_sol(self):
        max_k = 10000
        x_c = self.x
        k = 0
        dif = 10 ** 8 - 1

        while eps < dif < 10 ** 8 and k < max_k:
            x_p = x_c
            x_c = self.jacobi(x_p)
            dif = get_vect_dif(x_c, x_p)
            k += 1
            print(f'Done {k}')
        if dif < eps:
            self.x = x_c
            return k
        else:
            return -1

    def verify_sol(self):
        return get_vect_dif(prod_matrix_vect(self.a, self.x), self.b)


def get_vect_dif(x, y):
    return np.linalg.norm(np.subtract(np.array(x), np.array(y)))


def exists(matrix, i, j):
    for index, element in enumerate(matrix[i]):
        if element[1] == j:
            return index
    return -1


def get_sym(matrix, diag=False):
    n = len(matrix)
    sym = [[] for _ in range(n)]
    for line in range(n):
        for element in matrix[line]:
            column = element[1]
            value = element[0]
            if not diag and line == column:
                continue
            insert_in_matrix(sym, column, line, value)
    return sym


def insert_in_matrix(matrix, lin, col, val):
    index = exists(matrix, lin, col)
    if index == -1:
        matrix[lin] += [(val, col)]
    else:
        matrix[lin][index] = (matrix[lin][index][0] + val, matrix[lin][index][1])


def get_diagonal_element(matrix, i):
    for element in matrix[i]:
        if element[1] == i:
            return element[0]


def prod_matrix_vect(m1, m2):
    n = len(m1)
    m3 = [0 for _ in range(n)]
    m1_sym = get_sym(m1)

    for line in range(n):
        for element in m1[line]:
            column = element[1]
            m3[line] += m2[column] * element[0]
        for element in m1_sym[line]:
            column = element[1]
            m3[line] += m2[column] * element[0]
    return m3


def read_sparse_matrix(path):
    with open(path, 'r') as rd:
        try:
            n = rd.readline()
            n = int(n)
        except ValueError:
            print(colored(f'Invalid format for matrix file, "{n}" is not an integer', ERROR_COLOR))
            exit()
        matrix = [[] for _ in range(n)]

        rd.readline()
        line = rd.readline()
        while line:
            elements = line.split(',')
            try:
                elements = [
                    float(elements[0]),
                    int(elements[1]),
                    int(elements[2])
                ]
            except ValueError:
                print(colored('Invalid format for matrix file', ERROR_COLOR))
                exit()
            if elements[1] < elements[2]:
                print(colored(
                    f'Row index must be always greater or equal to column index ({elements[2]} not <= {elements[1]})'),
                    ERROR_COLOR)
            # Aici verificam ca toate eleementele de pe diagonala sunt nenule
            if elements[1] == elements[2] and elements[0] == 0:
                print(colored(
                    f'All elements on the diagonal must not be zero',
                    ERROR_COLOR))

            insert_in_matrix(matrix, elements[1], elements[2], elements[0])
            line = rd.readline()
    return matrix, n


def read_b_vector(path):
    with open(path, 'r') as rd:
        matrix = []

        line = rd.readline()
        while line:
            try:
                element = float(line)
            except ValueError:
                print(colored('Invalid format for b file', ERROR_COLOR))
                exit()
            matrix.append(element)
            line = rd.readline()
    return matrix


def read_system(path_a, path_b):
    a, n = read_sparse_matrix(path_a)
    b = read_b_vector(path_b)

    eq_system = EqSystem()
    eq_system.set_system(n, a, b)
    return eq_system


if __name__ == '__main__':
    eq_system_1 = read_system('a_1.txt', 'b_1.txt')
    result = eq_system_1.find_sol()
    print(eq_system_1.verify_sol())
