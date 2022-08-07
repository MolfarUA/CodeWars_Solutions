54cb771c9b30e8b5250011d4


def height(n, k)
  a, b = 0, 1
  (1..n).each do |i|
    b = b * (k - i + 1) / i
    a += b
  end
  a
end
_________________________
def height n, k
  f = 1
  n.times.reduce(0){|y,i|y+(f=f*(k-i)/(i+1))}
end
_________________________
def height(n, k)
  c, s = 1, 0
  for i in 0...n
    c = c * (k - i) / (i + 1)
    s += c
  end
  s
end
_________________________
def height n, m
    2.pow(m) - 1 - (n < m ? sum_c(m,m-n-1) : 0)
end

def sum_c n, d
    s = [1]
    (1..d).each{|k| s << s[-1] * (n - k + 1) / k} if d != 0
    s.sum
end
