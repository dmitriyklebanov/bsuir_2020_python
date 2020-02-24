from lab2.sources.cached import cached

import pytest
import random
import warnings


@cached
def get_random_number(a, b, *args, **kwars):
    print(a, b)
    return random.randint(a, b)


@cached
def get_number(a, b, *args, **kwars):
    return (a + b) // 2


class TestCached:
    def initialize(self):
        random.seed(42)

    def test_simple(self):
        self.initialize()
        for i in range(100):
            assert get_random_number(1, 2) == get_random_number(1, 2)

    def test_hashable_types(self):
        self.initialize()
        tpl = (1, 2.0, '123', None, True)
        for i in range(100):
            assert get_random_number(1, 2, tpl) == get_random_number(1, 2, tpl)

    def test_runtime_warning_unhashable_types(self):
        unhashable = {1: 2, 3: 4}
        with pytest.warns(RuntimeWarning):
            get_number(1, 2, unhashable)

    def test_unhashable_types(self):
        warnings.simplefilter("ignore")
        assert get_number(1, 2, {1: 2, 3: 4}) == 1
