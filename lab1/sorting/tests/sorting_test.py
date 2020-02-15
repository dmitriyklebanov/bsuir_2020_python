from ..sorting import merge_sort, quick_sort

import unittest


class TestMergeSort(unittest.TestCase):
    def test_empty(self):
        elems = []
        merge_sort(elems)
        self.assertEqual(elems, [])

    def test_equals(self):
        elems = [1] * 5
        merge_sort(elems)
        self.assertEqual(elems, [1] * 5)

    def test_simple(self):
        elems = [1, 5, 4, 2, 0, 3]
        merge_sort(elems)
        self.assertEqual(elems, [0, 1, 2, 3, 4, 5])


class TestQuickSort(unittest.TestCase):
    def test_empty(self):
        elems = []
        quick_sort(elems, 0, len(elems))
        self.assertEqual(elems, [])

    def test_equals(self):
        elems = [1] * 5
        quick_sort(elems, 0, len(elems))
        self.assertEqual(elems, [1] * 5)

    def test_simple(self):
        elems = [1, 5, 4, 2, 0, 3]
        quick_sort(elems, 0, len(elems))
        self.assertEqual(elems, [0, 1, 2, 3, 4, 5])
