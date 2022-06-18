56d0a591c6c8b466ca00118b


def is_triangular(t) 
  Math.sqrt(8 * t + 1) % 1 == 0
end
__________________________
def is_triangular(t) 
  ((t * 8 + 1) ** 0.5 % 1).zero?
end
