5a2be17aee1aaefe2a000151


def array_plus_array(arr1, arr2)
  arr1.sum + arr2.sum
end
_________________________
def array_plus_array(a, b)
  (a + b).sum
end
_________________________
def array_plus_array(arr1, arr2)
  sum = 0
  sum += arr1.reduce{|x,y| x+y}
  sum += arr2.reduce{|x,y| x+y}
  sum
end
