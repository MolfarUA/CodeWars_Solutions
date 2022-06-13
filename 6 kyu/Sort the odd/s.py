def sort_array(arr):
  odds = sorted((x for x in arr if x%2 != 0), reverse=True)
  return [x if x%2==0 else odds.pop() for x in arr]
_______________________________________________
def sort_array(source_array):
    odds = iter(sorted(v for v in source_array if v % 2))
    return [next(odds) if i % 2 else i for i in source_array]
_______________________________________________
def sort_array(source_array):

    odds = []
    answer = []
    
    for i in source_array:
        if i % 2 > 0:
            odds.append(i)
            answer.append("X")
            
        else:
            answer.append(i)
            
    odds.sort()
    
    for i in odds:
        x = answer.index("X")
        answer[x] = i
    return answer
_______________________________________________
def sort_array(source_array):
    result = sorted([l for l in source_array if l % 2 == 1])
    for index, item in enumerate(source_array):
        if item % 2 == 0:
            result.insert(index, item)
    return result
_______________________________________________
def sort_array(source_array):
    odd = []
    for i in source_array:
        if i % 2 == 1:
            odd.append(i)
    odd.sort()
    x=0
    for j in range(len(source_array)):
        if source_array[j]%2==1:
            source_array[j]=odd[x]
            x+=1
            
    return source_array
_______________________________________________
def sort_array(source_array):
    result = []
    temp = []
    for number in source_array:
        if number % 2 != 0:
            temp.append(number)
    i = 0
    temp.sort()
    for number in source_array:
        if number % 2 != 0:
            result.append(temp[i])
            i += 1
        else:
            result.append(number)
    return result
_______________________________________________
def sort_array(source_array):
    #return empty list if source is empty
    if not source_array: return []
        
    #extract odd numbers from source array and sort them
    odd_array = [odd for odd in source_array if odd % 2 == 1]
    odd_array.sort()
    
    #extract even number positions from source array
    even_pos_array = [i for i in range(len(source_array)) if source_array[i] % 2 == 0]
    
    #initialize result array same length as source array with ''
    result_array = [''] * len(source_array)
    
    #place the even numbers from source array into result array at original position
    for i in range(len(even_pos_array)):
        result_array[even_pos_array[i]] = source_array[even_pos_array[i]]
    
    #place the odd numbers from odd array into result array at empty positions
    j = 0
    for i in range(len(result_array)):
        if result_array[i] == '':
            result_array[i] = odd_array[j]
            j += 1
            
    return result_array
_______________________________________________
def sort_array(source_array):
    odd_numbers = []
    
    for num in source_array:
        if num % 2 == 1:
            odd_numbers.append(num)
    odd_numbers = sorted(odd_numbers).__iter__()
    for i,num in enumerate(source_array):
        if num % 2 == 1:
            source_array[i] = odd_numbers.__next__()
    return source_array
_______________________________________________
def sort_array(source_array):
    arr = []
    odd = []
    for i, e in enumerate(source_array):
        if e % 2:
            odd.append(e)
        else:
            arr.append((e, i))
    odd = sorted(odd)
    for e, i in arr:
        odd.insert(i, e)
    return odd
_______________________________________________
def sort_array(num_arr):
    num_arr_formated = []
    time_num_arr = []
    i = 0
    for number in num_arr:
            if number%2 != 0:
                time_num_arr.append(number)
                num_arr.insert(i, ' ')
                num_arr.remove(number)
            i += 1
    i = 0
    j = 0
    time_num_arr.sort()
    for character in num_arr:
        if character == ' ':
            num_arr.insert(i, time_num_arr[j])
            num_arr.remove(character)
            j += 1
        i += 1
    return num_arr
_______________________________________________
def sort_array(lst: list[float]) -> list:
  odds = iter(sorted(el for el in lst if el % 2))
  return [next(odds) if el % 2 else el for el in lst]
_______________________________________________
def sort_array(source_array):
    uneven=[]
    position=[]
    for i in range(len(source_array)):
        num=source_array[i]
        if num % 2 != 0:
            uneven.append(num)
            position.append(i)
    uneven.sort()
    array_out=source_array
    for i in range(len(position)):
        array_out[position[i]]=uneven[i]
        
    return(array_out)
_______________________________________________
def sort_array(source_array):
    odd = [x for x in source_array if x%2==1]
    odd.sort()
    new = []
    for i, x in enumerate(source_array):
        if x%2==0:
            new.append(x)
        else:
            new.append(odd.pop(0))
    return new
_______________________________________________
def sort_array(source_array):
    arrayEven = []
    arrayOdd = []
    indexOdd = []
    indexCounter = 0
    for i in source_array:
        if i % 2 != 0:
            arrayOdd.append(i)
            indexOdd.append(indexCounter)
        else:
            arrayEven.append(i)
        indexCounter += 1
    arrayOdd.sort()
    indexCounter = 0
    for i in arrayOdd:
        arrayEven.insert(indexOdd[indexCounter], i)
        indexCounter += 1
    return arrayEven
_______________________________________________
def sort_array(source_array):
    sort = sorted([i for i in source_array if i%2!=0])
    counter = 0
    for i in range(len(source_array)):
        if source_array[i]%2!=0:
            source_array[i] = sort[counter]
            counter += 1
    return source_array
_______________________________________________
def sort_array(source_array):
    u = [c for c in source_array if c%2 == 1]
    u.sort(reverse=True)
    return [c if c%2 == 0 else u.pop() for c in source_array]
