import math as mt


class Vector:
    '''Implements mathematical Vector.
    '''
    def __init__(self, iterable):
        if iterable is None:
            self.__values = []
            return
        for item in iterable:
            if not isinstance(item, (int, float)):
                raise TypeError('Vector should be numerical, '
                                f'{type(item).__name__} provided.')
        self.__values = list(iterable)

    @property
    def length(self):
        '''Return norm of the Vector.
        '''
        sqr_length = 0
        for item in self.__values:
            sqr_length += item ** 2
        return mt.sqrt(sqr_length)

    def __len__(self):
        '''Return dimension of the Vector.
        '''
        return len(self.__values)

    def __bool__(self):
        '''Return true if all elements of the Vector are zero.
        '''
        return not sum(map(bool, self.__values))

    def __str__(self):
        return '(' + ', '.join(map(str, self.__values)) + ')'

    def __getitem__(self, key):
        return self.__values[key]

    def __setitem__(self, key, value):
        '''Raises ValueError if value is not numeric.
        '''
        if not isinstance(value, (int, float)):
            raise TypeError('Value should be numerical, '
                             f'{type(value).__name__} provided.')

        self.__values[key] = value

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.__values == other.__values

    def __elementwise_operation(self, other, operation):
        if not isinstance(other, Vector):
            raise TypeError('Value for elementwise operation should be Vector,'
                             f'{type(other).__name__} provided.')
        if len(self) != len(other):
            raise ValueError('Vectors should have the same dimension.')

        return Vector([operation(l, r) for l, r in zip(self.__values, other.__values)])

    def __add__(self, other):
        '''Elementwise addition.
        '''
        return self.__elementwise_operation(other, lambda a, b: a + b)

    def __sub__(self, other):
        '''Elementwise subtraction.
        '''
        return self.__elementwise_operation(other, lambda a, b: a - b)

    def __scalar_operation(self, other, operation):
        if not isinstance(other, (int, float)):
            raise TypeError('Value for scalar operation should be numerical,'
                             f'{type(other).__name__} provided.')

        return Vector([operation(item, other) for item in self.__values])

    def __mul__(self, other):
        '''Scalar multiplication.
        '''
        return self.__scalar_operation(other, lambda a, b: a * b)

    def __truediv__(self, other):
        '''Scalar division.
        '''
        return self.__scalar_operation(other, lambda a, b: a / b)

    def __floordiv__(self, other):
        '''Scalar integer division.
        '''
        return self.__scalar_operation(other, lambda a, b: a // b)

    def __rmul__(self, other):
        '''Scalar multiplication.
        '''
        return self.__scalar_operation(other, lambda a, b: a * b)

    def __matmul__(self, other):
        '''Scalar product.
        '''
        return sum(self.__elementwise_operation(other, lambda a, b: a * b).__values)

    def __imatmul__(self, other):
        '''Raises ArithmeticError. Scalar product is a number.
        '''
        raise ArithmeticError('Scalar product is a number.')
