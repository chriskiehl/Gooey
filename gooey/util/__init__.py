from functools import reduce
from inspect import signature



def apply_transforms(data, func):
    return func(data)


def bootlegCurry(f):
    '''
    a bootleg curry.
    '''
    def _curry(f, remaining):
        def inner(*args):
            if len(args) >= remaining:
                return f(*args)
            else:
                newfunc = lambda *rem: f(*args, *rem)
                return _curry(newfunc, remaining - len(args))
        return inner
    return _curry(f, len(signature(f).parameters))


def excluding(item_dict, *to_exclude):
    excluded = set(to_exclude)
    return {key: val for key, val in item_dict.items()
            if key not in excluded}


def indentity(x):
    return x


def merge(*args):
    return reduce(lambda acc, val: acc.update(val) or acc, args, {})


def partition_by(f, coll):
    a = []
    b = []
    for item in coll:
        bucket = a if f(item) else b
        bucket.append(item)
    return a, b




if __name__ == '__main__':
    pass
    # a = {
    #     'a': 111,
    #     'b': 111,
    #     'c': 111,
    #     1: 111
    # }
    # print(excluding(a, 'a', 'c', 1))
