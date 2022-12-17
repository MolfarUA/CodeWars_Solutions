56a1c074f87bc2201200002e


def smaller(arr)
  arr.map.with_index(1) { |e, i| arr[i..-1].count { |n| e > n } }
end
____________________________
def smaller(arr)
  arr.map.with_index{|n,i|arr.drop(i).count{|m|m<n}}
end
____________________________
def smaller(arr)
  arr.map.with_index {|n, i| arr[i, arr.size].count {|v| n > v }}
end
