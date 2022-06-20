5ab6538b379d20ad880000ab


def area_or_perimeter(a , b)
  a == b ? a * b : 2 * (a + b)
end
________________________
def area_or_perimeter(length , width)
 measurement = 0 
  if length == width
    then measurement = (length * width)
  else
    measurement = (length * 2) + (width * 2)
  end
    end
________________________
def area_or_perimeter(l , w)
  if l == w
    return l * w
  elsif l != w
    return 2 * l + 2 * w
  end
end
