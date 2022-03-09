import numpy as np
from termcolor import colored
import prettymatrix

INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DISPLAY_COLOR = "blue"


def pretty_matrix_print(matrix, name):
    '''
    Displays a given matrix.
    '''
    # print("---------------------------")
    pretty_mat = prettymatrix.matrix_to_string(matrix).split('\n')
    for i, line in enumerate(pretty_mat):
        if i == len(pretty_mat) // 2:
            print(colored(name, WARNING_COLOR) + " = " + colored(line, DISPLAY_COLOR))
        else:
            print(' ' * len(f'{name} = ') + colored(line, DISPLAY_COLOR))
    # for i in range(matrix.shape[0]):
    #     if i == matrix.shape[0] // 2:
    #         print(f"{name} =  |\t", end="")
    #     else:
    #         print(' ' * len(f'{name} =  ') + '|\t', end="")
    #     for j in range(matrix.shape[1]):
    #         print(colored(str(matrix[i][j]), DISPLAY_COLOR), " ", end="")
    #     print("\t|")
    # print("---------------------------")


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
    for i in range(l, matrix.shape[0]):
        if matrix[max_position][l] < matrix[i][l]:
            max_position = i

    return max_position


def swap_lines(matrix, l1, l2):
    for i in range(matrix.shape[1]):
        aux = matrix[l1][i]
        matrix[l1][i] = matrix[l2][i]
        matrix[l2][i] = aux


def first_norm(a, x, b):
    res = np.matmul(a, x)
    return np.linalg.norm(res - b)


def second_norm(a, x, b):
    x_solved = np.linalg.solve(a, b)
    return np.linalg.norm(x - x_solved)


def third_norm(a, x, b):
    a_inv = np.linalg.inv(a)
    return np.linalg.norm(x - np.matmul(a_inv, b))


def fourth_norm(a, a_inv):
    lib_a_inv = np.linalg.inv(a)
    return np.linalg.norm(a_inv - lib_a_inv)


def get_input():
    # Read input
    while True:
        try:
            n = int(input(colored("Dimensiunea sistemului: ", INFO_COLOR)))
            break
        except:
            print(colored("Input invalid!", ERROR_COLOR))
            n = 3
            break

    while True:
        try:
            eps = int(input(colored("Precizia sistemului (minim 5): ", INFO_COLOR)))
            if eps < 5:
                raise Exception

            eps = 10 ** (-eps)
            break
        except:
            print(colored("Input invalid!", ERROR_COLOR))
            eps = 10 ** (-5)
            break

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
    pretty_matrix_print(a_init, "A_init")

    # Calculate the determinant
    a_init_det = np.linalg.det(a_init)
    # print("Determinatul matricei: ", a_init_det)

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

    return n, eps, a_init, b_init


def gaussian_elimination(n, eps, a, b):
    # Start the Gauss algorithm
    l = 0
    i0 = get_pivot(a, l)
    swap_lines(a, i0, l)
    swap_lines(b, i0, l)

    # Checking the value of the pivot
    if abs(a[l][l]) < eps:
        print(colored("Pivotul este nul!", WARNING_COLOR))
        exit(0)
    # print("\n-----\n")
    # pretty_matrix_print(a, "a")
    # pretty_matrix_print(b, "b")

    while l < n - 1 and abs(a[l][l]) > eps:
        for i in range(l + 1, n):
            f = a[i][l] / a[l][l]
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
        # print("\n-----\n")
        # pretty_matrix_print(a, "a")
        # pretty_matrix_print(b, "b")

    # Check the determinat of the newly created matrix
    if abs(a[l][l]) <= eps:
        print(colored("Matrice singulara", WARNING_COLOR))
        exit(0)
    convert_to_triangle_matrix(a)
    return a, b


def inverse_substitution(a, b, n):
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
    return x


def compute_inverse_matrix(a, n, eps):
    identity_matrix = np.identity(a.shape[0])
    a_ext = np.concatenate((a, identity_matrix), axis=1)
    number_of_cols = a_ext.shape[1]

    l = 0
    i0 = get_pivot(a_ext, l)
    swap_lines(a_ext, i0, l)

    # Checking the value of the pivot
    if abs(a[l][l]) < eps:
        print(colored("Pivotul este nul!", WARNING_COLOR))
        exit(0)

    while l < n - 1 and abs(a_ext[l][l]) > eps:
        for i in range(l + 1, n):
            if abs(a_ext[l][l]) < eps:
                print(colored("Pivotul este nul!", WARNING_COLOR))
                exit(0)
            a_ext[i][l] /= a_ext[l][l]
            for j in range(l + 1, number_of_cols):
                a_ext[i][j] -= (a_ext[i][l] * a_ext[l][j])
        l += 1
        i0 = get_pivot(a_ext, l)
        swap_lines(a_ext, i0, l)
        # Checking the value of the pivot
        if abs(a_ext[l][l]) < eps:
            print(colored("Pivotul este nul!", WARNING_COLOR))
            exit(0)

    if abs(a_ext[l][l]) <= eps:
        print(colored("Matrice singulara", WARNING_COLOR))
        exit(0)
    convert_to_triangle_matrix(a_ext)
    a_r, i_r = np.split(a_ext, 2, axis=1)
    inv = np.zeros((n, n))
    for j in range(n):
        b = np.reshape(i_r[:, j], (3, 1))
        x = np.reshape(inverse_substitution(a_r, b, n), (3, 1))
        inv[:, [j]] = x
    return inv


if __name__ == "__main__":
    n, eps, a_init, b_init = get_input()

    # Copy the initial values
    a = np.copy(a_init)
    b = np.copy(b_init)

    a, b = gaussian_elimination(n, eps, a, b)

    x = inverse_substitution(a, b, n)

    a_inv = compute_inverse_matrix(a_init, n, eps)

    # Print results
    print('\n------  Rezultate dupa eliminare gaussiana si substitutie inversa  ----')
    pretty_matrix_print(a, "A(dupa eliminare gaussiana)")
    pretty_matrix_print(b, "b(dupa eliminare gaussiana)")
    pretty_matrix_print(x, "x")
    print(colored('\nNorma I:\t', INFO_COLOR) + colored('||A_init×x - b_init||', ERROR_COLOR))
    print(colored('↪ ', INFO_COLOR) + colored(str(first_norm(a_init, x, b_init)), DISPLAY_COLOR) + '\n')
    print(colored('Norma II:\t', INFO_COLOR) + colored('||x - x_lib||', ERROR_COLOR))
    print(colored('↪ ', INFO_COLOR) + colored(str(second_norm(a, x, b)), DISPLAY_COLOR) + '\n')
    print(colored('Norma III:\t', INFO_COLOR) + colored('||x - A_lib_inv×b_init||', ERROR_COLOR))
    print(colored('↪ ', INFO_COLOR) + colored(str(third_norm(a, x, b)), DISPLAY_COLOR) + '\n')
    print('\n------  Rezultate dupa calcularea inversei  ----')
    pretty_matrix_print(a_inv, 'A_inv')
    print(colored('\nNorma IV:\t', INFO_COLOR) + colored('||A_inv - A_lib_inv||', ERROR_COLOR))
    print(colored('↪ ', INFO_COLOR) + colored(str(fourth_norm(a_init, a_inv)), DISPLAY_COLOR) + '\n')
