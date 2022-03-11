import copy
from termcolor import colored
from tqdm import tqdm

INFO_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
DISPLAY_COLOR = "blue"

eps = 10 ** -6


def exists(matrix, i, j):
    for index, element in enumerate(matrix[i]):
        if element[1] == j:
            return index
    return -1


def find_element(vect, index):
    for element in vect:
        if element[1] == index:
            return element[0]
    return None


def get_sym(matrix, c):
    col = []
    for index, line in enumerate(matrix):
        for element in line:
            if element[1] == c and element[1] != index:
                col += [(element[0], index)]
    return col


def reconstruct_line(line, sym):
    return sorted(line + sym, key=lambda x: x[1])


def insert_in_matrix(matrix, lin, col, val):
    index = exists(matrix, lin, col)
    if index == -1:
        matrix[lin] += [(val, col)]
    else:
        matrix[lin][index] = (matrix[lin][index][0] + val, matrix[lin][index][1])


def read_sparse_matrix(path):
    with open(path, 'r') as rd:
        try:
            n = int(rd.readline())
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

            insert_in_matrix(matrix, elements[1], elements[2], elements[0])
            line = rd.readline()
    return matrix


def verify_equality(m1, m2):
    global eps
    for line_index in range(len(m1)):
        for element in m1[line_index]:
            index = exists(m2, line_index, element[1])
            if index == -1 or abs(element[0] - m2[line_index][index][0]) >= eps:
                return False
    return True


def sum_matrix(m1, m2):
    m3 = copy.deepcopy(m1)
    for line_index in range(len(m2)):
        for element in m2[line_index]:
            insert_in_matrix(m3, line_index, element[1], element[0])
    return m3


def prod_matrix(m1, m2):
    n = len(m1)
    m3 = [[] for _ in range(n)]

    # Optimization, we store reconstructed columns as to not recalculate them
    reconstructed_columns = [None for _ in range(n)]

    for line in tqdm(range(n)):
        sym_line = get_sym(m1, line)
        if len(m1[line]) + len(sym_line) == 0:
            continue
        reconstructed_line = reconstruct_line(m1[line], sym_line)
        for column in range(line + 1):
            if reconstructed_columns[column] is not None:
                reconstructed_column = reconstructed_columns[column]
            else:
                sym_column = get_sym(m2, column)
                reconstructed_column = reconstruct_line(m2[column], sym_column)
                reconstructed_columns[column] = reconstructed_column
            if len(reconstructed_column) == 0:
                continue
            value = 0
            for element in reconstructed_line:
                col_val = find_element(reconstructed_column, element[1])
                if col_val is not None:
                    value += col_val * element[0]
            if value != 0:
                insert_in_matrix(m3, line, column, value)
    return m3


if __name__ == '__main__':
    a = read_sparse_matrix('a.txt')
    b = read_sparse_matrix('b.txt')
    verify_prod = read_sparse_matrix('a_ori_a.txt')
    verify_sum = read_sparse_matrix('a_plus_b.txt')
    print(verify_equality(sum_matrix(a, b), verify_sum))
    print(verify_equality(prod_matrix(a, a), verify_prod))
