from bsuir_2020_python.lab2.sources.singleton import Singleton


@Singleton
class SomeClass:
    def __init__(self, val):
        self.val = val


class TestSingleton:
    def test_simple(self):
        a = SomeClass(4)
        b = SomeClass(5)
        assert a.val == b.val == 4

    def test_access(self):
        a = SomeClass(4)
        a.val = 5
        assert a.val == 5
