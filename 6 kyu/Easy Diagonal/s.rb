559b8e46fa060b2c6a0000bf


def diagonal(n, p)
  row = [1]
  (p + 2).times{ |i| row << (row[i] * (n - i) / (i + 1)) }
  row[p] + row[p + 1]
end
_____________________________
def diagonal(n, p)
  (n-p+1..n+1).reduce(:*)/(1..p+1).reduce(:*)
end
_____________________________
def diagonal(n, p)
  (0..p).reduce(1){|c, k| c*(n+1-k)/(k+1)}
end
