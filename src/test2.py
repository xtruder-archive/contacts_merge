class ADecorator(object):
    func = None
    def __new__(cls, func):
        dec = object.__new__(cls)
        dec.__init__(func)
        def wrapper(*args, **kw):
            print func
            return dec(func, *args, **kw)
        return wrapper

    def __init__(self, func, *args, **kw):
        self.func = func
        self.act  = self.do_first

    def do_first(self, *args, **kw):
        args[0].a()

    def __call__(self, func, *args, **kw):
        func= args[1]
        return self.act(*args, **kw)

class A(object):
    m= 0
    def a(self):
        print self.m

    @property
    def function(self):
        return "a"
    @function.setter
    @ADecorator
    def function(self, value):
        self.m=value

a = A()
a.function=2
print a.function
a.function= 3