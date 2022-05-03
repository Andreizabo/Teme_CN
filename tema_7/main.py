import random
from termcolor import colored

class PolynomeSolver:
    def __init__(self, path):
        '''
        Constructs a solver for the given polynome (it needs a file to read each coefficient).
        '''
        self.eps = 10 ** -7
        self.ai = []
        self.solutions = []

        # Read coefficient
        with open(path, "r") as fin:
            try:
                self.ai = [int(x) for x in fin.readline().split()]
                self.solutions = fin.readline().split()
            except:
                print(colored(f"[ERROR] Invalid number in {path}", 'red'))
                exit()

        self.R = (abs(self.ai[0]) + max([abs(x) for x in self.ai[1:]])) / abs(self.ai[0])

    def P(self, x):
        '''
        Calculates the value of the polynome in the given point.
        '''
        result = 0
        n = len(self.ai)
        for i in range(n):
            result += self.ai[i] * (x ** (n - i - 1))
        return result

    def solve(self, debug_mode = False):
        '''
        Function for finding the roots of the polynome using Dehghan method.
        '''
        kmax = 10000
        k = 0
        xk = random.uniform(-self.R, self.R)
        delta_x = 1

        xk_orig = xk
        while abs(delta_x) >= self.eps and abs(delta_x) <= 10 ** 8 and k < kmax:
            if abs(self.P(xk)) < self.eps / 10:
                delta_x = 0
            else:
                Pxk = self.P(xk)
                Pxk_plus = self.P(xk + Pxk)
                Pxk_minus = self.P(xk - Pxk)
                yk = xk - ((2 * Pxk * Pxk) / (Pxk_plus - Pxk_minus))
                Pyk = self.P(yk)

                delta_x = 2 * Pxk * (Pxk + Pyk) / (Pxk_plus - Pxk_minus)

            xk = xk - delta_x
            k = k + 1

            if debug_mode: 
                print(f'Iteration {k}, delta_x = {delta_x}, new xk = {xk}')
            
        if debug_mode: 
            print(f'Original xk = {xk_orig}')

        if abs(delta_x) < self.eps:
            if debug_mode:
                print(colored(f'Solution (approx) : {xk}', 'green'))
                print(colored(f'Actual solutions : {self.solutions}', 'cyan'))
            output_str = f'Solution (approx) : {xk}\nActual solutions : {self.solutions}'
            return xk, output_str
        else:
            if debug_mode:
                print(colored(f'Divergent, try with another x0 (result : {xk})', 'red'))
            output_str = f'Divergent, try with another x0 (result : {xk})'
            return None, output_str

    def find_all_solutions(self):
        sols = []
        while len(sols) != len(self.solutions):
            result = None
            while result == None:
                result, output_str = self.solve()
            
            exists = False
            for i in range(len(sols)):
                if abs(sols[i] - result) < 0.0001:
                    exists = True
            if abs(self.P(result)) > self.eps:
                continue
            if not exists:
                sols.append(result)
        return sols

ps1 = PolynomeSolver('polynome1.txt')
ps2 = PolynomeSolver('polynome2.txt')
ps3 = PolynomeSolver('polynome3.txt')
ps4 = PolynomeSolver('polynome4.txt')

if __name__ == "__main__":
    ps1.solve()
    ps2.solve()
    ps3.solve()
    ps4.solve()

    print(ps1.find_all_solutions(), ps1.solutions)
    print(ps3.find_all_solutions(), ps3.solutions)
    print(ps4.find_all_solutions(), ps4.solutions)
    print(ps2.find_all_solutions(), ps2.solutions)

# For GUI
if __name__ == "main":
    selected_polynome = None