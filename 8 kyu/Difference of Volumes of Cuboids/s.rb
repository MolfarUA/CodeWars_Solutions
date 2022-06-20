58cb43f4256836ed95000f97


def find_difference(a, b)
  (a.inject(:*) - b.inject(:*)).abs
end
________________________
def find_difference(a, b)
  ((a).reduce(:*) - (b).reduce(:*)).abs
end
________________________
def find_difference(a, b)
  (a[0]*a[1]*a[2] - b[0]*b[1]*b[2]).abs
end
