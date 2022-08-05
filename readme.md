## The problem
Many books, blogs, courses, articles present code fragments (and their output) from REPL output, like (from Fluent Python, 2nd edition):
```
>>> board = []
>>> for i in range(3):
...     row = ['_'] * 3
...     board.append(row)
... 
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[2][0] = 'X'  
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]
```

Or (from a RealPython course):
```
>>> prices = {
...    "banana": 1.20,
...    "pineapple": 0.89,
...    "apple": 1.57,
...    "grape": 2.45,
... }


>>> min(prices)
'apple'

>>> max(prices)
'pineapple'
```
That's all fine for reading, but what if you want to run the code, or use it in another program, or just pleay with it?

In that case, you can copy the copy/paste the code and manually remove the `>>> ` and `... ` lines as well the generated output line(s).

Wait ... there must be a better way!

## The solution

The small `unrepl` utility is designed to do just that:

```
from unrepl import unrepl

print(unrepl("""\
>>> board = []
>>> for i in range(3):
...     row = ['_'] * 3
...     board.append(row)
... 
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[2][0] = 'X'  
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]"""))
```
When you run this, you will get:
```
board = []
for i in range(3):
    row = ['_'] * 3
    board.append(row)

print(repr(eval('board')))
board[2][0] = 'X'
print(repr(eval('board')))
------------------------------output------------------------------
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
[['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]
``` 

And for the second example:
```
from unrepl import unrepl

print(unrepl("""\
>>> prices = {
...    "banana": 1.20,
...    "pineapple": 0.89,
...    "apple": 1.57,
...    "grape": 2.45,
... }


>>> min(prices)
'apple'

>>> max(prices)
'pineapple'
""")
```
, resulting in
```
prices = {
   "banana": 1.20,
   "pineapple": 0.89,
   "apple": 1.57,
   "grape": 2.45,
}
print(repr(eval('min(prices)')))
print(repr(eval('max(prices)')))
------------------------------output------------------------------
'apple'
'pineapple'
```

## Installation
As unrepl.pynis just a singe file program, you can just download unrepl.py from GitHub and put it
in your working directory.

