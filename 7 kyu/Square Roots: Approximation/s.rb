58475cce273e5560f40000fa


def approx_root(n)
  base = Math::sqrt(n).floor
  diff_gn = n - base**2
  diff_lg = (base+1)**2 - base**2
  (base + diff_gn.fdiv(diff_lg)).round(2)
end
____________________________
def approx_root(n)
  n**0.5 % 1 == 0 ? n**0.5 : (n**0.5).to_i + (n - (n**0.5).to_i**2).fdiv((n**0.5).ceil**2 - (n**0.5).to_i**2).round(2)
end
____________________________
def approx_root(n)
  u = (0..n).find{ |x| x ** 2 >= n }; gps = u ** 2
  return u if gps == n
  l = u - 1; lps = l ** 2
  (l + (n - lps).fdiv(gps - lps)).round(2)
end
