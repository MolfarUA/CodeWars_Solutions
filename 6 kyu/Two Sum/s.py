def two_sum(nums, t):
    for i, x in enumerate(nums):
        for j, y in enumerate(nums):
            if i != j and x + y == t:
                return [i, j]
________________________________
def two_sum(nums, target):
    d = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in d:
            return [d[diff], i]
        d[num] = i
________________________________
def two_sum(numbers, target):
    d = {}
    for i,n in enumerate(numbers):
        if target-n in d:
            return [d[target-n],i]
        d[n] = i
________________________________
def two_sum(numbers, target):
    for i in range(0, len(numbers)):
        for x in range(0, len(numbers)):
            if numbers[i] + numbers[x] == target and i != x:
                index1 = i
                index2 = x
                break
    return sorted([index1, index2])
________________________________
def two_sum(numbers, target):
    return [[i, numbers.index(target - numbers[i])] for i in range(len(numbers)) if target - numbers[i] in numbers].pop()
________________________________
def two_sum(numbers, target, dict = {}):  
    for i, n in enumerate(numbers):
        if target - n in dict:
            return [dict[target - n], i]
        dict[n] = i
    
