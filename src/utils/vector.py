from typing import Union

ArrayTarget = Union[list ,tuple, float, int]

class Vector(list[float]):
    def __init__(self, values):
        if isinstance(values, tuple):
            values = list(values)
        super().__init__(values)

    def __add__(self, other: ArrayTarget):
        if isinstance(other, (int, float)):
            return Vector([x + other for x in self])
        elif isinstance(other, (list, tuple, Vector)):
            if len(other) != len(self):
                raise ValueError("Vectors must have the same length for element-wise addition.")
            return Vector([x + y for x, y in zip(self, other)])
        else:
            raise TypeError("Unsupported operand type for +: '{}'".format(type(other).__name__))
    
    def __sub__(self, other: ArrayTarget):
        if isinstance(other, (int, float)):
            return Vector([x - other for x in self])
        elif isinstance(other, (list, tuple)):
            if len(other) != len(self):
                raise ValueError("Vectors must have the same length for element-wise subtraction.")
            return Vector([x - y for x, y in zip(self, other)])
        else:
            raise TypeError("Unsupported operand type for -: '{}'".format(type(other).__name__))

    def __mul__(self, other: ArrayTarget):
        if isinstance(other, (int, float)):
            return Vector([x * other for x in self])
        elif isinstance(other, (list, tuple)):
            if len(other) != len(self):
                raise ValueError("Vectors must have the same length for element-wise multiplication.")
            return Vector([x * y for x, y in zip(self, other)])
        else:
            raise TypeError("Unsupported operand type for *: '{}'".format(type(other).__name__))
    
    def __truediv__(self, other: ArrayTarget):
        if isinstance(other, (int, float)):
            return Vector([x / other for x in self])
        elif isinstance(other, (list, tuple)):
            if len(other) != len(self):
                raise ValueError("Vectors must have the same length for element-wise division.")
            return Vector([x / y for x, y in zip(self, other)])
        else:
            raise TypeError("Unsupported operand type for /: '{}'".format(type(other).__name__))