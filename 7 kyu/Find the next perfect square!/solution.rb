def find_next_square(sq)
  # Return the next square if sq is a perfect square, -1 otherwise
  number = Math.sqrt(sq) + 1
  number % 1 == 0 ? number**2 : -1
end

_____________________________________
def find_next_square(sq)
  # Return the next square if sq is a perfect square, -1 otherwise
  sqrt = Math.sqrt(sq)
  sqrt % 1 == 0 ? (sqrt + 1)**2 : -1
end

_____________________________________
def find_next_square(sq)
  is_square = -> (n) { Math.sqrt(n) % 1 == 0 }
  is_square.call(sq) ? (Math.sqrt(sq) + 1) ** 2 : -1
end

_____________________________________
def find_next_square(num)
  return -1 unless perfect_square?(num)
  (Math::sqrt(num) + 1 )**2
end

def perfect_square?(num)
  Math::sqrt(num) % 1 == 0
end

_____________________________________
def find_next_square(sq)
  Math.sqrt(sq).floor**2==sq ? (Math.sqrt(sq)+1)**2 : -1
end

_____________________________________
def find_next_square(sq)  
  nextSquare = (Math.sqrt(sq) + 1) ** 2
  return -1 if nextSquare % 1 != 0
  nextSquare
end

_____________________________________
def find_next_square(sq)
  # Return the next square if sq is a perfect square, -1 otherwise
  sq**0.5 %1 == 0 ? (sq**0.5+1)**2 : -1
end
