5a2be17aee1aaefe2a000151


def array_plus_array(arr1, arr2)
  (arr1 + arr2).reduce(:+)
end
_________________________
def array_plus_array(arr1, arr2)
  (arr1 + arr2).sum
end
_________________________
def array_plus_array(arr1, arr2)
  (arr1 + arr2).inject(0, :+)
end
_________________________
def array_plus_array(*a)
  a.sum(&:sum)
end
