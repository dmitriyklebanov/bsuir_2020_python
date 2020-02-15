from ..utils import find_id, partition, merge, copy

import unittest


class TestFindId(unittest.TestCase):
    def test_empty(self):
        elems = []
        self.assertEqual(find_id(elems, 0, 0, lambda x: False), 0)

    def test_invalid_bounds(self):
        elems = [1, 2, 3, 4]
        self.assertEqual(find_id(elems, 1, 0, lambda x: False), 0)

    def test_right_bound(self):
        elems = [1, 2, 3, 4]
        self.assertEqual(find_id(elems, 0, 4, lambda x: False), 4)

    def test_out_of_bounds(self):
        elems = []
        with self.assertRaises(IndexError):
            find_id(elems, 1, 4, lambda x: False)


class TestPartition(unittest.TestCase):
    def test_empty(self):
        elems = []
        self.assertEqual(partition(elems, 0, 0, 1), 0)
        self.assertEqual(elems, [])

    def test_invalid_bounds(self):
        elems = [1, 2, 3, 4]
        self.assertEqual(partition(elems, 1, 0, 0), 0)
        self.assertEqual(elems, [1, 2, 3, 4])

    def test_right_bound(self):
        elems = [1, 2, 3, 4]
        self.assertEqual(partition(elems, 0, 4, 5), 4)
        self.assertEqual(elems, [1, 2, 3, 4])

    def test_out_of_bounds(self):
        elems = []
        with self.assertRaises(IndexError):
            partition(elems, 1, 4, 0)

    def test_simple(self):
        elems = [3, 2, 1, 1]
        self.assertEqual(partition(elems, 0, 4, 2), 3)
        self.assertEqual(elems, [1, 1, 2, 3])


class TestMerge(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(merge([], []), [])
        self.assertEqual(merge([1], []), [1])
        self.assertEqual(merge([], [1]), [1])

    def test_simple(self):
        self.assertEqual(merge([1, 3, 5, 7], [2]), [1, 2, 3, 5, 7])


class TestCopy(unittest.TestCase):
    def test_empty(self):
        elems = []
        copy([], elems, 0)
        self.assertEqual(elems, [])

    def test_out_of_bounds(self):
        elems = []
        with self.assertRaises(IndexError):
            copy([1, 2], elems, 0)

    def test_simple(self):
        elems = [1, 2, 3, 4, 5]
        copy([10, 11, 12], elems, 1)
        self.assertEqual(elems, [1, 10, 11, 12, 5])
