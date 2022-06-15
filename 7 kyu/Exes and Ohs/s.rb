def XO(str)
  str.downcase.count('x') == str.downcase.count('o')
end
__________________________________
def XO(str)
  str.downcase!
  str.count('o') == str.count('x')
end
__________________________________
def XO(str)
  str.count('Xx') == str.count('oO')
end
__________________________________
def XO(str)
  str.count('xX') == str.count('oO')
end
__________________________________
def XO(str)
  str.scan(/o/i).count == str.scan(/x/i).count
end
__________________________________
# i: string
#    any char
# o: boolean
#    true if count of 'x' and count of 'o' are the sime
#        case-insensitive
#    if no 'x' or 'x', return true
# e: see below
# d: string => array => Integer => boolean
# a:
#    split the string into an array
#    create a counter for 'x' and 'o' = 0
#    loop over the array and count the 'x' and 'o' appearances
#    increment the 'x' and 'o' counters accordingly
#    check if counters are equal
# c:

def XO(str)
  x_count = 0
  o_count = 0
  str.chars.each do |char|
    case char.downcase
    when 'x' then x_count += 1
    when 'o' then o_count += 1
    end
  end
  x_count == o_count
end
