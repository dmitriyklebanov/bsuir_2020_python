from lab2.sources.json import Serializer, Deserializer

import json
import pytest


class TestSerializer:
    class TestSerializeDict:
        @pytest.mark.parametrize('obj', [
            {},
            {'1': 2},
            {1: 2, 3: None, '4': r'\n', 'test': [1, None, True]},
        ])
        def test_universal(self, obj):
            assert Serializer.serialize_dict(obj) == json.dumps(obj)

    class TestSerializeIterable:
        @pytest.mark.parametrize('obj', [
            [],
            [1],
            (1, 2, 3),
            [1, None, False, [1, 2], {1: 2, 3: 4}],
        ])
        def test_universal(self, obj):
            assert Serializer.serialize_iterable(obj) == json.dumps(obj)

    class TestSerializeStr:
        @pytest.mark.parametrize('obj', [
            '',
            '\n\r\b\f\t\\',
            'abc\ndef\tghi',
        ])
        def test_universal(self, obj):
            assert Serializer.serialize_str(obj) == json.dumps(obj)

    class TestSerializeNumber:
        @pytest.mark.parametrize('obj', [0, 0.0, 42, 3.14])
        def test_universal(self, obj):
            assert Serializer.serialize_number(obj) == json.dumps(obj)

        def test_nan(self):
            with pytest.raises(ValueError):
                Serializer.serialize_number(float('nan'))

        def test_inf(self):
            with pytest.raises(ValueError):
                Serializer.serialize_number(float('inf'))

    class TestSerializeBool:
        @pytest.mark.parametrize('obj', [True, False])
        def test_universal(self, obj):
            assert Serializer.serialize_bool(obj) == json.dumps(obj)

    class TestSerializeNoneType:
        def test_none(self):
            assert Serializer.serialize_none_type(None) == 'null'

    class TestSerialize:
        @pytest.mark.parametrize('obj', [
            0,
            0.0,
            False,
            None,
            'str',
            [1, 2],
            {1: '2'},
            [1, False, None, {0.3: 'kokoko', 'test': [4, {1: 2}]}],
        ])
        def test_universal(self, obj):
            assert Serializer.serialize(obj) == json.dumps(obj)

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
        @pytest.mark.parametrize('string', [
            '{}',
            '{  }',
            '  {   } ',
            '{"1": 2}',
            r'{  "1": 2,  "3": null, "4": "\\n", "test"  :'
            r' [1, null,   true]   }',
        ])
        def test_universal(self, string):
            assert Deserializer.deserialize_dict(string)[0] == \
                json.loads(string)

        def test_broken(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize('{"1": 2; "3": 4}')

    class TestDeserializeIterable:
        @pytest.mark.parametrize('string', [
            '[]',
            '[  ]',
            '  [   ] ',
            '[1]',
            '[1, null, false, [1, 2], {"1": 2, "3": 4}]',
        ])
        def test_universal(self, string):
            assert Deserializer.deserialize_iterable(string)[0] == \
                json.loads(string)

    class TestDeserializeStr:
        @pytest.mark.parametrize('string', [
            '""',
            r'"\n\r\b\f\t\\"',
            r'"abc\ndef\tghi"',
        ])
        def test_universal(self, string):
            assert Deserializer.deserialize_str(string)[0] == \
                json.loads(string)

        def test_undefined_spec_char(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_str(r'"\z"')

    class TestDeserializeNumber:
        @pytest.mark.parametrize('number', [0, 0.0, 42, 3.14, 3.14e21])
        def test_simple(self, number):
            assert Deserializer.deserialize_number(str(number))[0] == number

    class TestDeserializeBool:
        @pytest.mark.parametrize('string', [
            'true',
            'false',
        ])
        def test_universal(self, string):
            assert Deserializer.deserialize_bool(string)[0] == \
                json.loads(string)

        def test_wrong_bool(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_bool('truu')

            with pytest.raises(SyntaxError):
                Deserializer.deserialize_bool('falss')

    class TestDeserializeNoneType:
        def test_none(self):
            string = 'null'
            assert Deserializer.deserialize_none_type(string)[0] == \
                json.loads(string)

        def test_exception(self):
            with pytest.raises(SyntaxError):
                Deserializer.deserialize_none_type('kokoko')

    class TestDeserialize:
        @pytest.mark.parametrize('string', [
            '0',
            'false',
            'null',
            '"str"',
            '[1, 2]',
            '{"1": "2"}',
            '[1, false, null, {"0.3": "kokoko", "test": [4, {"1": 2}]}]',
        ])
        def test_universal(self, string):
            assert Deserializer.deserialize(string)[0] == \
                json.loads(string)

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
