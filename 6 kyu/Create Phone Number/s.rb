def createPhoneNumber(array)
  '(%d%d%d) %d%d%d-%d%d%d%d' % array
end
_______________________________
def create_phone_number(numbers)
  return "(#{numbers.join().to_s[0..2]}) #{numbers.join().to_s[3..5]}-#{numbers.join().to_s[6..9]}"
end
_______________________________
def create_phone_number(numbers)
  "(#{numbers[0..2].join("")})\s#{numbers[3..5].join("")}-#{numbers[6..9].join("")}"
end
_______________________________
def join_digits(num_arr, i, x)
  num_arr.slice(i, x).join
end

def create_phone_number(numbers)  
  "(#{join_digits(numbers, 0, 3)}) #{join_digits(numbers, 3, 3)}-#{join_digits(numbers, 6, 4)}"
end
_______________________________
def create_phone_number(numbers)
  numbers.map!(&:to_s)
  phone_number = '(' + numbers.slice(0, 3).join + ') ' + numbers.slice(3, 3).join + "-" + numbers.slice(6, 4).join
  phone_number
end
_______________________________
def create_phone_number(numbers)
  s = numbers.join('')
  "(#{s[..2]}) #{s[3..5]}-#{s[6..]}"
end
