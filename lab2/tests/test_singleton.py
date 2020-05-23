from lab2.sources.singleton import Singleton


@Singleton
class SomeClass:
    def __init__(self, val):
        self.val = val


class TestSingleton:
    def test_simple(self):
        a = SomeClass.get_instance(4)
        b = SomeClass.get_instance(5)
        assert a is b
        assert a.val == b.val == 4

    def test_access(self):
        a = SomeClass.get_instance(4)
        a.val = 5
        assert a.val == 5
