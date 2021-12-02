def remove_smallest(numbers):
    return [v for i,v in enumerate(numbers) if i != numbers.index(min(numbers))]
print(remove_smallest([1,1,2,2,1]))
###############
def remove_smallest(numbers):
    num = numbers.copy()
    if len(num) != 0:
        num.remove(min(num))
        return num
    else: return []
#############
def remove_smallest(numbers):
    numbers_new = numbers.copy()
    if len(numbers) > 0:
        numbers_new.remove(min(numbers))
    return numbers_new
#############
def remove_smallest(numbers):
    if not numbers:
        return []
    else:
        new = numbers[:]
        smallest = min(new)
        pos = new.index(smallest)
        new.pop(pos)
        return new
##############
def remove_smallest(numbers):
    if len(numbers) <= 1:
        return []
    elif len(numbers) >= 1:
        del numbers[numbers.index(min(numbers))]
        return numbers
################
def remove_smallest(numbers):
    if numbers:
        result = numbers.copy()
        result.remove(min(result))
        return result
    else:
        return numbers
#############
def remove_smallest(numbers):
    try:
        a=numbers.index(min(numbers))
        return numbers[:a] + numbers[a+1:]
    except:
        return numbers
###############
def remove_smallest(numbers):
    ans = numbers.copy()
    if ans:
        ans.remove(min(numbers))
    return ans
################
def remove_smallest(numbers):
    if not numbers:
        return []
    
    new = numbers[:]
    idx = numbers.index(min(numbers))
    new.pop(idx)
    
    return new
################
def remove_smallest(numbers):
    if numbers == []:
        return []
    else:
        x = numbers.copy()
        x.remove(min(numbers))
        return x
###############
def remove_smallest(numbers):
    l= [i for i in numbers]
    if l ==[]:
        return []
    else:
        l.remove(min(l))
    return l
###############
def remove_smallest(numbers):
    if numbers == []:
        return []
    new_list = numbers.copy()
    min = 400
    for i in numbers:
        if i < min:
            min = i
    new_list.remove(min)
    return new_list
###############
def remove_smallest(numbers):
    if len(numbers) <= 0:
        return []
    min_value = min(numbers)
    i = numbers.index(min_value)
    new_list = numbers.copy()
    new_list.pop(i)
    return new_list
###############
def remove_smallest(numbers):
    numbersNew = [n for n in numbers]
    if len(numbersNew) == 0:
        return []
    index = 0
    tmp = numbersNew[0]
    for i in range(len(numbersNew)):
        if numbersNew[i] < tmp:
            tmp = numbersNew[i]
            index = i
    del numbersNew[index]
    return numbersNew
##################
import copy
def remove_smallest(numbers):
    if len(numbers) >= 1:
        smallest = min(numbers)

        indexSmallest = numbers.index(smallest)
        newList = []
        newList = copy.deepcopy(numbers)
        del newList[indexSmallest]

        return newList
    else:
        newList = []
        newList = copy.deepcopy(numbers)
        return newList
##############
def remove_smallest(numbers):
    if not numbers:
        return []
    result=numbers.copy()
    mini=min(numbers)
    for i in result:
        if i==mini:
            result.remove(i)
            return result
###############
def remove_smallest(numbers):
    new_list = numbers.copy()
    try:
        new_list.remove(min(new_list))
    except ValueError:
        pass
    finally:
        return new_list
###############
def remove_smallest(numbers):
    if numbers == []:
        return numbers
    m = min(numbers)
    c = list(numbers)
    i = c.index(m)
    c.pop(i)
    return c    
    raise NotImplementedError("TODO: remove_smallest")
