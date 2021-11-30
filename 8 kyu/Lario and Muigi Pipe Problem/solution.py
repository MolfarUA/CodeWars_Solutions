def pipe_fix (nums):
    minimum = min (nums)
    maximum = max (nums)
    
    nums = [i for i in range (minimum, maximum + 1)]
    
    return nums
#############
def pipe_fix(nums):
    return list(range(nums[0], nums[-1] + 1))
##############
def pipe_fix(num):
    return range(min(num), max(num)+1)
###########
def pipe_fix(l):
    return [x for x in range(min(l), max(l)+1)]
############
pipe_fix = lambda l: list(range(min(l),max(l)+1))
###########
def pipe_fix(ls):
    return range(min(ls), max(ls)+1)
############
def pipe_fix(arr):
    ls = []
    for i in range(arr[0],arr[len(arr)-1]+1):
        ls.append(i)
    return ls
############
def pipe_fix(numbers):
    length = len(numbers) - 1
    y = []
    x = numbers[0]
    while x <= numbers[length]:
        y.append(x)
        x += 1
    return y
############
def pipe_fix(nums):
    return [*range(nums[0],nums[-1]+1)]
###########
def pipe_fix(input):
  first_element = input[0]
  last_element = input[-1]
  result = []
  while last_element >= first_element:
    result.append(first_element)
    first_element += 1
  return result
############
pipe_fix = lambda initPipeConnection: list(range(initPipeConnection[0], initPipeConnection[-1] + 1))
###########
def pipe_fix(numbers):
    return list(range(min(numbers), max(numbers) + 1))
###########
def pipe_fix(ar):
    ar.sort()
    return [x for x in range(ar[0], ar[-1] + 1)]
#############
def pipe_fix(nums):
    highest_number = sorted(nums, reverse=True)[0:1]
    lowest_number = sorted(nums)[0:1]
    for integer in lowest_number:
        lowest_number = integer
    for integer in highest_number:
        highest_number = integer
    return [x for x in range(lowest_number, highest_number + 1)]
