import unrepl

repl_output = """\
>>> import math
>>> angle = 90
>>> math.radians(90)
1.5707963267948966
>>> math.pi / 2
1.5707963267948966
"""
unrepled = unrepl.unrepl(repl_output, use_print_statements=True)
print(unrepled)
print("execute ...")
exec(unrepled)

repl_output = """\
>>> def square(x):
...     (1, 2, 'ab')
(1, 2, 'ab')       
...     return x * x
>>> a=0
>>> b=2
>>> a+b
2
>>> square(_) * 'test'
'testtesttesttest'
"""
print("-----")
unrepled = unrepl.unrepl(repl_output, use_print_statements=True)
print(unrepled)
print("execute ...")
exec(unrepled)


repl_output = """\
>>> for i in range(5):
...     i * i
...
...
0
1
4
9
16
>>> _
16
"""
print("-----")
unrepled = unrepl.unrepl(repl_output, use_print_statements=True)
print(unrepled)
print("execute ...")
exec(unrepled)

from unrepl import unrepl

raise unrepl.IncorrectClipboardError('jj')
