55b2549a781b5336c0000103


def compare_powers(n1,n2)
  n2[1]*Math.log(n2[0]) <=> n1[1]*Math.log(n1[0])
end
________________________________
def compare_powers((x, a), (y, b))
  b * Math.log(y) <=> a * Math.log(x)
end
________________________________
def compare_powers(n1,n2)

 if n1[1].to_s.length > 6
  n1[1]/=500000
  n2[1]/=500000
 end

  c = (n1[0] ** n1[1]); 
  b = (n2[0] ** n2[1])

  (c == b) ? (0) : (c < b) ? (1) : (-1)
end
________________________________
def compare_powers(n1,n2)
  if n1[0] == 1 && n2[0] == 1
    return 0
  end
  if n1[0] == n2[0]
      return ((n2[1] > n1[1]) ? 1 : (( n2[1] < n1[1] ) ? -1 : 0))
  end
  if n1[1] === n2[1]
    return ((n2[0] > n1[0]) ? 1 : (( n2[0] < n1[0] ) ? -1 : 0))
  end

  p1 = Math.log(n1[0]) * n1[1]
  p2 = Math.log(n2[0]) * n2[1]
  return ((p2 > p1) ? 1 : (( p2 < p1 ) ? -1 : 0))
end
