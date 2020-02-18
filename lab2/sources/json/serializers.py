from math import isnan, isinf


def serialize_dict(obj):
    '''Return serialized dict to json.
    '''

    res = '{'
    for k, v in obj.items():
        res += serialize_str(k) + ': '
        res += serialize_to_json(v) + ', '
    if len(res) > 1:
        res = res[:-2]
    return res + '}'


def serialize_iterable(iterable):
    '''Return serialized as list iterable to json.
    '''

    res = '['
    for item in iterable:
        res += serialize_to_json(item) + ', '
    if len(res) > 1:
        res = res[:-2]
    return res + ']'


spec_chars = {
    '"': '\\"',
    '\\': '\\\\',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t'
}


def serialize_str(obj):
    '''Return serialized str to json.
    '''

    cur_s = str(obj)
    res = '"'
    for char in cur_s:
        if char in spec_chars:
            res += spec_chars[char]
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


serializable_obj = {
    dict: serialize_dict,
    list: serialize_iterable,
    tuple: serialize_iterable,
    str: serialize_str,
    float: serialize_number,
    int: serialize_number,
    bool: serialize_bool,
    type(None): serialize_none_type
}


def serialize_to_json(obj):
    '''Return serialized object to json.

    Supports default types.
    '''
    if type(obj) in serializable_obj:
        return serializable_obj[type(obj)](obj)
    else:
        raise TypeError('can\'t serialize')
