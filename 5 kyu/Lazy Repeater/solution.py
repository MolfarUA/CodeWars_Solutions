51fc3beb41ecc97ee20000c3


from itertools import cycle

def make_looper(s):
    g = cycle(s)
    return lambda: next(g)
_____________________________
from itertools import cycle

class make_looper(cycle):
    
    def __call__(self):
        return self.__next__()
_____________________________
from itertools import cycle

def make_looper(string):
    return cycle(string).__next__
_____________________________
def make_looper(string):
    global str
    str = string
    func1(str)
    return func
    
def func1(string):
    global x
    x = iter(string)
    
def func():
    try:
        elem = next(x)
    except StopIteration:
        func1(str)
        elem = next(x)
    return elem
_____________________________
from itertools import cycle

def make_looper(string):
    str_iter = cycle(string)
    
    def generate():
        return str_iter.__next__()
        
    return generate
_____________________________
class make_looper:
    
    def __init__(self, string):
        self.string = string
        self.ind = -1
        
    def __call__(self):
        self.ind += 1
        
        if self.ind >= len(self.string):
            self.ind = 0
        
        return self.string[self.ind]
_____________________________
def make_looper(string):
    def gen():
        while True:
            for s in string:
                yield s

    def return_func():
        return next(return_func.generator)

    return_func.generator = gen()
    return return_func
_____________________________
def make_looper(string):
    idx = -1
    
    def get_abc():
        nonlocal idx
        idx += 1
        abc = list(string)
        return abc[idx % len(abc)]
    
    return get_abc
_____________________________
def make_looper(string):
    pos=-1
    def insidefunc():
        nonlocal pos
        pos += 1
        if pos==len(string): pos=0
        return string[pos]
    return insidefunc
_____________________________
sss = ""
def make_looper(ss):
    global sss
    sss=ss
    def abc():
        global sss
        sss = sss[1:]+sss[0]
        return sss[-1]
    return abc
_____________________________
from itertools import cycle


def make_looper(string):
    if 'rep' not in globals() and 'rep_string' not in globals():
        global rep
        global rep_string
        rep = ''
        rep_string = ''
    if rep_string != string:
        rep = cycle(string)
        rep_string = string
    return lambda: next(rep)
_____________________________

def make_looper(string):
    def loop():
        loop.counter +=1
        if loop.counter >= len(string):
            loop.counter = 0
        return ( string[loop.counter] )  

    loop.counter = -1
    return loop
_____________________________
real_string = ""
def real_func():
    global count,real_string
    count = (count+1)%len(real_string)
    print(real_string[count])
    return real_string[count]
def make_looper(string):
    global real_string,count
    real_string = string
    count = -1
    return real_func
_____________________________
class make_looper:
    def __init__(self, s):
        self.i = -1
        self.s = s

    def __call__(self):
        self.i += 1
        return self.s[self.i % len(self.s)]
_____________________________
class make_looper:
    
    def __init__(self, string):
        self.string = string;
        self.c = -1
    
    def __call__(self):
        if self.c < len(self.string)-1:
            self.c += 1
            return self.string[self.c]
        self.c = 0
        return self.string[0]
