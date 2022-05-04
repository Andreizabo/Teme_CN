import json
import math
import numpy as np
import random
import matplotlib.pyplot as plotter


def str_to_function(string):
    if string == 'function1':
        return function1
    elif string == 'function2':
        return function2
    elif string == 'function3':
        return function3


def function1(x):
    return x ** 2 - 12 * x + 30


def function2(x):
    return math.sin(x) - math.cos(x)


def function3(x):
    return 2 * x ** 3 - 3 * x + 15


class FunctionApproximator:
    def __init__(self, path):
        self.input_path = path
        items = self.read_input()
        self.function = str_to_function(items['function'])
        self.x0 = items["x0"]
        self.xn = items["xn"]
        self.xi = []
        self.n = 100
        self.generate_x_array()
        self.eps = 10 ** -7
        self.y = []
        self.aitken()
        self.a = []
        self.polynomial_approximation()

    def is_zero(self, x):
        if abs(x) < abs(self.eps):
            return 0
        return x

    def read_input(self):
        try:
            with open(self.input_path, 'r') as rd:
                items = {}
                ln = rd.readline()
                items['x0'] = float(ln.strip())
                ln = rd.readline()
                items['xn'] = float(ln.strip())
                ln = rd.readline()
                items['function'] = ln.strip()
            return items
        except:
            print(f'Error at input!')
            exit()

    def generate_x_array(self):
        for xi in np.arange(self.x0, self.xn + (self.xn - self.x0) / self.n, (self.xn - self.x0) / self.n):
            self.xi.append((xi, self.function(xi)))

    def aitken(self):
        # Aitken
        div_dif = [[0.0 for _ in range(self.n + 1)] for _ in range(self.n + 1)]
        div_dif[0][0] = self.xi[0][1]
        for i in range(self.n):
            div_dif[i][i + 1] = self.is_zero((self.xi[i + 1][1] - self.xi[i][1]) / (self.xi[i + 1][0] - self.xi[i][0]))
        for k in range(1, self.n):
            for i in range(self.n - k):
                div_dif[i][i + 1 + k] = self.is_zero((div_dif[i + 1][i + 1 + k] - div_dif[i][i + k]) / (self.xi[i + 1 + k][0] - self.xi[i][0]))
        self.y = [div_dif[0][i] for i in range(self.n + 1)]

    def newton(self, x):
        return self.y[0] + sum(self.y[i] * math.prod([x - self.xi[j][0] for j in range(i)]) for i in range(1, self.n + 1))

    def verify_aitken_newton(self):
        for index in range(self.n):
            print(f'{self.xi[index][1]}\t{self.newton(self.xi[index][0])}\t{(self.xi[index][1] - self.newton(self.xi[index][0]))}')

    def polynomial_approximation(self):
        m = 6

        def sum1(i, j, n):
            result = 0
            for k in range(n + 1):
                result += self.xi[k][0] ** (i + j)
            return result

        def sum2(i, n):
            result = 0
            for k in range(n + 1):
                result += self.xi[k][1] * (self.xi[k][0] ** i)
            return result

        B = np.zeros((m + 1, m + 1))
        f = np.zeros((m + 1, 1))

        for i in range(m + 1):
            f[i][0] = sum2(i, self.n)
            for j in range(m + 1):
                B[i][j] = sum1(i, j, self.n)

        self.a, residuals, rank, s = np.linalg.lstsq(B, f)

    def calculate_polynom(self, x):
        return sum(self.a[i] * (x ** i) for i in range(len(self.a)))[0]

    def verify_polynom(self):
        for index in range(self.n):
            print(f'{self.xi[index][1]}\t{self.calculate_polynom(self.xi[index][0])}\t{(self.xi[index][1] - self.calculate_polynom(self.xi[index][0]))}')

    def pick_random_x(self):
        random_index = random.randint(0, self.n)
        return random.uniform(self.xi[random_index][0], self.xi[random_index + 1][0])

    def test_x(self, x):
        newton_x = self.newton(x)
        poly_x = self.calculate_polynom(x)
        func_x = self.function(x)
        return newton_x, poly_x, func_x, self.is_zero(abs(func_x - newton_x)), self.is_zero(abs(func_x - poly_x))

    def plot(self, functions):
        x = [self.xi[i][0] for i in range(self.n + 1)]
        for fc in functions:
            y = [fc(xi) for xi in x]
            plotter.plot(x, y, label=f'{fc.__name__.replace("self.", "")}')
        plotter.xlabel('X axis')
        plotter.ylabel('Y axis')
        plotter.title(f'Comparing {", ".join([fc.__name__.replace("self.", "") for fc in functions])}')
        plotter.legend()
        plotter.show()


if __name__ == "__main__":
    fxa = FunctionApproximator('input1.txt')
    print(fxa.test_x(fxa.pick_random_x()))
    fxa.plot([fxa.newton, fxa.calculate_polynom, function1])
