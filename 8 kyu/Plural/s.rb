def plural(n)
  n != 1
end
__________________
def plural(n)
  return false if n == 1
  true
end
__________________
def plural(num)
  num == 1 ? false : true
end
__________________
def plural(n)
  if n < 1 || n > 1
    return true
  else
    return false
    end
  
end
__________________
def plural(n)
  n.eql?(1) ? false : true
end
__________________
def plural(n)
  if n <= 0.9
    return true
  elsif n == 1
    return false
  elsif n >= 2
    return true
  end
end
__________________
def plural(n)
  hash = {
    0 => true,
    0.5 => true,
    1 => false,
    100 => true,
    Float::INFINITY => true
  }
  case n
    when 0
      true
    when 0.5
      true
    when 1
      false
    when 100
      true
    else
      true
  end
end
__________________
def plural(n)
  Float(n) != 1
end
