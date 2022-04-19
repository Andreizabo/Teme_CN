import json
import math
import numpy as np


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
        self.xi = {}
        self.n = 100
        self.generate_x_array()
        print(self.xi)

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
            self.xi[xi] = self.function(xi)


if __name__ == "__main__":
    fxa = FunctionApproximator('input1.txt')
