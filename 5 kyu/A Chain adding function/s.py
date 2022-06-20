539a0e4d85e3425cb0000a88


class add(int):
    def __call__(self,n):
        return add(self+n)
______________________
class CustomInt(int):
    def __call__(self, v):
        return CustomInt(self + v)

def add(num):
    return CustomInt(num)
______________________
def add(n):
    return MyInt(n)
    
class MyInt(object):
    def __init__(self, n):
        self.value = n

    def __add__(self, n):
        return MyInt(self.value + n)
        
    def __sub__(self, n):
        return MyInt(self.value - n)
        
    def __call__(self, n):
        return MyInt(self.value + n)
        
    def __eq__(self, other):
        if isinstance(other, MyInt):
            return self.value == other.value
        else:
            return self.value == other
______________________
class add(int):
    __call__ = lambda self, value: add(self + value)
______________________
class Add(int):
    def __call__(self, value):
        return Add(self + value)
add = Add()
______________________
class AddValues(int):
    def __call__(self, IntValue):
        return AddValues(self + IntValue)
def add(n):
    return AddValues(n)
______________________
class add(int):
    def __init__(self, num):
        self.num = num
    
    def __call__(self, addition):
        return add(self.num + addition)
    
    def __str__(self):
        return self.num
______________________
class curryable(type):
    #self note:bound methods dont get double instantiated unless manually set in instantiated class
    #and even then, it doesn't bind in a desirable way(at least in this context)
    def __new__(mcs, **kwargs):
        return super().__new__(mcs, 'cFunction', (kwargs['base'],), {})
    def __init__(self, value=None, **kwargs):
        self.func = kwargs['func']
        self.__call__ = self.call()
    def call(cls):
        #the purpose of this function is that without it, new_class.__call__ is a bound
        #method where the first variable(self) is bound to neww_class, as it is the instance of curryable
        def __call__(self, x):
            tmp = self.__class__(self.func(x) or self)
            self.__init__()
            return tmp
        return __call__

add = curryable(base=int, func=(lambda self,y: self+y))()
