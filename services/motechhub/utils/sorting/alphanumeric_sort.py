def alphanumeric_sort_key(key):
    """
    Sort the given iterable in the way that humans expect.
    Thanks to http://stackoverflow.com/a/2669120/240553
    """
    import re
    convert = lambda text: int(text) if text.isdigit() else text
    return [convert(c) for c in re.split('([0-9]+)', key)]


def alphanumeric_sorted(iterable, key=None):
    if key is None:
        return sorted(iterable, key=alphanumeric_sort_key)
    else:
        return sorted(iterable, key=lambda x: alphanumeric_sort_key(key(x)))
