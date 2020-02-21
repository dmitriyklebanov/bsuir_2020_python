from bsuir_2020_python.lab1.sources.utils import find_id, partition, merge, copy

import pytest


class TestFindId:
    def test_empty(self):
        elems = []
        assert find_id(elems, 0, 0, lambda x: False) == 0

    def test_invalid_bounds(self):
        elems = [1, 2, 3, 4]
        assert find_id(elems, 1, 0, lambda x: False) == 0

    def test_right_bound(self):
        elems = [1, 2, 3, 4]
        assert find_id(elems, 0, 4, lambda x: False) == 4

    def test_out_of_bounds(self):
        elems = []
        with pytest.raises(IndexError):
            find_id(elems, 1, 4, lambda x: False)


class TestPartition:
    def test_empty(self):
        elems = []
        assert partition(elems, 0, 0, 1) == 0
        assert elems == []

    def test_invalid_bounds(self):
        elems = [1, 2, 3, 4]
        assert partition(elems, 1, 0, 0) == 0
        assert elems == [1, 2, 3, 4]

    def test_right_bound(self):
        elems = [1, 2, 3, 4]
        assert partition(elems, 0, 4, 5) == 4
        assert elems == [1, 2, 3, 4]

    def test_out_of_bounds(self):
        elems = []
        with pytest.raises(IndexError):
            partition(elems, 1, 4, 0)

    def test_simple(self):
        elems = [3, 2, 1, 1]
        assert partition(elems, 0, 4, 2) == 3
        assert elems == [1, 1, 2, 3]


class TestMerge:
    def test_empty(self):
        assert merge([], []) == []
        assert merge([1], []) == [1]
        assert merge([], [1]) == [1]

    def test_simple(self):
        assert merge([1, 3, 5, 7], [2]) == [1, 2, 3, 5, 7]


class TestCopy:
    def test_empty(self):
        elems = []
        copy([], elems, 0)
        assert elems == []

    def test_out_of_bounds(self):
        elems = []
        with pytest.raises(IndexError):
            copy([1, 2], elems, 0)

    def test_simple(self):
        elems = [1, 2, 3, 4, 5]
        copy([10, 11, 12], elems, 1)
        assert elems == [1, 10, 11, 12, 5]
