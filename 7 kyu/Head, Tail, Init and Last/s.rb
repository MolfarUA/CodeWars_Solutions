def head(array)
  array[0]
end

def tail(array)
  array[1..-1]
end

def init(array)
  array[0..-2]
end

def last(array)
  array[-1]
end
_____________________________
def head(xs) xs.first end
def last(xs) xs.last end
def tail(xs) xs.drop(1) end
def init(xs) xs.take(xs.size-1) end
_____________________________
def head(xs) xs[0] end
def tail(xs) xs[1..-1] end
def init(xs) xs[0...-1] end
def last(xs) xs[-1] end
_____________________________
def head(arr)
  arr.first
end
def tail(arr)
  return [] if arr.length <= 1
  arr.slice(1, arr.length - 1)
end

def init(arr)
  arr.slice(0, arr.length - 1)
end

def last(arr)
  arr[arr.length-1]
end
