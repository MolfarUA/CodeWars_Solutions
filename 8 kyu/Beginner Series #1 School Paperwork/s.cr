55f9b48403f6b87a7c0000bd


def paperwork(n, m)
  n > 0 && m > 0 ? n * m : 0
end
__________________________
def paperwork(n, m)
  if n < 0 || m < 0
    0
  else
    n * m
  end
end
__________________________
def paperwork(n, m)
  return 0 if n<0 || m<0
  n*m
end
__________________________
def paperwork(n, m)
  (n < 1 || m < 1) ? 0 : n * m
end
__________________________
def paperwork(n, m)
  return (n < 0 || m < 0)? 0: n * m
end
__________________________
def paperwork(n, m)
 if n < 0 || m < 0
    return 0
  else
    n * m
  end
end
