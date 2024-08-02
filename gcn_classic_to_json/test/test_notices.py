import importlib.resources
from json import load

import pytest

from .. import notices
from ..json import dumps

files = importlib.resources.files(notices)


@pytest.mark.parametrize("key", notices.keys)
def test_notices(key, generate):
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
