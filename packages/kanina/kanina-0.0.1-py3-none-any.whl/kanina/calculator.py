


import math

class Calculator:
    """
    A simple calculator class with memory function
    """
    def __init__(self, value: float = 0):
        self.__value = value

    def reset(self):
        self.__value = 0

    def cval(self) -> float:
        return self.__value

    def add(self, num:float) -> float:
        self.__value = self.__value + num
        return self.__value

    def sub(self, num:float) -> float:
        self.__value = self.__value - num
        return self.__value

    def mult(self, num:float) -> float:
        self.__value = self.__value * num
        return self.__value

    def div(self, num:float) -> float:
        self.__value = self.__value / num
        return self.__value

    def pow(self, num:float) -> float:
        self.__value = self.__value ** num
        return self.__value

    def root(self, num:float) -> float:
        if self.__value < 0 and num % 2 == 0:
            raise ValueError('Math domain error')
        self.__value = math.pow(abs(self.__value), 1. / num) * (1, -1)[self.__value < 0]
        return self.__value
