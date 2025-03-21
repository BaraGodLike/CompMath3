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

    def runge_rule(self, method, n=4):
        I_n = method(n, self.func, self.a, self.b)
        I_2n = method(2 * n, self.func, self.a, self.b)
        while abs(I_n - I_2n) / (2 ** 2 - 1) > self.eps:
            n *= 2
            I_n = method(n, self.func, self.a, self.b)
            I_2n = method(2 * n, self.func, self.a, self.b)
        return I_2n, n

    def integrate(self, method_number):
        """
                'rectangle_left': 0 \n
                'rectangle_right': 1 \n
                'rectangle_mid': 2 \n
                'trapezoid': 3 \n
                'simpson': 4
            """
        method = self.methods[method_number]["func"]
        if method:
            return self.runge_rule(method)
        else:
            raise Exception("Неизвестный метод")
