import math


# Ex 1
def find_u():
    u = 1
    while u / 10 + 1 != 1:
        u /= 10
    print(f'[Ex 1] u = {u}')
    return u


# Ex 2
def verify_u(u):
    a = 1.0
    b = u / 10
    c = u / 10
    print(f'[Ex 2] Adunarea nu e asociativa: {((a + b) + c, a + (b + c))}')
    print(f'[Ex 2] Inmultirea nu e asociativa: {(u * 10) * 0.1, (u * 0.1) * 10}')


# Ex 3
def pq4(y, a0, a1, a2, a3, a4):
    return a0 + y * (a1 + y * (a2 + y * (a3 + y * a4)))


def approx_sin(x):
    a0 = 1805490264.690988571178600370234394843221
    a1 = -164384678.227499837726129612587952660511
    a2 = 3664210.647581261810227924465160827365
    a3 = -28904.140246461781357223741935980097
    a4 = 76.568981088717405810132543523682
    b0 = 2298821602.638922662086487520330827251172
    b1 = 27037050.118894436776624866648235591988
    b2 = 155791.388546947693206469423979505671
    b3 = 540.567501261284024767779280700089
    b4 = 1.0
    p = pq4(x ** 2, a0, a1, a2, a3, a4)
    q = pq4(x ** 2, b0, b1, b2, b3, b4)
    math_sin = math.sin(x * math.pi / 4)
    estimate_sin = x * (p / (q if abs(q) >= 10 ** -12 else 10 ** -12))
    print(f'[Ex 3] Pentru x = {x}, sin(¼×π×{x}) = {math_sin}, approx_sin({x}) = {estimate_sin}, diferenta = {abs(math_sin - estimate_sin)}')


def approx_cos(x):
    a0 = 1090157078.174871420428849017262549038606
    a1 = -321324810.993150712401352959397648541681
    a2 = 12787876.849523878944051885325593878177
    a3 = -150026.206045948110568310887166405972
    a4 = 538.333564203182661664319151379451
    b0 = 1090157078.174871420428867295670039506886
    b1 = 14907035.776643879767410969509628406502
    b2 = 101855.811943661368302608146695082218
    b3 = 429.772865107391823245671264489311
    b4 = 1.0
    p = pq4(x ** 2, a0, a1, a2, a3, a4)
    q = pq4(x ** 2, b0, b1, b2, b3, b4)
    math_cos = math.cos(x * math.pi / 4)
    estimate_cos = p / (q if abs(q) >= 10 ** -12 else 10 ** -12)
    print(f'[Ex 3] Pentru x = {x}, cos(¼×π×{x}) = {math_cos}, approx_cos({x}) = {estimate_cos}, diferenta = {abs(math_cos - estimate_cos)}')


def approx_ln(x):
    a0 = 75.151856149910794642732375452928
    a1 = -134.730399688659339844586721162914
    a2 = 74.201101420634257326499008275515
    a3 = -12.777143401490740103758406454323
    a4 = 0.332579601824389206151063529971
    b0 = 37.575928074955397321366156007781
    b1 = -79.890509202648135695909995521310
    b2 = 56.215534829542094277143417404711
    b3 = -14.516971195056682948719125661717
    b4 = 1.0
    z = (x - 1) / (x + 1)
    p = pq4(z ** 2, a0, a1, a2, a3, a4)
    q = pq4(z ** 2, b0, b1, b2, b3, b4)
    math_ln = math.log(x, math.e)
    estimate_ln = z * (p / (q if abs(q) >= 10 ** -12 else 10 ** -12))
    print(f'[Ex 3] Pentru x = {x}, ln({x}) = {math_ln}, approx_ln({x}) = {estimate_ln}, diferenta = {abs(math_ln - estimate_ln)}')


if __name__ == "__main__":
    u = find_u()
    verify_u(u)
    approx_sin(float(input()))
    approx_cos(float(input()))
    approx_ln(float(input()))


