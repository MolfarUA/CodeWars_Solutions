56d0a591c6c8b466ca00118b


def is_triangular(t)
  Math.sqrt(8*t+1)%1 == 0.0
end
__________________________
def is_triangular(t, start = 1)
  t.positive? ? is_triangular(t - start, start + 1) : t.zero?
end
__________________________
def is_triangular(t)
a=b=1
a+=b+=1while a<t
a==t
end
__________________________
def is_triangular(t)
  Math.sqrt(8*t+1) == Math.sqrt(8*t+1).to_i
end
__________________________
def is_triangular(t)
  Math.sqrt(8*t+1)-Math.sqrt(8*t+1).to_i == 0
end
__________________________
def is_triangular(t)
  n = (-1 + (1 + 8 * t) ** 0.5) / 2; n.to_i == n
end
__________________________
def is_triangular(t)
  
  total = 0
  value = 1
  
  while (total < t)
    total += value
    value += 1
  end
  
  if (total == t)
    return true
  else
    return false
  end
  
end
