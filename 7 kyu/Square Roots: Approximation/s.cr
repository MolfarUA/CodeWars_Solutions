58475cce273e5560f40000fa


def approx_root(n)
  a = (n**0.5).floor; b = a+1
  (a+(n-a*a)/(b*b-a*a)).round(2)
end
____________________________
def approx_root(n)
  top = 1.0
  while top * top < n
    top += 1
  end
  base = top - 1
  diff_gn = n - (base * base)
  diff_lg = (top * top) - (base * base)
  (base + (diff_gn / diff_lg)).round(2)
end
____________________________
def approx_root(n)
  return Math.sqrt(n) if Math.sqrt(n) % 1 == 0
  ss, ls = Math.sqrt(n).floor ** 2, Math.sqrt(n).ceil ** 2
  return Math.sqrt(ss) + ((n - ss).to_f / (ls - ss)).round(2)
end
