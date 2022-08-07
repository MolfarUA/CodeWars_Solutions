57cfdf34902f6ba3d300001e


def two_sort(s)
  s.min.chars.join('***')
end
___________________________
def two_sort(s)
  s.sort.first.chars.join('***')
end
___________________________
def two_sort(s)
  s.sort[0].chars.join("***")
end
___________________________
def two_sort(s)
str = s.sort  
arr =[ ] 
str[0].each_char.with_index do |char ,idx|
 arr << char
if idx != (str[0].length) -1 
  arr << "***"
end
 end 
 arr.join
end
___________________________
def two_sort(arr)
 arr.sort![0].split("").join("***")
end
