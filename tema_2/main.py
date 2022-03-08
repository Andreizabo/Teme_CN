import numpy as np
from termcolor import colored

INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DISPLAY_COLOR = "blue"


def pretty_matrix_print(matrix, name):
    '''
    Displays a given matrix.
    '''
    print(f"\n{name}:")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            print(colored(str(matrix[i][j]), DISPLAY_COLOR), " ", end="")
        print("")


def convert_to_triangle_matrix(matrix):
    for i in range(1, matrix.shape[0]):
        for j in range(0, i):
            matrix[i][j] = 0


def get_pivot(matrix, l):
    '''
    Returns i_0 which is the pivot's row.

    @param matrix : the matrix
    @param l : the column from which to extract the max
    '''

    max_position = l
    for i in range(l, matrix.shape[1]):
        if matrix[max_position][l] < matrix[i][l]:
            max_position = i

    return max_position


def swap_lines(matrix, l1, l2):
    for i in range(matrix.shape[1]):
        aux = matrix[l1][i]
        matrix[l1][i] = matrix[l2][i]
        matrix[l2][i] = aux


def verify_results(a, x, b):
    res = np.matmul(a, x)
    return np.linalg.norm(res - b)


if __name__ == "__main__":

    # Read input
    while True:
        try:
            n = int(input(colored("Dimensiunea sistemului: ", INFO_COLOR)))
            break
        except:
            print(colored("Input invalid!", ERROR_COLOR))

    while True:
        try:
            eps = int(input(colored("Precizia sistemului (minim 5): ", INFO_COLOR)))
            if eps < 5:
                raise Exception

            eps = 10 ** (-eps)
            break
        except:
            print(colored("Input invalid!", ERROR_COLOR))

    # Read matrix from file
    filepath = input(colored("Calea catre fisier (default ./matrice.txt): ", INFO_COLOR))
    if filepath == "":
        filepath = "./matrice.txt"

    a_init = np.empty((n, n))
    with open(filepath, "r") as fin:
        for i in range(n):
            buffer = fin.readline().split(" ")
            for j in range(n):
                a_init[i][j] = buffer[j]

    # Display the matrix to make sure it's working properly
    pretty_matrix_print(a_init, "a_init")

    # Calculate the determinant
    a_init_det = np.linalg.det(a_init)
    print("Determinatul matricei: ", a_init_det)

    if (a_init_det == 0):
        print(colored("Determinantul nu poate fi 0. Programul se va opri...", WARNING_COLOR))
        exit(0)

    # Read result from file
    filepath = input(colored("Calea catre fisier (default ./rezultat.txt): ", INFO_COLOR))
    if filepath == "":
        filepath = "./rezultat.txt"

    # Display result
    b_init = np.empty((n, 1))
    with open(filepath, "r") as fin:
        buffer = fin.readline().split(" ")
        for i in range(n):
            b_init[i][0] = buffer[i]

    pretty_matrix_print(b_init, "b_init")

    print("---------------------------")

    # Copy the initial values
    a = np.copy(a_init)
    b = np.copy(b_init)

    # Start the Gauss algorithm
    l = 0
    i0 = get_pivot(a, l)
    swap_lines(a, i0, l)
    swap_lines(b, i0, l)

    # Checking the value of the pivot
    if abs(a[l][l]) < eps:
        print(colored("Pivotul este nul!", WARNING_COLOR))
        exit(0)
    print("\n-----\n")
    pretty_matrix_print(a, "a")
    pretty_matrix_print(b, "b")

    while l < n - 1 and abs(a[l][l]) > eps:
        for i in range(l + 1, n):
            f = a[i][l] / a[l][l]
            print("f = ", f)
            for j in range(l + 1, n):
                a[i][j] = a[i][j] - f * a[l][j]
            b[i][0] = b[i][0] - f * b[l][0]
        l += 1
        i0 = get_pivot(a, l)

        swap_lines(a, i0, l)
        swap_lines(b, i0, l)

        # Checking the value of the pivot
        if abs(a[l][l]) < eps:
            print(colored("Pivotul este nul!", WARNING_COLOR))
            exit(0)
        print("\n-----\n")
        pretty_matrix_print(a, "a")
        pretty_matrix_print(b, "b")

    # Check the determinat of the newly created matrix
    if abs(a[l][l]) <= eps:
        print(colored("Matrice singulara", WARNING_COLOR))
        exit(0)

    # Convert the matrix to a triangular shape and display it
    convert_to_triangle_matrix(a)
    pretty_matrix_print(a, "a dupa convert")

    # Calculate x vector
    x = np.empty((n, 1))
    x[n - 1][0] = b[n - 1][0] / a[n - 1][n - 1]

    # Work backwords
    for i in range(n - 2, -1, -1):
        # Calculate the denominator of the equation
        denominator = b[i][0]
        for j in range(i + 1, n):
            denominator -= a[i][j] * x[j][0]

        x[i][0] = denominator / a[i][i]

    # Print results
    print("\n---------------------------------")
    pretty_matrix_print(a, "a")
    pretty_matrix_print(b, "b")
    pretty_matrix_print(x, "x")

    print('\n----------------------------------')
    print('Euclidean norm of Ax - b')
    print(verify_results(a_init, x, b_init))