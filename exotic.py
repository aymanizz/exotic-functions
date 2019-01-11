# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

"""Exotic Functions and where to find them.
Exotic functions provide the ability to curry and compose them.
This is achieved through overriding some operators (for the list of operators
defined see the class `ExoticFunction`.)

This module defines the following:
    - `ExoticFunction`: see class documentation for more info.
    - `exotic`: a helper function for constructing exotic functions
    - `unpack`: an exotic function that unpacks the argument it recieves
        and feeds it to a function passed to it as an argument.
    - `apply`: an exotic function for ever exotic application of functions!

Examples:
    >>> exotic % print * 'Hello, world' | apply
    Hello, world
    >>> exotic % list @ map * int @ str.split @ str.strip | apply << ' 1  2  3   4  '
    [1, 2, 3, 4]
    >>> # the above can also be done in a similar way using `*`
    >>> exotic % list @ map * int @ str.split @ str.strip * ' 1  2  3   4  ' | apply
    [1, 2, 3, 4]
    >>> exotic % print | unpack >> [1, 2, 3, 4] | apply
    1 2 3 4
    >>> exotic % print * "output:" | unpack << exotic % list @ map * int @ str.split * '1 2 3 4' | apply
    output: 1 2 3 4
"""

from functools import partial
from collections import Callable

class ExoticFunction(Callable):
    """ExoticFunction class.
    an object of type `ExoticFunction` is a callable that defines the following operators:

    `*`  -- for partial application.

    `<<` -- for partial application, but has a lower precedence.

    `>>` -- for partial application, useful for passing arguments wrapped in a lambda.

    `@`  -- for composing function.

    `|`  -- for feeding one ExoticFunction instance to another.

    calling an instance of this class will cause it to be applied.
    """
    def __init__(self, func, _composed=lambda x: x):
        """Construct an exotic function from `func`."""
        self.func = func
        self._composed = _composed

    def __call__(self, *args, **kwargs):
        """Fully apply self."""
        return self._composed(self.func(*args, **kwargs))

    def __matmul__(self, func):
        """Compose `self` and `func`. `self` is applied after `func`"""
        return ExoticFunction(func, self)

    def __mul__(self, arg):
        """Partially apply `self` to `arg`."""
        return ExoticFunction(partial(self.func, arg), self._composed)

    def __rshift__(self, arg):
        """Wrap `arg` in a lambda and partially apply `self` to it."""
        return self.__mul__(lambda *, __x=arg: __x)

    def __lshift__(self, arg):
        """Partially apply `self` to `arg`."""
        return self.__mul__(arg)

    def __or__(self, modifier):
        """Call `modifer`, passing `func=self`.
        the expression `exotic_func | modifer` is equivalent to `modifier(exotic_func)`
        """
        return modifier(func=self)


class _ExoticBuilder:
    def __init__(self, builder):
        self.builder = builder

    def __mod__(self, func):
        return self.builder(func)


@_ExoticBuilder
def exotic(func):
    """Constructs an exotic function from `func`."""
    return ExoticFunction(func)

@ExoticFunction
def unpack(arg, func=None):
    """Partially apply `func` passing unpacked result of calling `arg` to it."""
    return ExoticFunction(partial(func, *arg()))

@ExoticFunction
def apply(*args, func=None):
    """Call `func` passing unpacked args to it"""
    if func is None:
        func = args[0]
        return func(*args[1:])
    else:
        return func(*args)

@ExoticFunction
def identity(x):
    return x
