"""
Provide pre-/postconditions as function decorators.

Example usage:

  >>> def in_ge20(inval):
  ...    assert inval >= 20, 'Input value < 20'
  ...
  >>> def out_lt30(retval, inval):
  ...    assert retval < 30, 'Return value >= 30'
  ...
  >>> @precondition(in_ge20)
  ... @postcondition(out_lt30)
  ... def inc(value):
  ...   return value + 1
  ...
  >>> inc(5)
  Traceback (most recent call last):
    ...
  AssertionError: Input value < 20
  >>> inc(29)
  Traceback (most recent call last):
    ...
  AssertionError: Return value >= 30
  >>> inc(20)
  21

You can define as many pre-/postconditions for a function as you
like. It is also possible to specify both types of conditions at once:

  >>> @conditions(in_ge20, out_lt30)
  ... def add1(value):
  ...   return value + 1
  ...
  >>> add1(5)
  Traceback (most recent call last):
    ...
  AssertionError: Input value < 20

An interesting feature is the ability to prevent the creation of
pre-/postconditions at function definition time. This makes it
possible to use conditions for debugging and then switch them off for
distribution.

  >>> debug = False
  >>> @precondition(in_ge20, debug)
  ... def dec(value):
  ...   return value - 1
  ...
  >>> dec(5)
  4
"""

__all__ = ['precondition', 'postcondition', 'conditions']

DEFAULT_ON = True

def in_ge20( inval):
    print "cls"
    
def out_lt30( retval, inval):
    print "cls"

def precondition(func):
    def decorated(*args, **kwargs):
        a= conditions(in_ge20, None, DEFAULT_ON, func, *args, **kwargs)
        return a.wrapper()
    return decorated

def postcondition(func):
    def decorated(*args, **kwargs):
        a= conditions(None, out_lt30, DEFAULT_ON, func, *args, **kwargs)
        return a.wrapper()
    return decorated

class conditions(object):
    wrapper= None

    def __init__(self, pre, post, use_conditions, function, *args, **kwargs):
        if not use_conditions:
            pre, post = None, None

        self.__precondition  = pre
        self.__postcondition = post

        # combine recursive wrappers (@precondition + @postcondition == @conditions)
        pres  = set((self.__precondition,))
        posts = set((self.__postcondition,))

        # unwrap function, collect distinct pre-/post conditions
        while type(function) is FunctionWrapper:
            pres.add(function._pre)
            posts.add(function._post)
            function = function._func

        # filter out None conditions and build pairs of pre- and postconditions
        conditions = map(None, filter(None, pres), filter(None, posts))

        # add a wrapper for each pair (note that 'conditions' may be empty)
        for pre, post in conditions:
            function = FunctionWrapper(pre, post, function)

        self.wrapper= function

class FunctionWrapper(object):
    def __init__(self, precondition, postcondition, function):
        self._pre  = precondition
        self._post = postcondition
        self._func = function

    def __call__(self, *args, **kwargs):
        precondition  = self._pre
        postcondition = self._post

        if precondition:
            precondition(self, *args, **kwargs)
        result = self._func(*args, **kwargs)
        if postcondition:
            postcondition(self, result, *args, **kwargs)
        return result
   
class test(object):     
    @precondition
    @postcondition
    def inc(self, value):
        print self
        return value + 1
    
    class __metaclass__(type):
        def __new__(cls, name, bases, dict_):
            print("Creating class %s%s with attributes %s" % (name, bases, dict_))
            return type.__new__(cls, name, bases, dict_)
print "a"   
a= test()
a.inc(5)