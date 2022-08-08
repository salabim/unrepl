## The problem
Many blogs, courses, articles, (e)books present code fragments (and their output) from REPL output. But also
doctests in programs are presented that way.
Here's an example (from Fluent Python, 2nd edition):
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
That's all fine for reading (and doctests), but what if you want to run the code,
or use it in another program, or just play with it?

In that case, you can copy/paste the code and manually remove the `>>> ` and `... ` lines as well the generated output line(s).

Wait ... there must be a better way!

## The solution

The small `unrepl` utility is designed to do just that.

You just copy the code to the clipboard, e.g.:

```
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
and then run `unrepl`, which replaces the clupboard with:

```
board = []
for i in range(3):
    row = ['_'] * 3
    board.append(row)

board
#  [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
board[2][0] = 'X'
board
#  [['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]
``` 

And for the second example:
```
prices = {
   "banana": 1.20,
   "pineapple": 0.89,
   "apple": 1.57,
   "grape": 2.45,
}
#  
#  
min(prices)
#  'apple'
#  
max(prices)
#  'pineapple'
```
You can also choose to generate print statements for those lines that generate output,
so you can actually run the code and get the proper output, like:

```
prices = {
   "banana": 1.20,
   "pineapple": 0.89,
   "apple": 1.57,
   "grape": 2.45,
}
#  
#  
print(repr(eval('min(prices)')))
#  'apple'
#  
print(repr(eval('max(prices)')))
#  'pineapple'
```

Furthermore, `unrepl` can be used as a module (imported) in any Python program. 

## Installation
As unrepl.py is just a singe file program, you can just download unrepl.py from GitHub
https://github.com/salabim/unrepl
and put it in your working directory.
You can also install from anywhere with the `install_unrepl.py` script (also in the GitHub repository).

## Supported platforms
The utility should run on any Python implementation that has tkinter installed,
thus Windows (tested), MacOS (not tested) and Linux (not tested).
On top of that, the utility runs on iPadOS/iOS under Pythonista.


## Command line: clipboard translation
When you run `unrepl.py` from the command line, the program grabs the contents of the clipboard and
tries to remove the REPL overhead and handle prefixes a line that does not start with `>>> ` or `... `
with a `# ` to make it a comment.
The line that generated the output is either
* untranslated 
or
* changed into a proper print statement
The program prompts whether to use print statements.

## Combination with AutoHotKey (Windows only)
Under Windows, unrepl can be called with a hotkey, that inserts the converted clipboard directly.
So, for instance, if you want unrepl to be called with <Shift><Ctrl><Alt>v, add 
```
^!+v::
    RunWait, X:\utilities\unrepl.py,,hide
    Send, ^v
    return
```
to your AutoHotKeyScript (assuming unrepl.py is in X:\utilities\)

If conversion is not possible, the clipboard will be pasted untranslated.

With the -i command line option, it possible to avoid the question whether to include print statements.
Use `unrepl` -i y` to include print statements.
Use `unrepl` -i n` to not include print statements (i.e. leave lines creating output untouched).

## API
`unrepl` has just one public API function: `unrepl`:

```
def unrepl(code, include_print_statements=False):
    """
    Cleans up a code fragment from a REPL, with output lines

    Parameters
    ----------
    code : str
        code to clean up

    include_print_statements : bool
        if True (default) include print statements for lines that generate output
        if False, include lines untranslated for lines that generate output
        
    Returns
    -------
    Converted code, if proper REPL output
    
    Exceptions
    ----------
    Raises a unrepl.IncorrectClipboardError is code is not proper REPL output, i.e.
    first line starts with `>>> `.
    """
```

## Disclaimer
The `unrepl` utility does not provide a 100% reliable conversion. That's because the REPL output
is not analyzed in depth and thus will only serve the most basic REPL outputs.
Still, it will convert nearly all REPL output in a proper way.
