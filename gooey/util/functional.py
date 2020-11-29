"""
A collection of functional utilities/helpers
"""
from functools import reduce
from copy import deepcopy
from itertools import chain, dropwhile


def getin(m, path, default=None):
    """returns the value in a nested dict"""
    keynotfound = ':com.gooey-project/not-found'
    result = reduce(lambda acc, val: acc.get(val, {keynotfound: None}), path, m)
    # falsey values like 0 would incorrectly trigger the default to be returned
    # so the keynotfound val is used to signify a miss vs just a falesy val
    if isinstance(result, dict) and keynotfound in result:
        return default
    return result


def assoc(m, key, val):
    """Copy-on-write associates a value in a dict"""
    cpy = deepcopy(m)
    cpy[key] = val
    return cpy

def dissoc(m, key, val):
    cpy = deepcopy(m)
    del cpy[key]
    return cpy

def associn(m, path, value):
    """ Copy-on-write associates a value in a nested dict """
    def assoc_recursively(m, path, value):
        if not path:
            return value
        p = path[0]
        return assoc(m, p, assoc_recursively(m.get(p,{}), path[1:], value))
    return assoc_recursively(m, path, value)


def merge(*maps):
    """Merge all maps left to right"""
    copies = map(deepcopy, maps)
    return reduce(lambda acc, val: acc.update(val) or acc, copies)


def flatmap(f, coll):
    """Applies concat to the result of applying f to colls"""
    return list(chain(*map(f, coll)))


def indexunique(f, coll):
    """Build a map from the collection keyed off of f
    e.g.
        [{id:1,..}, {id:2, ...}] => {1: {id:1,...}, 2: {id:2,...}}

    Note: duplicates, if present, are overwritten
    """
    return zipmap(map(f, coll), coll)


def findfirst(f, coll):
    """Return first occurrence matching f, otherwise None"""
    result = list(dropwhile(f, coll))
    return result[0] if result else None


def zipmap(keys, vals):
    """Return a map from keys to values"""
    return dict(zip(keys, vals))


def compact(coll):
    """Returns a new list with all falsy values removed"""
    if isinstance(coll, dict):
        return {k:v for k,v in coll.items() if v is not None}
    else:
        return list(filter(None, coll))


def ifPresent(f):
    """Execute f only if value is present and not None"""
    def inner(value):
        if value:
            return f(value)
        else:
            return True
    return inner


def identity(x):
    """Identity function always returns the supplied argument"""
    return x


def unit(val):
    return val


def bind(val, f):
    return f(val) if val else None
