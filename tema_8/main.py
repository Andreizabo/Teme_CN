import math
import random


def function1(x):
    return (x ** 3) / 3 - 2 * (x ** 2) + 2 * x + 3


def function2(x):
    return x ** 2 + math.sin(x)


def function3(x):
    return x ** 4 - 6 * (x ** 3) + 13 * (x ** 2) - 12 * x + 4


class FunctionMinimizer:
    def __init__(self, func=function1):
        self.function = func
        self.eps = 10 ** -6
        self.h = 10 ** -6
        self.max_k = 10000
        pass

    def g1(self, x):
        return (3 * self.function(x) - 4 * self.function(x - self.h) + self.function(x - 2 * self.h)) / (2 * self.h)

    def g2(self, x):
        return (-self.function(x + 2 * self.h) + 8 * self.function(x + self.h) - 8 * self.function(x - self.h) + self.function(x - 2 * self.h)) / (12 * self.h)

    def second_derivative(self, x):
        return (-self.function(x + 2 * self.h) + 16 * self.function(x + self.h) - 30 * self.function(x) + 16 * self.function(x - self.h) - self.function(x - 2 * self.h)) / (12 * self.h ** 2)

    def steffensen(self, x, derivative):
        k = 0
        delta_x = 1
        while k <= self.max_k and self.eps <= abs(delta_x) <= 10 ** 8:
            g_x = derivative(x)
            divisor = derivative(x + g_x) - g_x
            if abs(divisor) <= self.eps:
                return x, k
            delta_x = (g_x ** 2) / divisor
            x -= delta_x
            k += 1
        if abs(delta_x) < self.eps:
            return x, k
        else:
            return "Divergence", k

    def find_x(self, g):
        x, k = self.steffensen(random.uniform(-5, 5), g)
        while x == 'Divergence' or self.second_derivative(x) <= 0:
            x, k = self.steffensen(random.uniform(-5, 5), g)
        return x, k

    def compare_results(self):
        g1_x, g1_k = self.find_x(self.g1)
        g2_x, g2_k = self.find_x(self.g2)
        print(f'Using G1 we found x* = {g1_x} in {g1_k} steps.')
        print(f'Using G2 we found x* = {g2_x} in {g2_k} steps.')
        return f'Using G1 we found x* = {g1_x} in {g1_k} steps.\nUsing G2 we found x* = {g2_x} in {g2_k} steps.'

if __name__ == "__main__":
    fm = FunctionMinimizer()
    fm.compare_results()

if __name__ == "main":
    f1 = FunctionMinimizer(function1)
    f2 = FunctionMinimizer(function2)
    f3 = FunctionMinimizer(function3)

    selected_function = f1