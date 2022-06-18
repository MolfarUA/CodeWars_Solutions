55f9b48403f6b87a7c0000bd


def paperwork(n, m)
  n >= 0 && m >= 0 ? n * m : 0
end
__________________________
def paperwork(n, m)
  m < 0 || n < 0 ? 0 : m*n
end
__________________________
def paperwork(n, m)
  if n < 0 || m < 0
    return 0
  else
    return m*n
  end
end
__________________________
def paperwork(n, m)
  n * m
  if n <= 0 or m <= 0
    return 0
  else
    return n * m
  end  
end
__________________________
def paperwork(n, m)
  sum = n * m
  if n < 0 or m < 0 
    return 0
    else
    sum
end
  end
__________________________
def paperwork(n, m)
  unless n < 1 or m < 1 then n * m else 0 end
end
__________________________
def paperwork(n, m)
  paper = n*m
   n <= 0 || m <= 0 ? 0 : paper
end
