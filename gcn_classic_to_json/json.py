from json import dump as _orig_dump
from json import dumps as _orig_dumps
from json import load, loads

import numpy as np

__all__ = ("dump", "dumps", "load", "loads")


def _default(value):
    if isinstance(value, np.ndarray):
        if value.ndim == 0:
            return value.item()
        else:
            return [_default(item) for item in value]
    elif isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, np.inexact):
        return float(value)
    return value


def dumps(*args, **kwargs):
    """
    Serialize data structures to JSON, handling all real number Numpy types.

    The arguments are the same as :func:`json.dumps`.

    Examples
    --------

    >>> dumps(np.asarray([1, 2, 3]))
    '[1, 2, 3]'

    >>> dumps(np.asarray([1.0, 2.0, 3.0]))
    '[1.0, 2.0, 3.0]'

    >>> dumps(np.int32(4))
    '4'

    >>> dumps(np.asarray(4, dtype='>i4'))
    '4'

    >>> dumps(np.arange(4, dtype='>i4'))
    '[0, 1, 2, 3]'

    >>> dumps(np.eye(3))
    '[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]'
    """
    return _orig_dumps(*args, default=_default, **kwargs)


def dump(*args, **kwargs):
    """
    Serialize data structures to JSON, handling all real number Numpy types.

    The arguments are the same as :func:`json.dumps`.

    Examples
    --------

    >>> import io
    >>> stream = io.StringIO()
    >>> dump(np.asarray([1, 2, 3]), stream)
    >>> stream.getvalue()
    '[1, 2, 3]'

    >>> stream = io.StringIO()
    >>> dump(np.asarray([1.0, 2.0, 3.0]), stream)
    >>> stream.getvalue()
    '[1.0, 2.0, 3.0]'

    >>> stream = io.StringIO()
    >>> dump(np.int32(4), stream)
    >>> stream.getvalue()
    '4'

    >>> stream = io.StringIO()
    >>> dump(np.asarray(4, dtype='>i4'), stream)
    >>> stream.getvalue()
    '4'

    >>> stream = io.StringIO()
    >>> dump(np.arange(4, dtype='>i4'), stream)
    >>> stream.getvalue()
    '[0, 1, 2, 3]'

    >>> stream = io.StringIO()
    >>> dump(np.eye(3), stream)
    >>> stream.getvalue()
    '[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]'
    """
    return _orig_dump(*args, default=_default, **kwargs)
