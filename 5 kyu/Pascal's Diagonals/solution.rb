def generate_diagonal(d, l)
  b = nil
  l.times.map { | n | b = n == 0 ? 1 : b * (n + d) / n }
end
_______________________________
def generate_diagonal(n, l)
  l > 0 ? [m = 1, *(1...l).map{|t|m *= n+t; m /= t;}]
        : []
end
_______________________________
def generate_diagonal(n, l)
  result = []
  l.times.each{|i| result << (result.empty? ? 1 : result.last * (n+i) / i)}
  result
end
_______________________________
def generate_diagonal(n, l)
  
  f = Proc.new do |n|
    (1..n).reduce(1, :*)
  end
  
  arr = []
  for i in 0..l-1
    arr.push(f.call(n+i)/(f.call(n)*f.call(i)))
    end
  arr
end
_______________________________
def generate_diagonal(n, l)
  return [] if l <= 0
  res, c = [1], 1
  (1...l).each{|i|
    res[i] = c = c * (n + i) / i
  }
  res
end
_______________________________
def generate_diagonal(n, l)
  return [] if l <= 0
  res = [1]
  for i in 1...l
    res << res[-1] * (n + i) / i
  end
  res
end
_______________________________
def generate_diagonal(n, l)
  arr = []
  for i in 0..l-1
    arr.push(f(n+i)/(f(n)*f(i)))
    end
  arr
end

def f(n)
  (1..n).reduce(1, :*)
end
_______________________________
def generate_diagonal(n, l)
  return [] if l.zero?
  return [1] * l if n.zero?
  return (1..l).to_a if n == 1
  
  (0...l).collect{ |i| i == 0 ? 1 : (((([i, n].max + 1)..(n + i)).inject(:*)) / (1..[i,n].min).inject(:*) ) }
end
_______________________________
def generate_diagonal(n, l)
  return [] if l == 0

  (1..l).to_a.map { |k|
    (1..n).inject(1) { |rez, i| rez * (k + i - 1) } / (1..(n - 1)).inject(1) { |rez, i| rez * (i + 1) }
  }
end
