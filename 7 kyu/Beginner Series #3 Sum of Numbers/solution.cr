def get_sum(a,b)
  c = [a, b].max
  d = [a, b].min
  (d..c).sum
end

_______________________________________
def get_sum(a,b)
  ((a-b).abs+1)*(a+b)>>1
end

_______________________________________
def get_sum(a,b)
  if a > b
    (b..a).to_a.sum
  else
    (a..b).to_a.sum
  end
end

_______________________________________
def get_sum(a,b)
  ([a,b].min..[a,b].max).sum
end

_______________________________________
def get_sum(a, b)
  Range.new(*{a, b}.minmax).sum
end

_______________________________________
def get_sum(*a)
  (a.min..a.max).sum
end

_______________________________________
def get_sum(a, b)
  (a + b) * ((a - b).abs + 1) // 2
end
