from trick import compose


def plus_two(x: int) -> int:
    return x + 2

def double(x: int) -> int:
    return x * 2

def minus_one(x: int) -> int:
    return x - 1


def test_compose_order():
    plus_double = compose(double, plus_two)
    double_plus = compose(plus_two, double)

    assert plus_double(4) == 12
    assert double_plus(4) == 10


def test_associative_law():
    foo = compose(compose(plus_two, double), minus_one)
    bar = compose(plus_two, compose(double, minus_one))
    assert foo(4) == bar(4)

