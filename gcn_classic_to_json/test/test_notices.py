import importlib.resources
from json import load

import numpy as np
import pytest

from .. import notices
from ..json import dumps
from ..notices import _frombuffer as _orig_frombuffer

files = importlib.resources.files(notices)


def keys_passing_except_for(*failing):
    return list(set(notices.keys) - set(failing)) + [
        pytest.param(item, marks=pytest.mark.xfail) for item in failing
    ]


@pytest.mark.parametrize(
    "key",
    keys_passing_except_for("SWIFT_BAT_GRB_POS_ACK"),
)
def test_all_fields_used(key, monkeypatch):
    """Check that every field in the binary packet is used in the conversion."""
    used = np.zeros(40, dtype=bool)

    class NDArrayNanny(np.ndarray):
        def __getitem__(self, i):
            used[i] = True
            return super().__getitem__(i)

    def mock_frombuffer(*args, **kwargs):
        return _orig_frombuffer(*args, **kwargs).view(NDArrayNanny)

    monkeypatch.setattr(notices, "_frombuffer", mock_frombuffer)

    bin_path = files / key / "example.bin"
    value = bin_path.read_bytes()
    notices.parse(key, value)

    if not used.all():
        raise AssertionError(
            f'All fields in the binary packet must be used. The fields with the following indices were unused: {' '.join(np.flatnonzero(~used).astype(str))}'
        )


@pytest.mark.parametrize("key", notices.keys)
def test_notices(key, generate):
    """Check the output of the parser against known JSON output."""
    bin_path = files / key / "example.bin"
    json_path = files / key / "example.json"

    value = bin_path.read_bytes()
    actual = notices.parse(key, value)

    if generate:
        with json_path.open("w") as f:
            print(dumps(actual, indent=2), file=f)
        pytest.skip(f"saved expected output to {json_path}")

    with json_path.open("r") as f:
        expected = load(f)
    assert actual == expected
