525f3eda17c7cd9f9e000b39


def zero(f = None): return 0 if not f else f(0)
def one(f = None): return 1 if not f else f(1)
def two(f = None): return 2 if not f else f(2)
def three(f = None): return 3 if not f else f(3)
def four(f = None): return 4 if not f else f(4)
def five(f = None): return 5 if not f else f(5)
def six(f = None): return 6 if not f else f(6)
def seven(f = None): return 7 if not f else f(7)
def eight(f = None): return 8 if not f else f(8)
def nine(f = None): return 9 if not f else f(9)

def plus(y): return lambda x: x+y
def minus(y): return lambda x: x-y
def times(y): return lambda  x: x*y
def divided_by(y): return lambda  x: x/y
__________________________
id_ = lambda x: x
number = lambda x: lambda f=id_: f(x)
zero, one, two, three, four, five, six, seven, eight, nine = map(number, range(10))
plus = lambda x: lambda y: y + x
minus = lambda x: lambda y: y - x
times = lambda x: lambda y: y * x
divided_by = lambda x: lambda y: y / x
__________________________
def zero(arg=""):  return eval("0" + arg)
def one(arg=""):   return eval("1" + arg)
def two(arg=""):   return eval("2" + arg)
def three(arg=""): return eval("3" + arg)
def four(arg=""):  return eval("4" + arg)
def five(arg=""):  return eval("5" + arg)
def six(arg=""):   return eval("6" + arg)
def seven(arg=""): return eval("7" + arg)
def eight(arg=""): return eval("8" + arg)
def nine(arg=""):  return eval("9" + arg)

def plus(n):       return "+%s" % n
def minus(n):      return "-%s" % n
def times(n):      return "*%s" % n
def divided_by(n): return "/%s" % n
__________________________
class Int(int):
    """Pseudo-int with operation on it.
    """
    def __init__(self, value=0):
        super(Int, self).__init__(value)
        self.operation = None

    def __call__(self, operand=None):
        if operand is None:
            return self
        elif operand.operation == 'times':
            return self * operand
        elif operand.operation == 'plus':
            return self + operand
        elif operand.operation == 'minus':
            return self - operand
        elif operand.operation == 'divided_by':
            return self / operand


def operation(name):
    def _operation(arg):
        arg.operation = name
        return arg
    return _operation


(zero, one, two, three, four, five, six, seven, eight, nine) = (
                                        Int(0),Int(1), Int(2), Int(3), Int(4),
                                        Int(5), Int(6), Int(7), Int(8), Int(9))

plus = operation('plus')
minus = operation('minus')
times = operation('times')
divided_by = operation('divided_by')
__________________________
id_ = lambda x: x
number = lambda x: lambda f=id_: f(x)
zero, one, two, three, four, five, six, seven, eight, nine = map(number, range(10))
plus = lambda x: lambda y: y + x
minus = lambda x: lambda y: y - x
times = lambda x: lambda y: y * x
divided_by = lambda x: lambda y: y // x
