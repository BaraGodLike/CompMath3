class Simpson:
    @staticmethod
    def execute(n, func, a, b):
        h = (b - a) / n
        return (func(a) + func(b) + 4 * sum(
            func(a + (i + 0.5) * h) for i in range(n)) + 2 * sum(
            func(a + i * h) for i in range(1, n))) * h / 6
