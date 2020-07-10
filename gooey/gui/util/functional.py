'''
Utils for functional methodologies throughout Gooey

'''


def merge_dictionaries(x,y):
    """
    Merge 2 dictionaries with y taking overwriting x if a key collision is found

    This is mainly useful for maintaining the dictionary arguments to allow for more expressive & extensible arguments.
    https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python-taking-union-o

    Args:
        x (dict): Input dictionary
        y (dict): Input dictionary

    Returns:
        The combined dictionary of x & y with y taking preference on the occasion of key collision
    """
    if x is None:
        x = {}
    if y is None:
        y = {}
    try:
        return {**x,**y}
    except:
        z = x.copy()
        z.update(y)
        return z
