5659c6d896bc135c4c00021e


def next_smaller(n):
    s = list(str(n))
    i = j = len(s) - 1
    while i > 0 and s[i - 1] <= s[i]: i -= 1
    if i <= 0: return -1
    while s[j] >= s[i - 1]: j -= 1
    s[i - 1], s[j] = s[j], s[i - 1]
    s[i:] = reversed(s[i:])
    if s[0] == '0': return -1
    return int(''.join(s))
_______________________________
def next_smaller(n):
    
    ## Create a list of each digit in n
    numbers = [int(i) for i in str(n)]

    ## Loop over each digit in the numbers list, from right to left
    for i in range(len(numbers) - 1, 0, -1):
    
        ## If a number is less than the number to its left, split into 2 lists
        if numbers[i] < numbers[i -1]:
            rearrange_list = numbers[i - 1:]  ## numbers on the right of i -1
            original_list = numbers[:i - 1]   ## numbers on the left of i -1
            less_than_values = []             ## will contain possible substitutions for i -1
            
            ## Loop over the rearrange_list
            for i in rearrange_list:
            
                ## if the number is smaller than i, append it to less_than_values
                if i < rearrange_list[0]:
                    less_than_values.append(i)
    
            ## Add the max value from less_than_values to the end of the original_list, 
            ## then add the rest of the sorted values from rearrange_list to the original_list
            original_list.append(max(less_than_values))
            rearrange_list.remove(max(less_than_values))
            original_list += sorted(rearrange_list, reverse=True)
            
            ## Join the list together to get the output
            output = int(''.join([str(num) for num in original_list]))

            ## If the output starts with 0, return -1. Otherwise, return the ouput.
            if len(str(output)) < len(str(n)):
                return -1
            else:
                return output
    
    ## Return -1 if n is None, or if there are no smaller numbers
    return -1            
_______________________________
def swap(s, a, b):
    s = list(s)
    s[a], s[b] = s[b], s[a]
    return ''.join(s)
    
def maximized_range(s, left): # Maximize value in range [left, end]
    return s[:left] + ''.join(sorted(s[left:], reverse=True))

def next_smaller(n):
    s = str(n)
    k = len(s)
    for i in range(k-1, -1, -1):
        for j in range(k-1, i, -1):
            if s[j] < s[i]:
                t = swap(s, i, j)
                if t[0] != '0':
                    return int(maximized_range(t, i+1))
    return -1
_______________________________
def next_smaller(n):
    s = str(n)
    i = next((i for i in range(len(s)-1,0,-1) if s[i-1]>s[i]),len(s))
    j = next((j for j in range(len(s)-1,i-1,-1) if s[i-1]>s[j]),-1)
    s = s[:i-1]+s[j]+(s[i:j]+s[i-1]+s[j+1:])[::-1]
    return [int(s),-1][s[0]=='0' or j<0]
_______________________________
def next_smaller(n):
    s = list(str(n))
    for i in range(len(s)-2,-1,-1):
        
        if s[i] > s[i+1]:
            t = s[i:]
            m = max(filter(lambda x: x<t[0], t))
            t.remove(m)
            t.sort(reverse=True)
            s[i:] = [m] + t
            if int(s[0]) != 0:
                return int("".join(s))
            
    return -1
_______________________________
import itertools
def next_smaller(n):
    print(n)
    a=list(str(n))
    b=len(a)
    if b==1:
        return -1
    for j in range(b-2,-1,-1):
        if a[j] > a[j+1]:         
            t=a[j:]
            m=max(filter(lambda x:x<t[0],t))
            t.remove(m)
            c=[]
            while len(t)>0:
                d=max(t)
                c.append(d)
                t.remove(d)
            a[j:]=[m]+c
            if a[0]=='0':
                return -1
            return int(''.join(a))
    return -1
_______________________________
import itertools

def next_smaller(n):
    print(n)
    number_list = [int(d) for d in str(n)]
    if(len(set(number_list))==1):
        return -1
    
    min_digit = 9
    replacer_index = 0
    replacement_index = 0
    
    replacement_possible = False
    for i in range(len(number_list)-1, 0, -1):
        if number_list[i] < number_list[i-1]:
            replacement_possible = True
    if replacement_possible == False:
        return -1
    
    for i in range(len(number_list)-1, -1, -1):
        print(number_list[i])
        if number_list[i] >= number_list [i-1]:
            continue
        else:
            index = i-1
            print("index: ", index)
            maximum = number_list[index]
            print("Maximum: ", maximum)
            print(number_list)
            break
        
        return -1
    
    if index > 0:
        temp = number_list[index:]
    else:
        temp = number_list
    print("temp: ", temp)
    print("maximum: ", maximum)
    best_min = 0
    replacer = temp[0]
    for number in temp:
        print(number)
        if number < maximum and number >= best_min:
            replacer = number
            best_min = number
    print("replacer= ", replacer)
    temp.remove(replacer)
    print("temp: ", temp)
    temp.sort(reverse = True)
    print("temp_sorted: ", temp)
    temp.insert(0, replacer)
    print(temp)
    
    if index != 0:
        for number in reversed(number_list[0:index]):
            temp.insert(0, number)
    #number_list =[]
    #for number in temp:
    #    number_list.append(number)
    #print(number_list)
    #if number_list[0] == min(number_list):
    #    number_list.insert(number_list.pop(0), 1)
    #number_list[replacement_index], number_list[replacer_index] = number_list[replacer_index], number_list[replacement_index]
            
    

    s = [str(integer) for integer in temp]
    a_string = "".join(s)
    number = int(a_string)
    
    if len(str(number)) != len(str(n)):
        return -1
    return number
_______________________________
def next_smaller(number):
    number = [int(x) for x in str(number)]
    lenght = len(number)
    if lenght == 1:
        return -1
    i = -2
    while True:
        if number[i] > number[i+1]:
            break 
        else:
            i -= 1
            if -i > len(number):
                return -1
    
    
    n = number[i:]
    for y in range(1, number[i] + 1):
        if (number[i] - y) in n:
            x = (number[i]-y)
            number[i] = x
            n.remove(x)
            break
    n.sort(reverse = True)
    number[i+1:] = n
    
    number = int(''.join([str(x) for x in number]))
    if len(str(number)) != lenght:
        return -1
    return number
_______________________________
def swap(lst, X, Y):
    x = lst[X]
    y = lst[Y]
    lst[X] = y
    lst[Y] = x

def next_smaller(n):
    lst = list(str(n))
    X = 0
    for i in range(len(lst)-2, -1, -1):
        if lst[i] > lst[i+1]:
            X = i
            break
    Y = 0
    m = -1
    slst = lst[X+1:]
    for i in range(len(slst)):
        if int(slst[i]) > m and slst[i] < lst[X]:
            Y = X+i+1
    swap(lst, X, Y)
    fhalf = lst[:X+1]
    shalf = sorted(lst[X+1:])
    shalf.reverse()
    ret = int("".join(fhalf + shalf))
    if len(list(str(ret))) < len(lst): return -1
    if ret == n: return -1
    if ret > n:
        return -1
    return ret
_______________________________
def next_smaller(n):
    
    
    num = list(str(n))
    
    if len(num) == 1:
        return -1
    n = 0
    while True:
        if num[-1-n] >= num[-2-n]:
            n += 1
        else:
            break
        if n == len(num) - 1:
                return -1    
    change = num[-2-n:]
    old = num[:-2-n]
    
    diff = []
    for number in change:
        if number < change[0]:
            diff.append(number)
    
    if diff == []:
        change = change.reverse()
    else:
        head = change.pop(change.index(max(diff)))

        change.sort(reverse= True)
        change.insert(0,head)
        
    n = old + change
    
    string = ""
    for i in n:
        string = string + i
        
    if len(str(int(string))) != len(n):
        return -1
    return int(string)
