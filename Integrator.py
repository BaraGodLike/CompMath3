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
        while abs(I_n - I_2n) / (2 ** (4 if method == simpson.Simpson.execute else 2) - 1) > self.eps:
            n *= 2
            I_n = method(n, self.func, self.a, self.b)
            I_2n = method(2 * n, self.func, self.a, self.b)
        return abs(I_2n), n

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
            if ((y1 is not None) and (y2 is not None) and (abs(y1 - y2) > self.eps)) or (y1 is None and y2 is None):
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
        parity = self.get_parity()
        if (abs(self.a) == abs(self.b)) and parity >= 0:
            return 0, 0

        if parity >= 0:
            if abs(self.a) < self.b:
                self.a = abs(self.a)
            else:
                self.b = -self.b

        breakpoints = self.find_breakpoints(int((self.b - self.a) * (1 / self.eps)))
        method = self.methods[method_number]["func"]

        if len(breakpoints) == 0:
            return self.runge_rule(method)

        if not self.is_convergent(breakpoints):
            raise Exception("Интеграл не существует")

        # ОДНА ТОЧКА РАЗРЫВА
        if len(breakpoints) == 1:
            if self.a in breakpoints:
                self.a += self.eps * self.eps
            elif self.b in breakpoints:
                self.b -= self.eps * self.eps
            return self.runge_rule(method)
        # МНОЖЕСТВО ТОЧЕК РАЗРЫВА
        else:
            res = 0
            n = 0

            # РАЗРЫВ В ПЕРВОМ ПОДИНТЕРВАЛЕ
            if not (self.try_func(self.a) is None or self.try_func(breakpoints[0] - self.eps * self.eps) is None):
                integrator = Integrator(self.func, self.a, breakpoints[0] - self.eps * self.eps, self.eps)
                results = integrator.integrate(method_number)
                res += results[0]
                n += results[1]

            # РАЗРЫВ В ПОСЛЕДНЕМ ПОДИНТЕРВАЛЕ
            if not (self.try_func(self.b) is None or self.try_func(breakpoints[0] + self.eps * self.eps) is None):
                integrator = Integrator(self.func, breakpoints[0] + self.eps * self.eps, self.b, self.eps)
                results = integrator.integrate(method_number)
                res += results[0]
                n += results[1]

            # ОСТАЛЬНЫЕ РАЗРЫВЫ
            for break_index in range(len(breakpoints) - 1):
                break_cur = breakpoints[break_index]
                break_next = breakpoints[break_index + 1]

                if not (self.try_func(break_cur + self.eps * self.eps) is None or self.try_func(
                        break_next - self.eps * self.eps) is None):
                    integrator = Integrator(self.func, break_cur + self.eps * self.eps,
                                            break_next - self.eps * self.eps, self.eps)
                    results = integrator.integrate(method_number)
                    res += results[0]
                    n += results[1]
            return res, n

    def get_parity(self):
        if self.a * self.b > 0:
            return -1

        start = max(self.a, -self.b)
        end = min(abs(self.a), self.b)

        points = {end}
        for i in range(0, int((end - start) / self.eps)):
            points.add(abs(start + i * self.eps))

        is_even = True
        is_odd = True
        for i in points:
            if not is_even and not is_odd:
                return -1

            y = self.try_func(i)
            y_ = self.try_func(-i)

            if y is None and y == y_:
                continue

            if y is None and not(y_ is None):
                return -1

            if y_ is None and not(y is None):
                return -1

            if y != y_:
                is_even = False

            if y != -y_:
                is_odd = False

        if is_even:
            return 0
        if is_odd:
            return 1
        return -1
