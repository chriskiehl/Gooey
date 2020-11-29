import re
from functools import wraps

from gooey.gui.components.filtering.prefix_filter import OperatorType


class SuperBool(object):
    """
    A boolean which keeps with it the rationale
    for when it is false.
    """
    def __init__(self, value, rationale):
        self.value = value
        self.rationale = rationale

    def __bool__(self):
        return self.value

    __nonzero__ = __bool__

    def __str__(self):
        return str(self.value)


def lift(f):
    """
    Lifts a basic predicate to the SuperBool type
    stealing the docstring as the rationale message.

    This is largely just goofing around and experimenting
    since it's a private internal API.
    """
    @wraps(f)
    def inner(value):
        result = f(value)
        return SuperBool(result, f.__doc__) if not isinstance(result, SuperBool) else result
    return inner


@lift
def is_tuple_or_list(value):
    """Must be either a list or tuple"""
    return isinstance(value, list) or isinstance(value, tuple)


@lift
def is_str(value):
    """Must be of type `str`"""
    return isinstance(value, str)

@lift
def is_str_or_coll(value):
    """
    Colors must be either a hex string or collection of RGB values.
    e.g.
        Hex string: #fff0ce
        RGB Collection: [0, 255, 128] or (0, 255, 128)
    """
    return bool(is_str(value)) or bool(is_tuple_or_list(value))


@lift
def has_valid_channel_values(rgb_coll):
    """Colors in an RGB collection must all be in the range 0-255"""
    return all([is_0to255(c) and is_int(c) for c in rgb_coll])


@lift
def is_three_channeled(value):
    """Missing channels! Colors in an RGB collection should be of the form [R,G,B] or (R,G,B)"""
    return len(value) == 3

@lift
def is_hex_string(value: str):
    """Invalid hexadecimal format. Expected: "#FFFFFF" """
    return isinstance(value, str) and bool(re.match('^#[\dABCDEF]{6}$', value, flags=2))


@lift
def is_bool(value):
    """Must be of type Boolean"""
    return isinstance(value, bool)

@lift
def non_empty_string(value):
    """Must be a non-empty non-blank string"""
    return value and bool(value.strip())

@lift
def is_tokenization_operator(value):
    """Operator must be a valid OperatorType i.e. one of: (AND, OR)"""
    return value in (OperatorType.AND, OperatorType.OR)

@lift
def is_tokenizer(value):
    """Tokenizers must be valid Regular expressions. see: options.PrefixTokenizers"""
    return bool(non_empty_string(value))


@lift
def is_int(value):
    """Invalid type. Expected `int`"""
    return isinstance(value, int)

@lift
def is_0to255(value):
    """RGB values must be in the range 0 - 255 (inclusive)"""
    return 0 <= value <= 255


def is_0to20(value):
    """Precision values must be in the range 0 - 20 (inclusive)"""
    return 0 <= value <= 20

@lift
def is_valid_color(value):
    """Must be either a valid hex string or RGB list"""
    if is_str(value):
        return is_hex_string(value)
    elif is_tuple_or_list(value):
        return (is_tuple_or_list(value)
                and is_three_channeled(value)
                and has_valid_channel_values(value))
    else:
        return is_str_or_coll(value)


validators = {
    'label_color': is_valid_color,
    'label_bg_color': is_valid_color,
    'help_color': is_valid_color,
    'help_bg_color': is_valid_color,
    'error_color': is_valid_color,
    'error_bg_color': is_valid_color,
    'show_label': is_bool,
    'show_help': is_bool,
    'visible': is_bool,
    'full_width': is_bool,
    'height': is_int,
    'readonly': is_bool,
    'initial_selection': is_int,
    'title': non_empty_string,
    'checkbox_label': non_empty_string,
    'placeholder': non_empty_string,
    'empty_message': non_empty_string,
    'max_size': is_int,
    'choice_tokenizer': is_tokenizer,
    'input_tokenizer': is_tokenizer,
    'ignore_case': is_bool,
    'operator': is_tokenization_operator,
    'index_suffix': is_bool,
    'wildcard': non_empty_string,
    'default_dir': non_empty_string,
    'default_file': non_empty_string,
    'default_path': non_empty_string,
    'message': non_empty_string,
    'precision': is_0to20
}



def collect_errors(predicates, m):
    return {
        k:predicates[k](v).rationale
        for k,v in m.items()
        if k in predicates and not predicates[k](v)}


def validate(pred, value):
    result = pred(value)
    if not result:
        raise ValueError(result.rationale)



if __name__ == '__main__':
    # TODO: there should be tests
    pass
    # print(validateColor((1, 'ergerg', 1234)))
    # print(validateColor(1234))
    # print(validateColor(123.234))
    # print(validateColor('123.234'))
    # print(validateColor('FFFAAA'))
    # print(validateColor('#FFFAAA'))
    # print(validateColor([]))
    # print(validateColor(()))
    # print(validateColor((1, 2)))
    # print(validateColor((1, 2, 1234)))
    # print(is_lifted(lift(is_int)))
    # print(is_lifted(is_int))
    # print(OR(is_poop, is_int)('poop'))
    # print(AND(is_poop, is_lower, is_lower)('pooP'))
    # print(OR(is_poop, is_int))
    # print(is_lifted(OR(is_poop, is_int)))
    # print(validate(is_valid_color, [255, 255, 256]))
    # print(is_valid_color('#fff000'))
    # print(is_valid_color([255, 244, 256]))
    # print(non_empty_string('asdf') and non_empty_string('asdf'))
    # validate(is_valid_color, 1234)


