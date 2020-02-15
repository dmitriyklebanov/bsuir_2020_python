from .utils import partition, merge, copy

from random import randrange


def merge_sort(elems):
    '''Sort elements inplace.
    '''

    block_size = 1
    while block_size < len(elems):
        block_start = 0
        while block_start < len(elems) - block_size:
            left = block_start
            right = block_start + block_size
            left_block = elems[left:right]

            left += block_size
            right += block_size
            right = min(right, len(elems))
            right_block = elems[left:right]

            copy(merge(left_block, right_block), elems, block_start)
            block_start += block_size * 2
        block_size *= 2


def quick_sort(elems, left, right):
    """Sort elements inplace in range [left, right).
    """

    if left + 1 < right:
        part_elem = elems[randrange(left, right)]
        partition_index = partition(elems, left, right, part_elem)
        quick_sort(elems, left, partition_index - 1)
        quick_sort(elems, partition_index, right)
