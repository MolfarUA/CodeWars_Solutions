def head(arr):
    return arr[0]

def tail(arr):
    return arr[1:]

def init(arr):
    return arr[:-1]

def last(arr):
    return arr[-1]
_____________________________
head = lambda array: array[0]
tail = lambda array: array[1:]
init = lambda array: array[:-1]
last = lambda array: array[-1]
_____________________________
def head(l):
  return l[0] if len(l) > 0 else None
def last(l):
  return l[-1] if len(l) > 0 else None
def init(l):
  return l[:-1] if len(l) > 1 else []
def tail(l):
  return l[1:] if len(l) > 1 else []
_____________________________
def head(array):
  return array[0]
def tail(array):
  return array[1:]
def init(array):
  return array[:-1]
def last(array):
  return array[-1]
_____________________________
def head(l):  return l[0]
def tail(l):  return l[1:]
def init(l):  return l[:-1]
def last(l):  return l[-1]
_____________________________
from operator import itemgetter

head = itemgetter(0)
tail = itemgetter(slice(1, None))
init = itemgetter(slice(-1))
last = itemgetter(-1)
_____________________________
head = lambda L: L[0]
tail = lambda L: L[1:]
init = lambda L: L[:-1]
last = lambda L: L[-1]
_____________________________
head = lambda xs: xs[0]
tail = lambda xs: xs[1:]
init = lambda xs: xs[:-1]
last = lambda xs: xs[-1]
