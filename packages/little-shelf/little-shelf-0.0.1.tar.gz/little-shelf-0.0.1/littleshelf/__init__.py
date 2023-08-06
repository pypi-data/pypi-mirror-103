"""Synchronized dictionaries."""

import json  # TODO use native comparisons


def is_dict(obj):
    return isinstance(obj, dict)


def read(shelf):
    """
    Return a dictionary containing shelf contents only.

        >>> read([{"coords": [{"x": [222, 0], "y": [444, 0]}, 0]}, 0])
        {'coords': {'x': 222, 'y': 444}}

    """
    if is_dict(shelf[0]):
        return {k: read(v) for k, v in shelf[0].items()}
    else:
        return shelf[0]


def create_patch(shelf, content):
    """
    Return a shelf containing changes to the content.

        >>> create_patch([{"coords": [{"x": [222, 0], "y": [444, 0]}, 0]}, 0],
        ...              {"coords": {"x": 222, "y": 445}})
        [{'coords': [{'y': [445, 1]}, 0]}, 0]

    """
    def is_equal(a, b):
        if is_dict(a):
            return is_dict(b)
        return a == b

    if is_equal(shelf[0], content):
        if is_dict(content):
            ret = [{}, shelf[1]]
            for k, v in shelf[0].items():
                if v[0] is not None and k not in content:
                    v[0] = None
                    v[1] += 1
                    ret[0][k] = v
            for k, v in content.items():
                if k not in shelf[0]:
                    shelf[0][k] = [None, shelf[1] - 1]
                changes = create_patch(shelf[0][k], v)
                if changes:
                    ret[0][k] = changes
            return ret if ret[0] else None
    else:
        shelf[1] += 1
        if is_dict(content):
            shelf[0] = {}
            for k, v in content.items():
                if is_dict(v):
                    shelf[0][k] = [None, shelf[1] - 1]
                    create_patch(shelf[0][k], v)
                else:
                    shelf[0][k] = [v, shelf[1]]
        else:
            shelf[0] = content
        return shelf


def merge(a, b):
    """
    Modify shelf a to incorporate changes from shelf b.

        >>> alice = [None, -1]
        >>> bob = [{"coords": [{"x": [222, 0], "y": [444, 0]}, 0]}, 0]
        >>> merge(alice, bob)
        True
        >>> alice
        [{'coords': [{'x': [222, 0], 'y': [444, 0]}, 0]}, 0]
        >>> alice == bob
        True

        >>> alice = [{"coords": [{"x": [222, 0], "y": [445, 1]}, 0]}, 0]
        >>> merge(bob, alice)
        True
        >>> bob
        [{'coords': [{'x': [222, 0], 'y': [445, 1]}, 0]}, 0]
        >>> alice == bob
        True

    """
    mutated = False

    def is_less_than(a, b):
        if is_dict(a):
            return True
        if is_dict(b):
            return False
        return json.dumps(a) < json.dumps(b)

    if is_dict(a[0]) and is_dict(b[0]):
        if b[1] > a[1]:
            mutated = True
            a[1] = b[1]
            for k, v in a[0].items():
                if (v[1] < a[1]):
                    del a[0][k]
        for k, v in b[0].items():
            if v[1] < a[1]:
                continue
            if k not in a[0]:
                mutated = True
                a[0][k] = [None, -1]
            if merge(a[0][k], v):
                mutated = True
    else:
        if b[1] > a[1] or (b[1] == a[1] and is_less_than(b[0], a[0])):
            mutated = True
            a[0] = b[0]
            a[1] = b[1]
    return mutated


class LittleShelf:

    """
    A Little shelf.

    """

    def __init__(self):
        self._shelf = [None, -1]
        self._content = {}

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self._content[k] = v
        return create_patch(self._shelf, self._content)

    def merge(self, patch):
        merge(self._shelf, patch)
        self._content = read(self._shelf)

    def __getitem__(self, key):
        return self._content[key]

    get = __getitem__

    def __repr__(self):
        return repr(self._content)

    def __eq__(self, other):
        try:
            other_content = other._content
        except AttributeError:
            other_content = other
        return self._content == other_content
