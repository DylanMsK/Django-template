import pytest


def square(a):
    return a * a


@pytest.mark.parametrize(
    ("a", "expected"),
    [(2, 4), (3.0, 9.0), (-2, 4)],
)
def test_square(a, expected):
    assert square(a) == expected
