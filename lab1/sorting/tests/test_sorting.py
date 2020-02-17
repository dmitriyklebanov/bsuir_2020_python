from ..sorting import merge_sort, quick_sort


class TestMergeSort:
    def test_empty(self):
        elems = []
        merge_sort(elems)
        assert elems == []

    def test_equals(self):
        elems = [1] * 5
        merge_sort(elems)
        assert elems == [1] * 5

    def test_simple(self):
        elems = [1, 5, 4, 2, 0, 3]
        merge_sort(elems)
        assert elems == [0, 1, 2, 3, 4, 5]


class TestQuickSort:
    def test_empty(self):
        elems = []
        quick_sort(elems, 0, len(elems))
        assert elems == []

    def test_equals(self):
        elems = [1] * 5
        quick_sort(elems, 0, len(elems))
        assert elems == [1] * 5

    def test_simple(self):
        elems = [1, 5, 4, 2, 0, 3]
        quick_sort(elems, 0, len(elems))
        assert elems == [0, 1, 2, 3, 4, 5]
