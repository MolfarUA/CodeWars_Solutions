def is_square(x)
  (r = Math.sqrt(x)).round == r
end
__________________________________
def is_square(x)
   x >= 0 && (x ** 0.5).floor == (x ** 0.5).ceil
end
__________________________________
def is_square(x)
  x >= 0 && Math.sqrt(x) % 1 == 0
end
__________________________________
def is_square(x)
  x>=0&&(x**0.5).to_i**2==x
end
