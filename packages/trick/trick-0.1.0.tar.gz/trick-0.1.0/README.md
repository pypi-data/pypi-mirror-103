# python-trick

一些helper函数合集。

## Reference

### compose

```python
def add_ten(x: int) -> int:
    return x + 10

def multi_five(x: int) -> int:
    return x * 5

add_ten_then_multi_five = compose(multi_five, add_ten)

add_ten_then_multi_five(2)  # output: 60
```

### curry

```python
@curry
def add(a, b, c, d):
    return a + b + c + d

assert add(1, 2, 3, 4) == add(1)(2)(3)(4)
```
