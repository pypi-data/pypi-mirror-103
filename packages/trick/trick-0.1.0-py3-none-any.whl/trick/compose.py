from typing import TypeVar, Callable
from functools import reduce
from .identity import identity


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def _compose(g: Callable[[B], C], f: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: g(f(x))

def compose(*funcs: Callable):
    # TODO: can it typed?
    return reduce(_compose, funcs, identity)

