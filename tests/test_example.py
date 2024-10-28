def inc(x):
    return x + 1


def test_inc_negative():
    assert inc(3) == 5


def test_inc_positive():
    assert inc(3) == 4
