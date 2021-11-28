import unittest

def opposite (number):
    return number * -1

class TestOpposite (unittest.TestCase):
    
    def test_opposite (self):
        self.assertEqual (opposite (1), -1)

if __name__ == '__main__':
    unittest.main()
###################
def opposite(number):
    return -number
###############
from operator import neg as opposite
#############
def opposite(number):
  return number * -1
#############
opposite = lambda x: -x
#############
def opposite(number):
    """
    Function have one required argument.
    At start our function check your number. If it's int, float or complex - func multiplies number by -1 and return it
    If our argument is string, try to convert to complex number
    If we had Value Error in our convertation, say(use print when except):
        Input data cannot be represented as a number.
    And after return None

    Return:
        Number int or float if input number is int or float.
        Number complex if input number is complex or wrote in string
        None if we had empty line or another input types
    """
    if (type(number) is int) or (type(number) is float) or (type(number) is complex):
        number = number * -1
        return number
    else:
        try:
            number = complex(number) * -1
            return number
        except ValueError:
            print("Input data cannot be represented as a number")
            return None
########################
opposite=lambda n:-n
################
def opposite(n): return -n
################
def opposite(number):
  import re
  m = re.match("-", str(number))
  if m:
     number = re.sub("-", "", str(number))
  else:
     number = "-" + str(number)
  try:
    return int(number)
  except ValueError:
    return float(number)
##################
def opposite(number):
  return abs(number) if number < 0 else 0 - number
##################
def opposite(number):
  # your solution here
  numbers=str(number)
  if isinstance(number, int):
      if numbers[0]=="-":
          negatives=numbers[1:]
          negative=int(negatives)
          return negative
      else:
          positives="-"+numbers
          positive=int(positives)
          return positive
  if isinstance(number, float):
      if numbers[0]=="-":
          negatives=numbers[1:]
          negative=float(negatives)
          return negative
      else:
          positives="-"+numbers
          positive=float(positives)
          return positive
##################
opposite=(0.).__sub__
################
def opposite(number):
  return float(('-' + str(number)).replace('--', ''))
################
def opposite(number):
    return (~int(number) + int(number)) * number
###################
def opposite(number):
  return(number*(-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1))
#################
opposite = lambda l: -l
###############
def opposite(number):
  return number - (number * 2)
###############
def opposite(number):
    
    return(number - number * 2)

o_number = opposite(9)
print(o_number)
