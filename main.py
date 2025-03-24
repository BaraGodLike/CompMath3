import Integrator
import functions
try:
    for i in range(len(functions.functions)):
        print(f"{i}. {functions.functions[i]['name']}")

    func = None
    a = -float("inf")
    b = float("inf")
    eps = -1.0
    method_num = -1
    try:
        func = functions.functions[int(input("Введите номер функции: "))]["func"]
    except ValueError:
        raise ValueError("Некорректный номер функции!")
    except KeyError:
        raise ValueError("Некорректный номер функции!")

    try:
        print("ВАЖНО! Верхний предел интегрирования должен быть больше нижнего!")
        a = float(input("Введите нижний предел интегрирования: "))
        b = float(input("Введите верхний предел интегрирования: "))
        if a >= b:
            raise ValueError
    except ValueError:
        raise ValueError("Некорректный предел интегрирования")

    try:
        eps = float(input("Введите точность вычислений: "))
    except ValueError:
        raise ValueError("Некорректная точность вычислений")

    integrator = Integrator.Integrator(func, a, b, eps)

    for i in range(len(integrator.methods)):
        print(f"{i}. {integrator.methods[i]['name']}")

    try:
        method_num = int(input("Введите номер метода: "))
        if method_num >= len(integrator.methods) or method_num < 0:
            raise ValueError
        result = integrator.integrate(method_num)
        print(f"Значение интеграла: {result[0]}, число разбиения интервала: {result[1]}")
    except ValueError:
        raise ValueError("Некорректный номер метода")
except Exception as e:
    print(e.args[0])
