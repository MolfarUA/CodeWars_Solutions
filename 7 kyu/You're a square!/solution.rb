def is_square(x)
  x < 0 ? false : Math.sqrt(x) % 1 == 0
end
__________________________________
def is_square(x)
  x > -1 && Math.sqrt(x) % 1 == 0;
end
__________________________________
def is_square(x)
  return false if x < 0
  (x ** 0.5) % 1 == 0
end
__________________________________
def is_square(x)
  (0..x).any?{|i|i*i==x}
end
__________________________________
def is_square(number)
  return false if number.negative?

  (Math.sqrt(number) % 1).zero?
end
__________________________________
def is_square(x)
  return false if x.negative?

  Math.sqrt(x) % 1 == 0 ? true : false
end
__________________________________
def is_square(x)
  if x >= 0 and x ** 0.5 == (x  ** 0.5).to_i then return true else return false end
end
