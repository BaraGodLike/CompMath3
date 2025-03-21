class Trapezoid:
    @staticmethod
    def execute(n, func, a, b):
        h = (b - a) / n
        return (func(a) + func(b) + 2 * sum(func(a + i * h) for i in range(1, n))) * h / 2
