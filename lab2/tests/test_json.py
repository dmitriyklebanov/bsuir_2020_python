from bsuir_2020_python.lab2.sources.json import Serializer, Deserializer

import pytest


class TestSerializer:
    class TestSerializeDict:
        def test_empty(self):
            assert Serializer.serialize_dict({}) == '{}'

        def test_one(self):
            assert Serializer.serialize_dict({"1": 2}) == '{"1": 2}'

        def test_mixed(self):
            res = Serializer.serialize_dict({1: 2, 3: None, '4': r'\n', 'test': [1, None, True]})
            ans = r'{"1": 2, "3": null, "4": "\\n", "test": [1, null, true]}'
            assert res == ans

    class TestSerializeIterable:
        def test_empty(self):
            assert Serializer.serialize_iterable([]) == '[]'

        def test_one(self):
            assert Serializer.serialize_iterable([1]) == '[1]'

        def test_tuple(self):
            assert Serializer.serialize_iterable((1, 2, 3)) == '[1, 2, 3]'

        def test_different_types(self):
            res = Serializer.serialize_iterable([1, None, False, [1, 2], {1: 2, 3: 4}])
            ans = '[1, null, false, [1, 2], {"1": 2, "3": 4}]'
            assert res == ans

    class TestSerializeStr:
        def test_empty(self):
            assert Serializer.serialize_str('') == '""'

        def test_spec_chars(self):
            assert Serializer.serialize_str('\n\r\b\f\t\\') == r'"\n\r\b\f\t\\"'

        def test_mixed(self):
            assert Serializer.serialize_str('abc\ndef\tghi') == r'"abc\ndef\tghi"'

    class TestSerializeNumber:
        def test_nan(self):
            with pytest.raises(ValueError):
                Serializer.serialize_number(float('nan'))

        def test_inf(self):
            with pytest.raises(ValueError):
                Serializer.serialize_number(float('inf'))

        @pytest.mark.parametrize('number', [0, 0.0, 42, 3.14])
        def test_simple(self, number):
            assert Serializer.serialize_number(number) == str(number)

    class TestSerializeBool:
        def test_bool(self):
            assert Serializer.serialize_bool(True) == 'true'
            assert Serializer.serialize_bool(False) == 'false'

    class TestSerializeNoneType:
        def test_none(self):
            assert Serializer.serialize_none_type(None) == 'null'

    class TestSerialize:
        def test_different_types(self):
            assert Serializer.serialize(0) == '0'
            assert Serializer.serialize(0.0) == '0.0'
            assert Serializer.serialize(False) == 'false'
            assert Serializer.serialize(None) == 'null'
            assert Serializer.serialize('str') == '"str"'
            assert Serializer.serialize([1, 2]) == '[1, 2]'
            assert Serializer.serialize({1: '2'}) == '{"1": "2"}'

        def test_mixed(self):
            res = Serializer.serialize([1, False, None, {0.3: 'kokoko', 'test': [4, {1: 2}]}])
            ans = '[1, false, null, {"0.3": "kokoko", "test": [4, {"1": 2}]}]'
            assert ans == res

        def test_undefined_type(self):
            class SomeType:
                def __init__(self):
                    self.__a = 42
                    self._b = 3.14
                    self.c = 'kokoko'

            res = Serializer.serialize(SomeType())
            ans = '{"_SomeType__a": 42, "_b": 3.14, "c": "kokoko"}'
            assert res == ans


class TestDeserializer:
    class TestDeserializeDict:
        def test_empty(self):
            assert Deserializer.deserialize_dict('{}')[0] == {}
            assert Deserializer.deserialize_dict('{  }')[0] == {}
            assert Deserializer.deserialize_dict('  { }  ')[0] == {}

        def test_one(self):
            assert Deserializer.deserialize_dict('{"1": 2}')[0] == {"1": 2}

        def test_broken(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize('{"1": 2; "3": 4}')

        def test_mixed(self):
            string = r'{  "1": 2,  "3": null, "4": "\\n", "test"  : [1, null,   true]   }'
            res = Deserializer.deserialize_dict(string)[0]
            ans = {'1': 2.0, '3': None, '4': r'\n', 'test': [1.0, None, True]}
            assert res == ans

    class TestDeserializeIterable:
        def test_empty(self):
            assert Deserializer.deserialize_iterable('[]')[0] == []
            assert Deserializer.deserialize_iterable(' [  ]  ')[0] == []
            assert Deserializer.deserialize_iterable(' [ ] ')[0] == []

        def test_one(self):
            assert Deserializer.deserialize_iterable('[1]')[0] == [1]

        def test_different_types(self):
            string = '[1, null, false, [1, 2], {"1": 2, "3": 4}]'
            res = Deserializer.deserialize_iterable(string)[0]
            ans = [1, None, False, [1, 2], {'1': 2, '3': 4}]
            assert res == ans

    class TestDeserializeStr:
        def test_empty(self):
            assert Deserializer.deserialize_str('""')[0] == ''

        def test_spec_chars(self):
            assert Deserializer.deserialize_str(r'"\n\r\b\f\t\\"')[0] == '\n\r\b\f\t\\'

        def test_undefined_spec_char(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_str(r'"\z"')

        def test_mixed(self):
            assert Deserializer.deserialize_str(r'"abc\ndef\tghi"')[0] == 'abc\ndef\tghi'

    class TestDeserializeNumber:
        @pytest.mark.parametrize('number', [0, 0.0, 42, 3.14, 3.14e21])
        def test_simple(self, number):
            assert Deserializer.deserialize_number(str(number))[0] == number

    class TestDeserializeBool:
        def test_bool(self):
            assert Deserializer.deserialize_bool('true')[0] == True
            assert Deserializer.deserialize_bool('false')[0] == False

        def test_wrong_bool(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_bool('truu')

            with pytest.raises(SyntaxError):
                Deserializer.deserialize_bool('falss')

    class TestDeserializeNoneType:
        def test_none(self):
            assert Deserializer.deserialize_none_type('null')[0] == None

        def test_exception(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_none_type('kokoko')

    class TestDeSerialize:
        def test_different_types(self):
            assert Deserializer.deserialize('0')[0] == 0
            assert Deserializer.deserialize('false')[0] == False
            assert Deserializer.deserialize('null')[0] == None
            assert Deserializer.deserialize('"str"')[0] == 'str'
            assert Deserializer.deserialize('[1, 2]')[0] == [1, 2]
            assert Deserializer.deserialize('{"1": "2"}')[0] == {"1": "2"}

        def test_mixed(self):
            string = '[1, false, null, {"0.3": "kokoko", "test": [4, {"1": 2}]}]'
            res = Deserializer.deserialize(string)[0]
            ans = [1, False, None, {'0.3': 'kokoko', 'test': [4, {'1': 2}]}]
            assert ans == res

        def test_empty(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize('')

        def test_undefined_type(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize('kokoko')

        def test_custom_type(self):
            class SomeType:
                def __init__(self):
                    self.__a = 0
                    self._b = 0
                    self.c = 0

                @property
                def get_a(self):
                    return self.__a

                @property
                def get_b(self):
                    return self._b

                @property
                def get_c(self):
                    return self.c

            string = '{"_SomeType__a": 42, "_b": 3.14, "c": "kokoko"}'
            obj = SomeType()
            res = Deserializer.deserialize(string, obj=obj)
            ans = {'_SomeType__a': 42, '_b': 3.14, 'c': 'kokoko'}
            assert res[0] == ans
            assert obj.get_a == 42
            assert obj.get_b == 3.14
            assert obj.get_c == 'kokoko'
