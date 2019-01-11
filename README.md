# Exotic Function

A module for writing in a functional and/or declarative style, but in an exotic way!

You can curry, compose, and do other stuff with the help of the exotic functions.

## Quick Example

Here is an example:

```python
>>> exotic % print * 'output: ' | unpack << exotic % map * int @ str.split @ input * 'numbers: ' | apply
numbers: 1 2 3 4
output:  1 2 3 4
```

which is equivalent to:

```python
>>> print('output: ', *(list(map(int, str.split(input('numbers: '))))))
```

or in a more readable way:

```python
inp = input('numbers: ').split()
inp = map(int, inp)
print('output: ', *inp)
```

more examples can be found in the module source file, `builder.py`.

## Testing

To test the module run:
```
$ python3 -m doctest -v builder.py
```
