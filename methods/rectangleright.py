class RectangleRight:
    @staticmethod
    def execute(n, func, a, b):
        h = (b - a) / n
        return sum(func(a + i * h) for i in range(n)) * h
