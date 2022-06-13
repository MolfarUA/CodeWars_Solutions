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
________________________________
def two_sum(n, t):
    res = []
    for i_1 in n:
        i_2 = t - i_1
        if i_2 in n:
            if i_1 == i_2 == 2:
                return [0,1]
            res.append(n.index(i_1))
            res.append(n.index(i_2))
            break
    return res
________________________________
def two_sum(n, t):
    i = 0
    for n1 in n:
        n2 = t-n1
        if n2 in n and i!=n.index(n2):
            return [i,n.index(n2)]
        i = i + 1
________________________________
def two_sum(numbers, target):
    props = []
    for x,y in enumerate(numbers):
        remainder = target - y
        if not props and remainder > 0:
            props.append(x)
            if remainder in numbers:
                if x == numbers.index(remainder):
                    props.append(x+1)
                else:
                    props.append(numbers.index(remainder))
                return props
        else:
            if remainder == 0:
                props.append(x)
            else:
                props = []
    return props
________________________________
def two_sum(numbers, target):
    list = []
    for num in (numbers):
        for next_num in numbers:
            if target == num + next_num:
                list.append(numbers.index(num))
                list.append(numbers.index(next_num))
                if num == next_num:
                    list = []
                    x = numbers.index(num)
                    list.append(x)
                    list.append(numbers.index(next_num, x+1))

                return list
________________________________
def two_sum(arr, target):
    for i in range(0,len(arr)-1):
        for j in range(i+1,len(arr)):
            if(arr[i]+arr[j] == target):
                return sorted([i,j])
    return []
________________________________
def two_sum(numbers, target):
    numbers.sort(reverse=True)
    for number in numbers:
        target_list = target- number
        numbers.sort()
        try: 
            first = numbers.index(target_list)
            numbers.pop(first)
            second = numbers.index(number) + 1
            return [first, second]
        except ValueError:
            continue
