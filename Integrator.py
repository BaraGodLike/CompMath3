import math

from methods import rectangleleft, rectangleright, rectanglemid, trapezoid, simpson


class Integrator:
    def __init__(self, func, a, b, eps=1e-6):
        self.func = func
        self.a = a
        self.b = b
        self.eps = eps

    methods = {
        0: {
            "name": "Метод прямоугольников (левый)",
            "func": rectangleleft.RectangleLeft.execute,
        },
        1: {
            "name": "Метод прямоугольников (правый)",
            "func": rectangleright.RectangleRight.execute,
        },
        2: {
            "name": "Метод прямоугольников (средний)",
            "func": rectanglemid.RectangleMid.execute,
        },
        3: {
            "name": "Метод трапеций",
            "func": trapezoid.Trapezoid.execute,
        },
        4: {
            "name": "Метод Симпсона",
            "func": simpson.Simpson.execute
        }
    }

    def try_func(self, x):
        try:
            return self.func(x)
        except (ZeroDivisionError, OverflowError, ValueError):
            return None

    def runge_rule(self, method, n=4):
        I_n = method(n, self.func, self.a, self.b)
        I_2n = method(2 * n, self.func, self.a, self.b)
        while abs(I_n - I_2n) / (2 ** 2 - 1) > self.eps:
            n *= 2
            I_n = method(n, self.func, self.a, self.b)
            I_2n = method(2 * n, self.func, self.a, self.b)
        return I_2n, n

    def find_breakpoints(self, n):
        breakpoints = set()

        if self.try_func(self.a) is None:
            breakpoints.add(self.a)

        if self.try_func(self.b) is None:
            breakpoints.add(self.b)

        if self.try_func((self.a + self.b) / 2) is None:
            breakpoints.add((self.a + self.b) / 2)

        h = (self.b - self.a) / n
        for i in range(n):
            point = self.a + i * h
            if self.try_func(self.a + i * h) is None:
                breakpoints.add(point)

        return list(breakpoints)

    def is_convergent(self, breakpoints):
        for bp in breakpoints:
            y1 = self.try_func(bp - self.eps)
            y2 = self.try_func(bp + self.eps)
            if ((y1 is not None)
                    and (y2 is not None) and ((abs(y1 - y2) > self.eps) or (y1 == y2 and y1 is not None))):
                return False
        return True

    def integrate(self, method_number):
        """
            'rectangle_left': 0 \n
            'rectangle_right': 1 \n
            'rectangle_mid': 2 \n
            'trapezoid': 3 \n
            'simpson': 4
        """
        breakpoints = self.find_breakpoints(int((self.b - self.a) * 1000))
        method = self.methods[method_number]["func"]

        if len(breakpoints) == 0:
            return self.runge_rule(method)

        if not self.is_convergent(breakpoints):
            raise Exception("Интеграл не существует")

        # ОДНА ТОЧКА РАЗРЫВА
        if len(breakpoints) == 1:
            if self.a in breakpoints:
                self.a += self.eps
            elif self.b in breakpoints:
                self.b -= self.eps

        # МНОЖЕСТВО ТОЧЕК РАЗРЫВА
        else:
            res = 0
            n = 0

            # РАЗРЫВ В ПЕРВОМ ПОДИНТЕРВАЛЕ
            if not (self.try_func(self.a) is None or self.try_func(breakpoints[0] - self.eps) is None):
                integrator = Integrator(self.func, self.a, breakpoints[0] - self.eps, self.eps)
                results = integrator.integrate(method_number)
                res += results[0]
                n += results[1]

            # РАЗРЫВ В ПОСЛЕДНЕМ ПОДИНТЕРВАЛЕ
            if not (self.try_func(self.b) is None or self.try_func(breakpoints[0] + self.eps) is None):
                integrator = Integrator(self.func, breakpoints[0] + self.eps, self.b, self.eps)
                results = integrator.integrate(method_number)
                res += results[0]
                n += results[1]

            # ОСТАЛЬНЫЕ РАЗРЫВЫ
            for break_index in range(len(breakpoints) - 1):
                break_cur = breakpoints[break_index]
                break_next = breakpoints[break_index + 1]

                if not (self.try_func(break_cur + self.eps) is None or self.try_func(break_next - self.eps) is None):
                    integrator = Integrator(self.func, break_cur + self.eps, break_next - self.eps, self.eps)
                    results = integrator.integrate(method_number)
                    res += results[0]
                    n += results[1]
            return res, n

        if not breakpoints or self.a - self.eps in breakpoints or self.b + self.eps in breakpoints:
            return self.runge_rule(method)
