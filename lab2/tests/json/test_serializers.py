from sources.json.serializers import serialize_dict, serialize_iterable
from sources.json.serializers import serialize_str, serialize_number
from sources.json.serializers import serialize_bool, serialize_none_type
from sources.json.serializers import serialize_to_json

import pytest


class TestSerializeDict:
    def test_empty(self):
        assert serialize_dict({}) == '{}'

    def test_one(self):
        assert serialize_dict({"1": 2}) == '{"1": 2}'

    def test_mixed(self):
        res = serialize_dict({1: 2, 3: None, '4': r'\n', 'test': [1, None, True]})
        ans = r'{"1": 2, "3": null, "4": "\\n", "test": [1, null, true]}'
        print(res, ans)
        assert res == ans


class TestSerializeIterable:
    def test_empty(self):
        assert serialize_iterable([]) == '[]'

    def test_one(self):
        assert serialize_iterable([1]) == '[1]'

    def test_tuple(self):
        assert serialize_iterable((1, 2, 3)) == '[1, 2, 3]'

    def test_different_types(self):
        res = serialize_iterable([1, None, False, [1, 2], {1: 2, 3: 4}])
        ans = '[1, null, false, [1, 2], {"1": 2, "3": 4}]'
        assert res == ans


class TestSerializeStr:
    def test_empty(self):
        assert serialize_str('') == '""'

    def test_spec_chars(self):
        assert serialize_str('\n\r\b\f\t\\') == r'"\n\r\b\f\t\\"'

    def test_mixed(self):
        assert serialize_str('abc\ndef\tghi') == r'"abc\ndef\tghi"'


class TestSerializeNumber:
    def test_nan(self):
        with pytest.raises(ValueError):
            serialize_number(float('nan'))

    def test_inf(self):
        with pytest.raises(ValueError):
            serialize_number(float('inf'))

    @pytest.mark.parametrize('number', [0, 0.0, 42, 3.14])
    def test_simple(self, number):
        assert serialize_number(number) == str(number)


class TestSerializeBool:
    def test_bool(self):
        assert serialize_bool(True) == 'true'
        assert serialize_bool(False) == 'false'


class TestSerializeNoneType:
    def test_none(self):
        assert serialize_none_type(None) == 'null'

class TestSerializeToJson:
    def test_different_types(self):
        assert serialize_to_json(0) == '0'
        assert serialize_to_json(0.0) == '0.0'
        assert serialize_to_json(False) == 'false'
        assert serialize_to_json(None) == 'null'
        assert serialize_to_json('str') == '"str"'
        assert serialize_to_json([1, 2]) == '[1, 2]'
        assert serialize_to_json({1: '2'}) == '{"1": "2"}'

    def test_mixed(self):
        res = serialize_to_json([1, False, None, {0.3: 'kokoko', 'test': [4, {1: 2}]}])
        ans = '[1, false, null, {"0.3": "kokoko", "test": [4, {"1": 2}]}]'
        assert ans == res

    def test_undefined_type(self):
        class SomeType:
            def f(self):
                print('SomeType.f()')

        with pytest.raises(TypeError):
            serialize_to_json(SomeType())
