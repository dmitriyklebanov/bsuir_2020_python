from bsuir_2020_python.lab2.sources.external_algorithms import NumbersReader, NumbersWriter
from bsuir_2020_python.lab2.sources.external_algorithms import external_merge, external_sort

from tempfile import TemporaryDirectory

import os
import pytest
import random


@pytest.fixture
def tmpdirname():
    tmpdir = TemporaryDirectory()
    yield tmpdir.name
    tmpdir.cleanup()


class TestingUtils:
    def generate_numbers_in_file(filename, n, max_val, sort=True):
        res = [random.randint(-max_val, max_val) for _ in range(n)]
        if sort:
            res.sort()
        with open(filename, 'w') as f:
            f.write(' '.join(map(str, res)))
        return res

    def load_result_from_file(filepath):
        with open(filepath, 'r') as f:
            return list(map(int, f.read().split()))


class TestNumbersReader:
    def initialize(self, tmpdirname):
        random.seed(42)
        return os.path.join(tmpdirname, 'file.txt')

    @pytest.mark.parametrize("num_count", [0, 1, 2, 100])
    def test_single_number_reading(self, tmpdirname, num_count):
        filepath = self.initialize(tmpdirname)
        lst = TestingUtils.generate_numbers_in_file(filepath, num_count, 10)
        with NumbersReader(filepath) as nr:
            for item in lst:
                assert nr.read_number() == item
            assert nr.read_number() is None

    @pytest.mark.parametrize("num_count, block_size", [
        (0, 1),
        (1, 1),
        (1, 10000),
        (1000, 10)])
    def test_block_reading(self, tmpdirname, num_count, block_size):
        filepath = self.initialize(tmpdirname)
        lst = TestingUtils.generate_numbers_in_file(filepath, num_count, 10)
        with NumbersReader(filepath) as nr:
            i = 0
            while i < len(lst):
                assert nr.read_block(block_size) == lst[i:i + block_size]
                i += block_size
            assert nr.read_block(block_size) == []


class TestNumbersWriter:
    def initialize(self, tmpdirname):
        random.seed(42)
        return os.path.join(tmpdirname, 'file.txt')

    @pytest.mark.parametrize("num_count", [0, 1, 2, 100])
    def test_single_number_writing(self, tmpdirname, num_count):
        filepath = self.initialize(tmpdirname)
        lst = [random.randint(-100, 100) for _ in range(num_count)]
        with NumbersWriter(filepath) as nr:
            for item in lst:
                nr.write_number(item)
        with open(filepath, 'r') as f:
            assert list(map(int, f.read().split())) == lst

    @pytest.mark.parametrize("num_count, block_size", [
        (0, 1),
        (1, 1),
        (1, 10000),
        (1000, 10)])
    def test_block_writing(self, tmpdirname, num_count, block_size):
        filepath = self.initialize(tmpdirname)
        lst = [random.randint(-100, 100) for _ in range(num_count)]
        with NumbersWriter(filepath) as nr:
            i = 0
            while i < len(lst):
                nr.write_block(lst[i:i + block_size])
                i += block_size
        with open(filepath, 'r') as f:
            assert list(map(int, f.read().split())) == lst


class TestExternalMerge:
    def initialize(self, tmpdirname):
        random.seed(42)
        filepath1 = os.path.join(tmpdirname, 'file1.txt')
        filepath2 = os.path.join(tmpdirname, 'file2.txt')
        dst_filepath = os.path.join(tmpdirname, 'dst.txt')
        return filepath1, filepath2, dst_filepath

    @pytest.mark.parametrize("num_count1, num_count2", [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (100, 100),
        (1000, 1000)])
    def test_simple_merge(self, tmpdirname, num_count1, num_count2):
        filepath1, filepath2, dst_filepath = self.initialize(tmpdirname)
        lst1 = TestingUtils.generate_numbers_in_file(filepath1, num_count1, 10)
        lst2 = TestingUtils.generate_numbers_in_file(filepath2, num_count2, 10)
        external_merge(filepath1, filepath2, dst_filepath)
        merge_res = TestingUtils.load_result_from_file(dst_filepath)
        assert sorted(lst1 + lst2) == merge_res


class TestExternalSort:
    def initialize(self, tmpdirname):
        random.seed(42)
        input_filepath = os.path.join(tmpdirname, 'input.txt')
        output_filepath = os.path.join(tmpdirname, 'output.txt')
        return input_filepath, output_filepath

    @pytest.mark.parametrize("num_count, block_size", [
        (0, 1),
        (1, 1),
        (10, 1),
        (100, 2),
        (1000, 3)])
    def test_simple_sort(self, tmpdirname, num_count, block_size):
        input_filepath, output_filepath = self.initialize(tmpdirname)
        lst = TestingUtils.generate_numbers_in_file(input_filepath, num_count, 100, sort=False)
        external_sort(input_filepath, output_filepath, block_size)
        sort_res = TestingUtils.load_result_from_file(output_filepath)
        assert sorted(lst) == sort_res
