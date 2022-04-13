import sys

from termcolor import colored
import numpy as np
import prettymatrix

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"

eps = 10 ** -7

INPUT = {'matrix_path': 'matrix1.txt'}


def pretty_matrix_print(matrix, name):
    '''
    Displays a given matrix.
    '''
    pretty_mat = prettymatrix.matrix_to_string(np.array([[float(str(f'{matrix[i][j]:.4f}')) for j in range(len(matrix[i]))] for i in range(len(matrix))])).split('\n')
    res = ''
    for i, line in enumerate(pretty_mat):
        if i == len(pretty_mat) // 2:
            res += name + " = " + line + '\n'
        else:
            res += ' ' * len(f'{name} = ') + line + '\n'
    return res


class Homework5:
    def __init__(self):
        self.eps = 10 ** -7
        self.k_max = 100
        self.A = None
        self.A_init = None

    def read_matrix(self):
        global INPUT
        self.A = []
        with open(INPUT['matrix_path'], 'r') as rd:
            ln = rd.readline()
            while ln:
                self.A.append([float(element) for element in ln.split(' ')])
                ln = rd.readline()
        self.A = np.array(self.A)
        self.A_init = self.A.copy()

    def indices(self):
        max = 0
        p = -1
        q = -1
        for j in range(len(self.A)):
            for i in range(j):
                if max < abs(self.A[i][j]):
                    max = abs(self.A[i][j])
                    p = i
                    q = j
        return p, q

    def check_value(self, value):
        '''
        Checks whether or not the given value is close to zero.
        '''
        if abs(value) < abs(self.eps):
            return 0

        return value

    def jacobi_algorithm(self, n: int):
        '''
        Something
        '''

        k = 0
        U = np.identity(n)

        p, q = self.indices()

        alpha = (self.A[p][p] - self.A[q][q]) / (2 * self.A[p][q])
        t = -alpha + (1 if alpha >= 0 else -1) * ((alpha ** 2 + 1) ** (1 / 2))
        c = 1 / ((1 + t ** 2) ** (1 / 2))
        s = t / ((1 + t ** 2) ** (1 / 2))

        # Print status
        # print(f'''p = {p}, q = {q}\nc = {c}, s = {s}, t = {t}\n{A}''')

        while not self.is_diagonal(self.A) and k <= self.k_max:
            print(colored(f'[STEP] {k}', 'yellow'))

            for j in range(n):
                if j != p and j != q:
                    self.A[p][j] = self.check_value(c * self.A[p][j] + s * self.A[q][j])

            for j in range(n):
                if j != p and j != q:
                    self.A[q][j] = self.A[j][q] = self.check_value(-s * self.A[j][p] + c * self.A[q][j])

            for j in range(n):
                if j != p and j != q:
                    self.A[j][p] = self.check_value(self.A[p][j])

            self.A[p][p] = self.check_value(self.A[p][p] + t * self.A[p][q])
            self.A[q][q] = self.check_value(self.A[q][q] - t * self.A[p][q])
            self.A[p][q] = 0
            self.A[q][p] = 0

            U_orig = np.copy(U)
            for i in range(n):
                U[i][p] = self.check_value(c * U[i][p] + s * U[i][q])
                U[i][q] = self.check_value(-s * U_orig[i][p] + c * U[i][q])

            p, q = self.indices()

            if p == -1 and q == -1:
                break

            alpha = (self.A[p][p] - self.A[q][q]) / (2 * self.A[p][q])
            t = -alpha + (1 if alpha >= 0 else -1) * ((alpha ** 2 + 1) ** (1 / 2))
            c = 1 / ((1 + t ** 2) ** (1 / 2))
            s = t / ((1 + t ** 2) ** (1 / 2))

            # Print status
            # print(f'''p = {p}, q = {q}\nc = {c}, s = {s}, t = {t}\n{A}''')
            k += 1

        # print(A, '\n')
        # print(U)
        return U

    def is_diagonal(self, matrix: np.matrix) -> bool:
        '''
        Test whether or not a matrix is diagonal, meaning that
        all elements besides the main diagonal (i==j) are zero.
        '''
        # return np.count_nonzero(matrix - np.diag(np.diagonal(matrix))) == 0

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i != j and abs(matrix[i][j]) > self.eps:
                    return False
        return True

    def verify_sum(self, jacobi, library):
        s = 0
        for diag_jacobi in jacobi:  # Diagonal elements in matrix calculated with Jacobi
            minimum = sys.maxsize
            for diag_lib in library:  # Diagonal elements in matrix calculated with library
                if abs(diag_jacobi - diag_lib) < minimum:
                    minimum = abs(diag_jacobi - diag_lib)
            s += minimum
        return s


def part_1():
    result = ''
    result += pretty_matrix_print(h.A, "A") + ' '
    U = h.jacobi_algorithm(len(h.A))
    result += '\n' + pretty_matrix_print(U, "U") + ' '
    result += '\nFirst norm : ' + str(h.check_value(np.linalg.norm(np.matmul(h.A_init, U) - np.matmul(U, h.A)))) + '\n'
    result += '---------------------------------------------\n \n'
    return result


def part_2():
    result = ''
    eigen_values, eigen_vectors = np.linalg.eigh(h.A_init)
    result += 'Eigen values = ' + str(eigen_values) + '\n \n'
    result += pretty_matrix_print(eigen_vectors, 'Eigen vectors') + ' '
    result += '\nSecond norm : ' + str(h.check_value(h.verify_sum(np.diag(h.A), eigen_values))) + '\n'
    result += '---------------------------------------------\n \n'
    return result


def part_3():
    # https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html
    result = ''
    u, s, v_transpose = np.linalg.svd(h.A_init)
    s_i = np.array([[0 if i != j else (0 if h.check_value(s[j]) == 0 else 1 / s[j]) for i in range(len(s))] for j in
                    range(len(s))])
    A_I = np.matmul(np.matmul(np.transpose(v_transpose), s_i), np.transpose(u))
    A_J = np.matmul(np.linalg.pinv(np.matmul(np.transpose(h.A_init), h.A_init)), np.transpose(h.A_init))

    result += f'Singular values : {s}\n \n'
    result += f'Matrix rank : {np.count_nonzero(s[abs(s) >= h.eps])}\n \n'
    result += f'Conditioning number : {np.max(s) / np.min(list(filter(lambda x: abs(x) > h.eps, s)))}\n'
    result += pretty_matrix_print(A_I, "A_I") + ' '
    result += '\n' + pretty_matrix_print(A_J, "A_J") + ' '
    result += f'\nThird norm: {h.check_value(np.linalg.norm(A_I - A_J))}\n'
    result += '---------------------------------------------\n \n'
    return result


# Global values
h = Homework5()
h.read_matrix()
