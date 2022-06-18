def find_even_index(arr)
  (0...arr.size).find {|i|arr[0...i].sum == arr[(i+1)...arr.size].sum} || -1
end
________________________
def find_even_index(arr)
  (0...arr.size).each do |i|
    if arr[0...i].sum == arr[i + 1..-1].sum
      return i
    end
  end
  -1
end
________________________
def find_even_index(arr)
  (0..arr.size-1)
  .find(-1) {|n| arr.first(n).sum == arr.skip(n + 1).sum}
end
________________________
def find_even_index(arr)
  v = arr[0]; i = l = 0; r = arr[1..-1].sum
  while i < arr.size
    return i if l == r
    l += v
    r -=(v = arr[i += 1]? || 0)
  end || -1
end
________________________
def find_even_index(arr)
  (0..arr.size-1).each do |i|
    return i if arr.reverse.skip(arr.size-i).sum == arr.skip(i+1).sum
  end
  -1
end
