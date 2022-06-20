58cb43f4256836ed95000f97


def find_difference(a, b)
  (a.product - b.product).abs
end
________________________
def find_difference(a, b)
  volume_a = 1
  volume_b = 1
  a.each do |e|
    volume_a = volume_a * e end
  b.each do |e|
    volume_b = volume_b * e end
  (volume_a - volume_b).abs
end
________________________
def find_difference(a, b) 
  diff = a[0] * a[1] * a[2] - b[0] * b[1] * b[2];
  if diff < 0 
    delta = -diff
  else
    delta = diff
  end
  delta
end
