import math


def func1(x):
    """x ^ 3 - 5 * x ^ 2 + 3 * x - 16"""
    return x ** 3 - 5 * x ** 2 + 3 * x - 16


def func2(x):
    """-x ^ 3 - x ^ 2 - 2 * x + 1"""
    return -x ** 3 - x ** 2 - 2 * x + 1


def func3(x):
    """-3 * x ^ 3 - 5 * x ^ 2 + 4 * x - 2"""
    return -3 * x ** 3 - 5 * x ** 2 + 4 * x - 2


def func4(x):
    """1 / (1 - x)"""
    return 1 / (1 - x)


def func5(x):
    """1 / sqrt(x)"""
    return 1 / math.sqrt(x)


def func6(x):
    """1 / sqrt(1 - x)"""
    return 1/math.sqrt(1 - x)


functions = {
    0: {
        "name": "x ^ 3 - 5 * x ^ 2 + 3 * x - 16",
        "func": func1
    },
    1: {
        "name": "-x ^ 3 - x ^ 2 - 2 * x + 1",
        "func": func2
    },
    2: {
        "name": "-3 * x ^ 3 - 5 * x ^ 2 + 4 * x - 2",
        "func": func3
    },
    3: {
        "name": "1 / (1 - x)",
        "func": func4
    },
    4: {
        "name": "1 / sqrt(x)",
        "func": func5
    },
    5: {
        "name": "1 / sqrt(1 - x)",
        "func": func6
    },
}
