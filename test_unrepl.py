from unrepl import unrepl
import pytest


def test1():
    code = """\
>>> a = 1
>>> b = 2
>>> a + b
3
"""
    assert (
        unrepl(code, use_print_statements=True)
        == """\
a = 1
b = 2
_ = a + b; print(repr(_)) # a + b
#  3
"""
    )
    assert (
        unrepl(code, use_print_statements=False)
        == """\
a = 1
b = 2
a + b
#  3
"""
    )


def test2():
    code = """\
>>> for i in range(4):
...     i * i
...
0
1
4
9
>>> _
9
"""
    assert (
        unrepl(code, use_print_statements=True)
        == """\
for i in range(4):
    _ = i * i; print(repr(_)) # i * i

#  0
#  1
#  4
#  9
_ = _; print(repr(_)) # _
#  9
"""
    )
    assert (
        unrepl(code, use_print_statements=False)
        == """\
for i in range(4):
    i * i

#  0
#  1
#  4
#  9
_
#  9
"""
    )


def test_no_repl():
    with pytest.raises(ValueError):
        x = unrepl("")
    with pytest.raises(ValueError):
        x = unrepl(">>>")
    x = unrepl(">>> ")


if __name__ == "__main__":
    pytest.main(["-vv", "-s", __file__])
