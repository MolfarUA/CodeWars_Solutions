5659c6d896bc135c4c00021e


def next_smaller n
  digits = n.to_s.chars.map{|d| d.to_i }  
  return -1 if n.to_s.size == 1 || digits.sort.join == n.to_s  
  digits.reverse!
  digits.each_with_index do |d,i|
    if digits[i+1] && digits[i+1] > digits[i]                        
      max = digits[0...i+1].select{|a| a<digits[i+1]}.sort.reverse.shift
      arr = digits[0..i+1].sort
      arr.delete_at(arr.index(max))
      arr << max
      arr += digits[i+2..-1]
      smaller = arr.reverse.join.to_i
      return -1 if smaller.to_s.size < digits.size
      return smaller
    end
  end
end
_______________________________
def next_smaller n
  # get the digits used
  digits = n.digits.sort
  
  # generate smallest number, avoiding leading zeros
  if digits[0] == 0
    idx = digits.index(&:nonzero?)
    digits[0], digits[idx] = digits[idx], digits[0]
  end
  smallest = digits.join.to_i
  
  # already the smallest?
  return -1 if n == smallest
  
  # sort the digits again
  digits.sort!
  
  # search for next number
  n -= 9
  n -= 9 until n.digits.sort == digits
  
  return n
end
_______________________________
def next_smaller n
  chars_found = n.to_s.chars.last(8).join
  permut = chars_found.chars.permutation(chars_found.size).to_a.map(&:join).uniq.sort
  index = permut.index(chars_found)
  return -1 if (index-1) < 0
  
  result = n.to_s.sub(chars_found, permut[index - 1]).to_i
  return -1 if result.to_s.size < n.to_s.size
  
  result
end
