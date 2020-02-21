from bsuir_2020_python.lab1.sources.fibonacci import fibonacci


class TestFibonacci:
    def test_empty(self):
        assert list(fibonacci(0)) == []

    def test_simple(self):
        assert list(fibonacci(6)) == [1, 1, 2, 3, 5, 8]
