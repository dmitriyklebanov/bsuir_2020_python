from ..fibonacci import fibonacci

import unittest


class TestFibonacci(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(list(fibonacci(0)), [])

    def test_simple(self):
        self.assertEqual(list(fibonacci(6)), [1, 1, 2, 3, 5, 8])
