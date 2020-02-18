def fibonacci(n):
    '''Generate Fibonacci numbers.
    '''

    a, b = 0, 1
    for _ in range(n):
        yield b
        a, b = b, a + b
