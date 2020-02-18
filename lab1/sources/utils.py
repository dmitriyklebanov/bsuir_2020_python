def find_id(elems, left, right, condition):
    '''Return first position where 'condition' is True.

    Find element id in range [left, right). If it is not found
    then return 'right'.
    '''

    for i in range(left, right):
        if condition(elems[i]):
            return i
    return right


def partition(elems, left, right, part_elem):
    '''Return position from which all elements more than part_elem.

    Partition elements in range [left, right). If part_elem is in elems
    then puts it to the left of returned position.
    '''

    first = find_id(elems, left, right, lambda x: x > part_elem)

    for i in range(first + 1, right):
        if elems[i] <= part_elem:
            elems[first], elems[i] = elems[i], elems[first]
            first += 1

    if first != left:
        for i in range(left, first):
            if part_elem == elems[i]:
                elems[first - 1], elems[i] = elems[i], elems[first - 1]
                break
    return first


def merge(elems1, elems2):
    '''Merge elements from sorted 'elems1' and 'elems2'.
    '''

    res = []
    pos1 = pos2 = 0
    while pos1 != len(elems1) and pos2 != len(elems2):
        if elems1[pos1] <= elems2[pos2]:
            res.append(elems1[pos1])
            pos1 += 1
        else:
            res.append(elems2[pos2])
            pos2 += 1

    while pos1 != len(elems1):
        res.append(elems1[pos1])
        pos1 += 1

    while pos2 != len(elems2):
        res.append(elems2[pos2])
        pos2 += 1

    return res


def copy(elems, dst, pos):
    '''Copy elements to 'dst' from 'pos'.
    '''

    for item in elems:
        dst[pos] = item
        pos += 1
