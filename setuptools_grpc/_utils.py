"""Setuptools grpc utils."""


# Taken from https://github.com/python-babel/babel/blob/master/babel/messages/frontend.py
def listify_value(arg, split=None):
    """Make a list out of an argument.

    Values from `distutils` argument parsing are always single strings;
    values from `optparse` parsing may be lists of strings that may need
    to be further split.
    No matter the input, this function returns a flat list of whitespace-trimmed
    strings, with `None` values filtered out.
    >>> listify_value("foo bar")
    ['foo', 'bar']
    >>> listify_value(["foo bar"])
    ['foo', 'bar']
    >>> listify_value([["foo"], "bar"])
    ['foo', 'bar']
    >>> listify_value([["foo"], ["bar", None, "foo"]])
    ['foo', 'bar', 'foo']
    >>> listify_value("foo, bar, quux", ",")
    ['foo', 'bar', 'quux']
    :param arg: A string or a list of strings
    :param split: The argument to pass to `str.split()`.
    :return:
    """
    out = []

    if not isinstance(arg, (list, tuple)):
        arg = [arg]

    for val in arg:
        if val is None:
            continue
        if isinstance(val, (list, tuple)):
            out.extend(listify_value(val, split=split))
            continue
        out.extend(s.strip() for s in str(val).split(split))
    assert all(isinstance(val, str) for val in out)  # noqa: S101
    return out


def py_module_name(file):
    return "%s_pb2.py" % file.rpartition(".")[0]


def grpc_py_module_name(file):
    return "%s_pb2_grpc.py" % file.rpartition(".")[0]
