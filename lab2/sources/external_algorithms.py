from copy import deepcopy
from tempfile import TemporaryDirectory

import os
import shutil


class NumbersReader:
    '''Class for reading numbers from a file.
    '''

    DELIMETERS = ' \n'

    def __init__(self, filename, number_type=int):
        self.__file = open(filename, 'r')
        self.__number_type = number_type

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        '''Closes file.
        '''
        self.__file.close()

    def read_number(self):
        '''Return a number or None if EOF.
        '''

        buffer = ''
        char = self.__file.read(1)
        while char:
            if char in NumbersReader.DELIMETERS:
                if buffer:
                    return self.__number_type(buffer)
            else:
                buffer += char
            char = self.__file.read(1)

        buffer = buffer.strip()
        if buffer:
            return self.__number_type(buffer)
        else:
            return None

    def read_block(self, block_size):
        '''Return list of numbers. Returned list size is not more than block_size.
        '''

        block = []
        for _ in range(block_size):
            number = self.read_number()
            if number is not None:
                block.append(number)
            else:
                break
        return block


class NumbersWriter:
    '''Class for writing numbers in a file.
    '''

    def __init__(self, filename):
        self.__file = open(filename, 'w')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        '''Closes file.
        '''

        self.__file.close()

    def write_number(self, number):
        '''Write a numbers into a file.
        '''

        self.__file.write(f'{number} ')

    def write_block(self, block):
        '''Write a list of numbers into a file.
        '''

        for number in block:
            self.write_number(number)


def external_merge(filepath1, filepath2, dst_filepath):
    '''Merges sorted numbers from two files into one.
    '''

    with NumbersReader(filepath1) as nr1, \
            NumbersReader(filepath2) as nr2, \
            NumbersWriter(dst_filepath) as nw:
        number1 = nr1.read_number()
        number2 = nr2.read_number()
        while number1 is not None and number2 is not None:
            if number1 <= number2:
                nw.write_number(number1)
                number1 = nr1.read_number()
            else:
                nw.write_number(number2)
                number2 = nr2.read_number()

        while number1 is not None:
            nw.write_number(number1)
            number1 = nr1.read_number()

        while number2 is not None:
            nw.write_number(number2)
            number2 = nr2.read_number()


class external_sort:
    '''Sort the input file in external memory and print numbers into the output file.
    At any time of executing there is no more than "block_size" elements in the RAM memory.
    '''

    class __TmpFilePaths:
        '''Class for generating paths for temp files.

        Temp file path contains files iteration and file id.
        '''

        def __init__(self, tmpdir, iteration=0):
            self.__dirname = tmpdir.name
            self.iteration = iteration
            self.file_id = 0

        def get_path(self):
            '''Return new path to a file and increments their counter.
            '''

            name = f'{self.iteration}_{self.file_id}'
            path = os.path.join(self.__dirname, name)
            self.file_id += 1
            return path

        def drop_count(self):
            '''Return paths counter and nullify it.
            '''

            res = self.file_id
            self.file_id = 0
            return res

        def next_iteration(self):
            '''Increases iteration of temp files and nullify files counter.
            '''

            self.iteration += 1
            self.file_id = 0

    def __split_on_sorted_blocks(tmpdir, input_filename, block_size):
        '''Load numbers from input file, split them on blocks of "block_size" len,
        sort them, and print each block in a separate file in the "tmpdir".
        '''

        filepaths = external_sort.__TmpFilePaths(tmpdir)
        with NumbersReader(input_filename) as nr:
            block = nr.read_block(block_size)
            while block:
                block.sort()
                with NumbersWriter(filepaths.get_path()) as nw:
                    nw.write_block(block)
                block = nr.read_block(block_size)
        return filepaths

    def __new__(cls, input_filename, output_filename, block_size=2):
        tmpdir = TemporaryDirectory()
        filepaths = external_sort.__split_on_sorted_blocks(tmpdir, input_filename, block_size)
        while filepaths.file_id > 1:
            prev_filepaths = deepcopy(filepaths)
            prev_file_cnt = prev_filepaths.drop_count()
            filepaths.next_iteration()

            for _ in range(1, prev_file_cnt, 2):
                external_merge(
                    prev_filepaths.get_path(),
                    prev_filepaths.get_path(),
                    filepaths.get_path())

            if prev_file_cnt % 2 == 1:
                os.rename(prev_filepaths.get_path(), filepaths.get_path())

        if filepaths.file_id:
            filepaths.file_id -= 1
            shutil.copy(filepaths.get_path(), output_filename)
        else:
            shutil.copy(input_filename, output_filename)
        tmpdir.cleanup()
