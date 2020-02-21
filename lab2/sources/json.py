from math import isnan, isinf


class Serializer:
    '''Class with implemented serialization functions for basic types.
    '''

    __spec_chars = {
        '"': '\\"',
        '\\': '\\\\',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t'
    }

    def serialize_dict(obj):
        '''Return serialized dict to json.
        '''

        res = '{'
        for k, v in obj.items():
            res += Serializer.serialize_str(k) + ': '
            res += Serializer.serialize(v) + ', '
        if len(res) > 1:
            res = res[:-2]
        return res + '}'

    def serialize_iterable(iterable):
        '''Return serialized as list iterable to json.
        '''

        res = '['
        for item in iterable:
            res += Serializer.serialize(item) + ', '
        if len(res) > 1:
            res = res[:-2]
        return res + ']'

    def serialize_str(obj):
        '''Return serialized str to json.
        '''

        cur_s = str(obj)
        res = '"'
        for char in cur_s:
            if char in Serializer.__spec_chars:
                res += Serializer.__spec_chars[char]
            else:
                res += char
        res += '"'
        return res

    def serialize_number(obj):
        '''Return serialized int or float number to json.

        Raises ValueError if number is nan or inf.
        '''

        if isnan(obj) or isinf(obj):
            raise ValueError('nan and inf not specified in json')
        return str(obj)

    def serialize_bool(obj):
        '''Return serialized boolean to json.
        '''
        serialized_bool = {
            True: 'true',
            False: 'false'
        }
        return serialized_bool[obj]

    def serialize_none_type(obj):
        '''Return serialized None to json.
        '''
        return 'null'

    def serialize(obj):
        '''Return serialized object to json.

        Supports default types.
        '''
        if type(obj) in Serializer.__serializable_objects:
            return Serializer.__serializable_objects[type(obj)](obj)
        else:
            raise TypeError('can\'t serialize')

    __serializable_objects = {
        dict: serialize_dict,
        list: serialize_iterable,
        tuple: serialize_iterable,
        str: serialize_str,
        float: serialize_number,
        int: serialize_number,
        bool: serialize_bool,
        type(None): serialize_none_type
    }


class Deserializer:
    '''Class with implemented deserialization functions for basic types.
    '''

    __spec_chars = {
        '"': '"',
        '\\': '\\',
        'b': '\b',
        'f': '\f',
        'n': '\n',
        'r': '\r',
        't': '\t'
    }

    def remove_whitespaces(string, pos):
        '''Return position of first not whitespace character.
        '''

        while pos < len(string) and string[pos] == ' ':
            pos += 1
        return pos

    def __validate_length(string, pos):
        if pos == len(string):
            raise SyntaxError('end of parsing string')

    def __validate_char_in_string(string, pos, char):
        pos = Deserializer.remove_whitespaces(string, pos)
        Deserializer.__validate_length(string, pos)
        if string[pos] != char:
            raise SyntaxError(f'expected "{char}", but found {string[pos]}')
        return pos + 1

    def deserialize_dict(string, pos=0):
        '''Return deserialized dict from json.
        Also return position in string after the last character of the deserialized object.
        '''

        pos = Deserializer.remove_whitespaces(string, pos)
        pos = Deserializer.__validate_char_in_string(string, pos, '{')
        pos = Deserializer.remove_whitespaces(string, pos)
        res = {}
        while pos < len(string) and string[pos] != '}':
            if res:
                pos = Deserializer.__validate_char_in_string(string, pos, ',')

            key, pos = Deserializer.deserialize_str(string, pos)
            pos = Deserializer.__validate_char_in_string(string, pos, ':')
            value, pos = Deserializer.deserialize(string, pos)
            res[key] = value

            pos = Deserializer.remove_whitespaces(string, pos)

        pos = Deserializer.__validate_char_in_string(string, pos, '}')
        return res, pos

    def deserialize_iterable(string, pos=0):
        '''Return deserialized as list iterable from json.
        Also return position in string after the last character of the deserialized object.
        '''

        pos = Deserializer.remove_whitespaces(string, pos)
        pos = Deserializer.__validate_char_in_string(string, pos, '[')
        pos = Deserializer.remove_whitespaces(string, pos)
        res = []
        while pos < len(string) and string[pos] != ']':
            if res:
                pos = Deserializer.__validate_char_in_string(string, pos, ',')
            value, pos = Deserializer.deserialize(string, pos)
            res.append(value)
            pos = Deserializer.remove_whitespaces(string, pos)

        pos = Deserializer.__validate_char_in_string(string, pos, ']')
        return res, pos

    def deserialize_str(string, pos=0):
        '''Return deserialized str from json.
        Also return position in string after the last character of the deserialized object.
        '''

        pos = Deserializer.remove_whitespaces(string, pos)
        pos = Deserializer.__validate_char_in_string(string, pos, '"')
        res = ''
        while pos < len(string) and string[pos] != '"':
            if string[pos] == '\\':
                pos += 1
                Deserializer.__validate_length(string, pos)
                if string[pos] not in Deserializer.__spec_chars:
                    raise SyntaxError(f'undefined special character: {string[pos - 1:pos + 1]}')
                res += Deserializer.__spec_chars[string[pos]]
            else:
                res += string[pos]
            pos += 1

        pos = Deserializer.__validate_char_in_string(string, pos, '"')
        return res, pos

    def __deserialize_primitive(string, pos, marker_kv):
        pos = Deserializer.remove_whitespaces(string, pos)
        start = pos
        while pos < len(string) and string[pos] in marker_kv:
            pos += 1
        return string[start:pos], pos

    def deserialize_number(string, pos=0):
        '''Return deserialized float number from json.
        Also return position in string after the last character of the deserialized object.
        '''
        cur_string, pos = Deserializer.__deserialize_primitive(string, pos, '-+.0123456789eE')
        return float(cur_string), pos

    def deserialize_bool(string, pos=0):
        '''Return deserialized boolean from json.
        Also return position in string after the last character of the deserialized object.
        '''
        cur_string, pos = Deserializer.__deserialize_primitive(string, pos, 'truefalse')

        if cur_string == 'true':
            return True, pos
        elif cur_string == 'false':
            return False, pos
        else:
            raise SyntaxError(f'expected true/false, but found {cur_string}')

    def deserialize_none_type(string, pos=0):
        '''Return deserialized None from json.
        Also return position in string after the last character of the deserialized object.
        '''
        cur_string, pos = Deserializer.__deserialize_primitive(string, pos, 'null')
        if cur_string != 'null':
            raise SyntaxError(f'expected null, but found {cur_string}')
        return None, pos

    def deserialize(string, pos=0):
        '''Return deserialized object to json.
        Also return position in string after the last character of the deserialized object.

        Supports default types.
        '''
        pos = Deserializer.remove_whitespaces(string, pos)
        Deserializer.__validate_length(string, pos)
        for marker, func in Deserializer.__objects_markers.items():
            if string[pos] in marker:
                return func(string, pos)
        raise SyntaxError(f'can\'t deserialize, first characters: {string[pos:pos + 10]}')

    __objects_markers = {
        '{': deserialize_dict,
        '[': deserialize_iterable,
        '"': deserialize_str,
        '+-.0123456789eE': deserialize_number,
        'tf': deserialize_bool,
        'n': deserialize_none_type
    }
