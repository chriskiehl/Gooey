from textwrap import dedent

from pyrsistent import m, pmap, v
import re


def validate_and_raise(validators, some_map):
    err, success = validate(validators, some_map)
    if err:
        raise ValueError(err)
    return success

def validate(validators, some_map):
    failures = {}
    for k, v in some_map.items():
        validator = validators.get(k, _unit)
        err, success = validator(v)
        if err:
            failures[k] = err

    if failures:
        return [[failures], None]
    return [None, some_map]

def _unit(value):
    return [None, value]

def is_tuple_or_list(value):
    return isinstance(value, list) or isinstance(value, tuple)

def is_str(value):
    return isinstance(value, str)


def validate_str_or_coll(value):
    error_msg = dedent('''
    Colors must be either a hex string or collection of RGB values. 
    e.g. 
        Hex string: #fff0ce 
        RGB Collection: [0, 255, 128] or (0, 255, 128) 
    ''')
    return ([None, value]
            if is_str(value) or is_tuple_or_list(value)
            else [[error_msg], None])

def validate_color(value):
    def _validate(value):
        if isinstance(value, str):
            return isfoo(value)
        else:
            return validate_rgb(value)
    return _flatmap(_validate, validate_str_or_coll(value))

def validate_rgb_vals(rgb_coll):
    failures = []
    for val, channel in zip(rgb_coll, 'RGB'):
        err, success = is_uint8(val)
        if err:
            failures += ['{} value: {}'.format(channel, msg) for msg in err]
    return [failures, None] if failures else [None, rgb_coll]

def is_uint8(value):
    return _flatmap(is0to255, isInt(value))

def validate_rgb(value):
    return _flatmap(validate_rgb_vals, three_channels(value))


def three_channels(value):
    return ([None, value]
            if len(value) == 3
            else [['Colors in an RGB collection should be of the form [R,G,B] or (R,G,B)'], None])

def isfoo(value: str):
    return ([None, value]
        if re.match('^#[\dABCDEF]{6}$', value, flags=2)
        else [['Invalid hexadecimal format. Expected: "#FFFFFF"'], None])

def is0to255(value: int):
    return ([None, value]
            if 0 <= value <= 255
            else [['Colors myst be 0-255'], None])

def isInt(value):
    return ([None, value]
            if isinstance(value, int)
            else [['Invalid RGB value. Expected type int'], None])


def _or(f, g):
    def inner(value):
        err1, val1 = f(value)
        err2, val2 = g(value)
        if val1 and val2:
            return [None, val1]
        elif err1 and err2:
            return [err1 + err2, None]
        elif err1:
            return [err1, None]
        else:
            return err2
    return inner


def _and(f, g):
    def inner(value):
        return _flatmap(f, g(value))
    return inner

def _flatmap(f, v):
    err, value = v
    if err:
        return v
    else:
        return f(value)

if __name__ == '__main__':
    print(validate_color((1,'ergerg',1234)))
    print(validate_color(1234))
    print(validate_color(123.234))
    print(validate_color('123.234'))
    print(validate_color('FFFAAA'))
    print(validate_color('#FFFAAA'))
    print(validate_color([]))
    print(validate_color(()))
    print(validate_color((1,2)))
    print(validate_color((1, 2, 1234)))
