# -*- coding: utf-8 -*-
#
# system utilities methods
# IMIO <support@imio.be>
#

from collections import OrderedDict

# ------------------------------------------------------------------------------


def safe_encode(value, encoding='utf-8'):
    """Converts a value to encoding, only when it is not already encoded."""
    if isinstance(value, unicode):
        return value.encode(encoding)
    return value

# ------------------------------------------------------------------------------


def insert_in_ordereddict(dic, value, after_key='', at_position=None):
    """Insert a tuple in an new Ordereddict.

        :param dic: the original OrderedDict
        :param value: a tuple (key, value) that will be added at correct position
        :param after_key: key name after which the tup is added
        :param at_position: position at which the tup is added. Is also a default if after_key is not found
        :return: a new OrderedDict or None if insertion position is undefined
    """
    position = None
    if after_key is not None:
        keys = dic.keys()
        if after_key in keys:
            position = keys.index(after_key) + 1
    if position is None and at_position is not None:
        position = at_position
    if position is None:
        return None
    if position >= len(dic.keys()):
        return OrderedDict(dic.items() + [value])
    tuples = []
    for i, tup in enumerate(dic.items()):
        if i == position:
            tuples.append(value)
        tuples.append(tup)
    if not tuples:  # dic was empty
        tuples.append(value)
    return OrderedDict(tuples)


def replace_in_list(lst, value, replacement, generator=False):
    """
        Replace a value in a list of values.
        :param lst: the list containing value to replace
        :param value: the value to be replaced
        :param replacement: the new value to replace with
        :param generator=False: will return a generator instead a list when set to True
        :return: a new list/generator with replaced values
    """
    def _replacer(lst, value, replacement):
        new_lst = list(lst)
        for item in new_lst:
            if item == value:
                yield replacement
            else:
                yield item
    res = _replacer(lst, value, replacement)
    if not generator:
        res = list(res)
    return res
