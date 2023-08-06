from trick import curry


@curry
def calc(a, b, c, d):
    return a **2 + b - c // d

def test_curry():
    assert calc(1)(2)(3)(4) == calc(1, 2, 3, 4)
