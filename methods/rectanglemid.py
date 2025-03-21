class RectangleMid:
    @staticmethod
    def execute(n, func, a, b):
        h = (b - a) / n
        return sum(func(a + (i + 0.5) * h) for i in range(n)) * h
