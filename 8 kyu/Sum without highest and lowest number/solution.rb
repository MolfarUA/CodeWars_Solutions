def sum_array(arr)
  if arr.kind_of?(Array) and arr.length > 2
    arr.inject(:+) - arr.min - arr.max
  else
    0
  end
end
________________________________________
def sum_array(arr)
  return 0 if arr == nil
  arr.length < 3 ? 0 : arr.sort!.inject(0, :+) - arr[0] - arr[-1]
end
________________________________________
def sum_array(arr)
  arr.nil? || arr.empty? ? 0 : arr.sort[1..-2].reduce(0, :+)
end
________________________________________
def sum_array(arr)
  arr ? (arr.size > 2 ? arr.sort[1...-1].inject(:+) : 0) : 0
end
________________________________________
def sum_array(arr)
  if arr == nil || arr == [] || arr.length <=1 then return 0 end
  a = arr.sort()
  a.inject(0){|t,x| t + x } - a[0] - a[-1]
end
