def f(x, y, z)
  x * (y + 1) * (z + 1) + (x + 1) * y * (z + 1) + (x + 1) * (y + 1) * z
end
_____________________________________
def f(x, y, z)
  z*(3*x*y+1+2*(x+y))+2*x*y+x+y
end
_____________________________________
def f(x, y, z)
  x*(y+1)*(z+1) + y*(x+1)*(z+1) + z*(x+1)*(y+1)
end
_____________________________________
def f(*xs)
  xs.map(&:succ).reduce(:*).then{ |p| xs.sum{ |x| p / x.succ * x } }
end
_____________________________________
def f(x, y, z)
  x * (y + 1) * (z + 1) + y * (z + 1) * (x + 1) + z * (x + 1) * (y + 1)
end
