5b71af678adeae41df00008c


def shortest_distance(a, b, c)
  a, b, c = [a, b, c].sort
  Math.hypot(c, a+b)
end
____________________________
def shortest_distance(a, b, c)
  [((a+b)**2+c**2)**0.5,((a+c)**2+b**2)**0.5,((b+c)**2+a**2)**0.5].min
end
____________________________
def shortest_distance(a, b, c)
  [Math.sqrt(a*a + (b + c) ** 2), Math.sqrt(b*b + (a + c) ** 2), Math.sqrt(c*c + (b + a) ** 2)].min
end
____________________________
def shortest_distance(a, b, c)
   [
      Math.sqrt(a**2 + (b+c) * (b+c)),
      Math.sqrt(b**2 + (a+c) * (a+c)),
      Math.sqrt(c**2 + (a+b) * (a+b))
    ].min
end
