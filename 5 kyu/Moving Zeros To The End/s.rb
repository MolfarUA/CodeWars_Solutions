52597aa56021e91c93000cb0


def moveZeros(arr) 
  zeros = arr.count(0)
  arr.delete(0)
  arr.fill(0, arr.size, zeros)
end
_____________________________
def moveZeros(arr) 
  arr.partition { |elem| elem == 0 }.reverse.inject(:+)
end
_____________________________
def moveZeros(arr) 
  arr.partition{_1 != 0}.reduce(&:+)
end
