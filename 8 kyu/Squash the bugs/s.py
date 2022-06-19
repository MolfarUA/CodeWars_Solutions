56f173a35b91399a05000cb7


def find_longest(strng):
    return max(len(a) for a in strng.split())
__________________________
def find_longest(string):
    return max(map(len, string.split()))
__________________________
def find_longest(string):
    spl = string.split(" ")
    longest = 0
    i=0
    while (i < len(spl)):
        print(spl[i])
        if (len(spl[i]) > longest):
            longest = len(spl[i])
        i +=1
    return longest
__________________________
def find_longest(string):
    return max(len(w) for w in string.split())
__________________________
def find_longest(string):
    longest = max(string.split(), key=len)
    longest = len(longest)
    return longest
__________________________
def find_longest(string):
    longest = 0
    for word in string.split(" "):
        longest = max(longest, len(word))
    return longest
__________________________
def find_longest(s):
    len_lst = [len(word) for word in s.split()]
    return max(len_lst)
__________________________
def find_longest(string):
    spl = string.split(" ")
    print(spl)
    longest = 0
    i=0
    while (i < len(spl)):
        if (len(spl[i]) > longest): 
            longest = len(spl[i])
            i += 1
        else:
            i += 1
    return longest
__________________________
def find_longest(string):
    split = string.split(' ')
    return max([len(x) for x in split])
__________________________
def find_longest(string):
    list_of_ints = []
    string = string.split()
    
    for i in string:
        list_of_ints.append(len(i))
    
    return(max(list_of_ints))
