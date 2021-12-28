def get_sum(a,b)
  return a < b ? (a..b).reduce(:+) : (b..a).reduce(:+) 
end

_______________________________________
def get_sum(a,b)
  (a..b).reduce(:+) || (b..a).reduce(:+)
end

_______________________________________
def get_sum(a,b)
  Range.new(*[a, b].sort).reduce(:+)
end

_______________________________________
def get_sum(a,b)
  (a + b) / 2.0 * ((a - b).abs + 1)
end

_______________________________________
def get_sum(a,b)
  smaller, higher = [a, b].sort

  (smaller..higher).sum
end

_______________________________________
def get_sum(a,b)
  ([a,b].min..[a,b].max).sum
end

_______________________________________
def get_sum(a,b)
  sum = 0
  if a < b
    (a..b).to_a.each { |num| sum += num }
  else
    (b..a).to_a.each { |num| sum += num }
  end
  return sum
end
