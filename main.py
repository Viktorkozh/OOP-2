#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Pair:
    def __init__(self, first=0.0, second=0):
        if not isinstance(first, (int, float)) or not isinstance(second, int):
            raise ValueError("Некорректные значения аргументов")

        self.first = float(first)
        self.second = int(second)

    def read(self, prompt=None):
        line = input() if prompt is None else input(prompt)
        parts = line.split()

        if len(parts) != 2:
            raise ValueError("Введите два значения")

        self.first = float(parts[0])
        self.second = int(parts[1])

    def display(self):
        print(f"First: {self.first}, Second: {self.second}")

    def summa(self, work_ddays):
        if work_ddays <= 0:
            raise ValueError(
                "Количество дней в месяце должно быть положительным")

        return self.first / work_ddays * self.second

    def __add__(self, rhs):  # +
        result = self.__clone__()
        result.__iadd__(rhs)
        return result

    def __iadd__(self, rhs):  # +=
        if isinstance(rhs, Pair):
            a = self.first + rhs.first
            b = self.second + rhs.second
            self.first, self.second = a, b
            return self
        else:
            raise ValueError("Illegal type of the argument")

    def __sub__(self, rhs):  # +
        if isinstance(rhs, Pair):
            return Pair(self.first - rhs.first, self.second - rhs.second)
        else:
            raise ValueError("Illegal type of the argument")

    def __isub__(self, rhs):  # +=
        if isinstance(rhs, Pair):
            self.first -= rhs.first
            self.second -= rhs.second
            return self
        else:
            raise ValueError("Illegal type of the argument")

    def __mul__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Pair(self.first * rhs, int(self.second * rhs))
        else:
            raise ValueError("Illegal type of the argument")

    def __imul__(self, rhs):
        if isinstance(rhs, (int, float)):
            self.first *= rhs
            self.second = int(self.second * rhs)
            return self
        else:
            raise ValueError("Illegal type of the argument")

    def __eq__(self, rhs):
        if isinstance(rhs, Pair):
            return self.first == rhs.first and \
                self.second == rhs.second
        return False

    def __lt__(self, rhs):
        if isinstance(rhs, Pair):
            return self.first < rhs.first or \
                (self.first == rhs.first and self.second < rhs.second)
        raise False

    def __gt__(self, rhs):
        if isinstance(rhs, Pair):
            return self.first > rhs.first or \
                (self.first == rhs.first and self.second > rhs.second)
        raise False

    def __repr__(self):
        return f"Pair({self.first}, {self.second})"

    def __clone__(self):
        return Pair(self.first, self.second)

    def __str__(self) -> str:
        return f"Оклад: {self.first}; Отработанные дни: {self.second};"


def make_pair(first, second):
    try:
        return Pair(first, second)
    except ValueError as e:
        print(f"Ошибка: {e}")
        exit(1)


if __name__ == '__main__':
    p1 = make_pair(3000.2501, 20)
    p1.display()
    print(f"Summa: {p1.summa(31)}")

    p2 = make_pair(5640.2501, 10)
    p2.display()
    print(f"Summa: {p2.summa(31)}")

    print(f"Сложение с перегрузкой {p1 + p2}")
    print(f"Вычитание с перегрузкой {p1 - p2}")
    print(f"Умножение с перегрузкой {p1 * 2}")
    print(f"Сравнение с перегрузкой {p1 == p2}")
    print(f"Сравнение с перегрузкой {p1 < p2}")
    print(f"Сравнение с перегрузкой {p1 > p2}")
