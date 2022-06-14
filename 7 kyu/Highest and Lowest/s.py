def high_and_low(numbers): #z.
    nn = [int(s) for s in numbers.split(" ")]
    return "%i %i" % (max(nn),min(nn))
______________________________
def high_and_low(numbers):
    nums = sorted(numbers.split(), key=int)
    return '{} {}'.format(nums[-1], nums[0])
______________________________
def high_and_low(numbers):
  return " ".join(x(numbers.split(), key=int) for x in (max, min))
______________________________
def high_and_low(numbers):
  numbers = [int(c) for c in numbers.split(' ')]
  return f"{max(numbers)} {min(numbers)}"
______________________________
def high_and_low(numbers):
    numbers = [int(x) for x in numbers.split(" ")]
    return str(max(numbers)) + " " + str(min(numbers))
______________________________
def high_and_low(numbers):
    numbers_list = numbers.split(' ')
    numbers_list = list(map(int, numbers_list))
    print(numbers_list)
    max_num = max(numbers_list)
    min_num = min(numbers_list)
    return str(max_num) + ' ' + str(min_num)
______________________________
def high_and_low(numbers):
    # ...

    num = ""
    ints = []
    for i in range(0, len(numbers)):
        print(num)
        if i == len(numbers) - 1:
            num = num + numbers[i]
            ints.append(int(num))
        if numbers[i] == " ":
            ints.append(int(num))
            num = ""
        else:
            num = num + numbers[i]
    
    high = ints[0]
    low = ints[0]
    for i in ints:
        if i > high:
            high = i
        if i < low:
            low = i
        
    return "{} {}".format(str(high), str(low))
______________________________
def high_and_low(numbers):
    temp = numbers.split(" ")
    temp = [int(i) for i in temp]
    return str(max(temp)) + " " + str(min(temp))
______________________________
import math

def high_and_low(numbers: str) -> str:
    maximum = -math.inf
    minimum = math.inf
    for n in (int(m) for m in numbers.split(' ')):
        if n < minimum:
            minimum = n
        if n > maximum:
            maximum = n
    return str(maximum) + ' ' + str(minimum)
______________________________
def high_and_low(numbers):
    num_list_int = [int(i) for i in numbers.split()]
    return(str(max(num_list_int)))+" "+str(min(num_list_int))
______________________________
def high_and_low(numbers):
    # ...
    numbers = numbers.split(" ")
    numbers = [int(i) for i in numbers]
    # searching for highest number, start from 0
    highest = float('-inf')
    # searching for lowest number, start from max int
    lowest = float('inf')
    for number in numbers:
        lowest = lowest if lowest < number else number
        highest = highest if highest > number else number
    
    return "{} {}".format(highest, lowest)
