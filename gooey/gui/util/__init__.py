from inspect import signature
from functools import partial, reduce
from itertools import zip_longest


def bootlegCurry(f):
    def _curry(f, remaining):
        def inner(*args):
            if len(args) >= remaining:
                return f(*args)
            else:
                newfunc = lambda *rem: f(*args, *rem)
                return _curry(newfunc, remaining - len(args))
        return inner
    return _curry(f, len(signature(f).parameters))


def isRequired(widget):
    return widget['required']


def isOptional(widget):
    return not isRequired(widget)


def isRequiredPositional(widget):
    return isRequired(widget) and widget['data']['commands']


def isRequiredNonPositional(widget):
    return isRequired(widget) and not widget['data']['commands']


@bootlegCurry
def belongsTo(parent, widget):
    return widget['parent'] == parent


def forEvent(target):
    return lambda action: action['type'] == target


def flatten(lists):
    for item in lists:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def compose(f, g):
    def inner(*args, **kwargs):
        return g(f(*args, **kwargs))
    return inner


def chunk(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


@bootlegCurry
def nestedget(path, obj):
    return reduce(lambda acc, val: acc.get(val, {}), path, obj)
