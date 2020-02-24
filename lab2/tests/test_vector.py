from lab2.sources.vector import Vector

import pytest


class TestVector:
    def test_init(self):
        a = Vector(())
        b = Vector((1,))
        c = Vector(None)
        with pytest.raises(TypeError):
            d = Vector(('1'))

    def test_len(self):
        assert len(Vector([1, 2, 3])) == 3
        assert len(Vector([1, 2])) == 2
        assert len(Vector([1, ])) == 1
        assert len(Vector([])) == 0

    def test_bool(self):
        assert bool(Vector([])) == True
        assert bool(Vector([0, 0])) == True
        assert bool(Vector([1, ])) == False
        assert bool(Vector([2, -2])) == False

    def test_str(self):
        assert str(Vector(())) == '()'
        assert str(Vector((1,))) == '(1)'
        assert str(Vector((1, 2))) == '(1, 2)'

    def test_get_and_set_items(self):
        a = Vector((1, 2))
        assert a[0] == 1 and a[1] == 2
        a[0] = 4
        assert a[0] == 4 and a[1] == 2
        with pytest.raises(TypeError):
            a[0] = 's'

    def test_length(self):
        assert Vector((3, 4)).length == 5
        assert Vector((5, 12)).length == 13
        assert Vector((8, 15)).length == 17

    def test_eq(self):
        assert (Vector((1, 2)) != Vector((3, 4))) == True
        assert (Vector((1, 2)) == Vector((1, 2))) == True
        assert (Vector((1, 2)) != 1) == True

    def test_add(self):
        assert Vector((1, 2)) + Vector((3, 4)) == Vector((4, 6))
        assert Vector((-1, 2)) + Vector((2, -1)) == Vector((1, 1))

        with pytest.raises(TypeError):
            Vector((1, 2)) + 3

        with pytest.raises(ValueError):
            a = Vector((1, 2)) + Vector((3, 4, 5))

    def test_sub(self):
        assert Vector((1, 2)) - Vector((3, 4)) == Vector((-2, -2))
        assert Vector((-1, 2)) - Vector((2, -1)) == Vector((-3, 3))

    def test_mul(self):
        assert Vector((1, -2)) * 3 == Vector((3, -6))
        assert 3 * Vector((1, -2)) == Vector((3, -6))
        assert Vector((1, 2)) @ Vector((3, 4)) == 11
        with pytest.raises(TypeError):
            Vector((1, 2)) * Vector((1, 2))

        with pytest.raises(ArithmeticError):
            a = Vector((1, 2))
            b = Vector((3, 4))
            a @= b

    def test_div(self):
        assert Vector((3, -6)) / 3 == Vector((1, -2))
        assert Vector((4, -7)) // 3 == Vector((1, -3))
