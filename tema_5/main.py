import sys

from termcolor import colored
import numpy as np
import math

# Default colors
INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DEBUG_COLOR = "blue"

eps = 10 ** -6


class Homework5:
    def __init__(self):
        self.eps = 10 ** -7
        self.k_max = 100

    def indices(self, A: np.matrix):
        max = 0
        p = -1
        q = -1
        for j in range(len(A)):
            for i in range(j):
                if max < abs(A[i][j]):
                    max = abs(A[i][j])
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

    def jacobi_algorithm(self, n: int, A: np.ndarray):
        '''
        Something
        '''

        k = 0
        U = np.identity(n)

        p, q = self.indices(A)

        alpha = (A[p][p] - A[q][q]) / (2 * A[p][q])
        t = -alpha + (1 if alpha >= 0 else -1) * ((alpha ** 2 + 1) ** (1 / 2))
        c = 1 / ((1 + t ** 2) ** (1 / 2))
        s = t / ((1 + t ** 2) ** (1 / 2))

        # Print status
        # print(f'''p = {p}, q = {q}\nc = {c}, s = {s}, t = {t}\n{A}''')

        while not self.is_diagonal(A) and k <= self.k_max:
            print(colored(f'[STEP] {k}', 'yellow'))

            for j in range(n):
                if j != p and j != q:
                    A[p][j] = self.check_value(c * A[p][j] + s * A[q][j])

            for j in range(n):
                if j != p and j != q:
                    A[q][j] = A[j][q] = self.check_value(-s * A[j][p] + c * A[q][j])

            for j in range(n):
                if j != p and j != q:
                    A[j][p] = self.check_value(A[p][j])

            A[p][p] = self.check_value(A[p][p] + t * A[p][q])
            A[q][q] = self.check_value(A[q][q] - t * A[p][q])
            A[p][q] = 0
            A[q][p] = 0

            U_orig = np.copy(U)
            for i in range(n):
                U[i][p] = self.check_value(c * U[i][p] + s * U[i][q])
                U[i][q] = self.check_value(-s * U_orig[i][p] + c * U[i][q])

            p, q = self.indices(A)

            alpha = (A[p][p] - A[q][q]) / (2 * A[p][q])
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


if __name__ == "__main__":
    # Part 1
    h = Homework5()
    A = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [1.0, 1.0, 1.0]])
    A_init = A.copy()
    print(A)
    U = h.jacobi_algorithm(3, A)
    print(U)
    print(h.check_value(np.linalg.norm(np.matmul(A_init, U) - np.matmul(U, A))))

    # Part 2
    eigen_values, eigen_vectors = np.linalg.eigh(A_init)
    print(eigen_values)
    print(eigen_vectors)
    print(h.check_value(h.verify_sum(np.diag(A), eigen_values)))

    # Part 3
    # https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html
    u, s, vh = np.linalg.svd(A_init)

    print(f'Valori singulare: {s}')
    print(f'Rangul matricei: {np.count_nonzero(s[abs(s) >= h.eps])}')
    print(f'Numar de conditionare: {np.max(s) / np.linalg.pinv(A_init)}')


