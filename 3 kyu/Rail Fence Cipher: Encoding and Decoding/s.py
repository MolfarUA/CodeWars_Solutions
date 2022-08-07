58c5577d61aefcf3ff000081


from itertools import chain

def fencer(what, n):
    lst = [[] for _ in range(n)]
    x,dx = 0,1
    for c in what:
        lst[x].append(c)
        if x==n-1 and dx>0 or x==0 and dx<0: dx *= -1
        x += dx
    return chain.from_iterable(lst)
    

def encode_rail_fence_cipher(s, n): return ''.join(fencer(s,n))
    
def decode_rail_fence_cipher(s, n):
    lst = ['']*len(s)
    for c,i in zip(s, fencer(range(len(s)), n)):
        lst[i] = c
    return ''.join(lst)
_____________________________
from itertools import cycle


def rail_pattern(n):
    r = list(range(n))
    return cycle(r + r[-2:0:-1])


def encode_rail_fence_cipher(string, n):
    p = rail_pattern(n)
    
    return ''.join(sorted(string, key=lambda i: next(p)))


def decode_rail_fence_cipher(string, n):
    p = rail_pattern(n)
    indexes = sorted(range(len(string)), key=lambda i: next(p))
    result = [''] * len(string)
    for i, c in zip(indexes, string):
        result[i] = c

    return ''.join(result)
_____________________________
from itertools import zip_longest

def idxs(m, n):
    s = (n-1) * 2
    yield from range(0, m, s)
    for k in range(1, n-1):
        for i, j in zip_longest(range(k, m, s), range(s-k, m, s)):
            yield i
            if j is not None:
                yield j
    yield from range(n-1, m, s)

def encode_rail_fence_cipher(s, n):
    return ''.join(s[i] for i in idxs(len(s), n))

def decode_rail_fence_cipher(s, n):
    return ''.join(c for _, c in sorted(zip(idxs(len(s), n), s)))
_____________________________
def encode_rail_fence_cipher(s, n):
    return ''.join([s[rv] for rv,i in rails(n, len(s))]) if n>1 else s
    
def decode_rail_fence_cipher(s, n):
    return ''.join([s[i] for rv,i in sorted(rails(n, len(s)), key=lambda e:e[0])]) if n>1 else s

def rails(rn, ln):
    i = -1
    for rc in range(rn):
        rv, rd = rc, rc
        while rv < ln:
            yield (rv, i := i + 1)
            rv += 2 * (rn - 1 - (0 if rn == rd + 1 else rd))
            rd = rn - 1 - rd
_____________________________
def encode_rail_fence_cipher(string, n):
    ans = [[] for x in range(n)]
    i = 0
    is_stopped = False
    
    for x in string:
        ans[i].append(x)
        if i == (n-1):
            is_stopped = True
        
        if is_stopped == True:
            i -= 1
        
        if is_stopped == False:
            i += 1
        
        if i == 0:
            is_stopped = False
        
    cipher = ""
    for x in ans:
        for y in x:
            cipher += y
    
    return cipher
    
def decode_rail_fence_cipher(string, n):
    ans = [[0 for x in range(len(string))] for x in range(n)]
    
    row = 0
    col = 0
    is_stopped = False
    
    for x in string:
        ans[row][col] = x
    
        if row == (n-1):
            is_stopped = True
        
        if is_stopped == True:
            row -= 1
            col += 1
        
        if is_stopped == False:
            row += 1
            col += 1
        
        if row == 0:
            is_stopped = False
    
    index = 0
    for row in range(len(ans)):
        for col in range(len(ans[row])):
            if ans[row][col] != 0:
                ans[row][col] = string[index]
                index += 1
            else:
                ans[row][col] = ans[row][col]
    
    row = 0
    col = 0
    is_stopped = False
    
    decryption = ""
    for x in range(len(string)):
        decryption += ans[row][col]
        
        if row == (n-1):
            is_stopped = True
        
        if is_stopped == True:
            row -= 1
            col += 1
        
        if is_stopped == False:
            row += 1
            col += 1
        
        if row == 0:
            is_stopped = False
    
    return decryption
_____________________________
from itertools import tee, zip_longest

def encode_rail_fence_cipher(string, n):
    res = [[] for _ in range(n)]
    res += res[-2:0:-1]
    for t in zip_longest(*[iter(string)]*len(res), fillvalue=""):
        for a, b in zip(res, t):
            a.append(b)
    return "".join("".join(v) for v in res[:n])      
    
def decode_rail_fence_cipher(string, n):
    res = [[] for _ in range(n)]
    res += res[-2:0:-1]
    for t in zip_longest(*[iter(range(len(string)))]*len(res)):
        for a, b in zip(res, t):
            if b is None: break
            a.append(b)
    return "".join(v[1] for v in sorted(zip(sum(res, []), string)))
_____________________________
def encode_rail_fence_cipher(string, n):
    if not string:
        return ""
    rail_idx = (list(range(n-1)) + list(range(n-1, 0, -1))) * (len(string) // (2*n-2) + 1)
    return "".join(e[2] for e in sorted(zip(rail_idx, range(len(string)), string)))

def decode_rail_fence_cipher(string, n):
    if not string:
        return ""
    rail_idx = (list(range(n-1)) + list(range(n-1, 0, -1))) * (len(string) // (2*n-2) + 1)
    _, sorted_idx = zip(*sorted(zip(rail_idx, range(len(string)))))
    return "".join(e[1] for e in sorted(zip(sorted_idx, string)))
_____________________________
def encode_rail_fence_cipher(string, n):
    x = n - 1
    d = 0
    nexxt = 0
    result = ""
    mySlice = []
    counter = -1
    for v in string:
        counter = counter + 1
        if int(counter/x)%2 == 0:
            d = 1
        else:
            d = -1
        mySlice.append((nexxt, counter))
        nexxt = nexxt + d
    for i in range(n):
        for row, pos in mySlice:
            if row == i:
                result += string[pos]
    return result

def decode_rail_fence_cipher(string, n):
    x = n - 1
    d = 0
    nexxt = 0
    result = ""
    mySlice = []
    counter = -1
    anotherCounter = 0
    decrypted = []
    anotherList = []
    for v in string:
        counter = counter + 1
        if int(counter/x)%2 == 0:
            d = 1
        else:
            d = -1
        mySlice.append((nexxt, counter))
        nexxt = nexxt + d
    for i in range(n):
        for row, pos in mySlice:
            if int(row) == int(i):
                decrypted.append(pos)
    for i in decrypted:
                anotherList.append((i, anotherCounter))
                anotherCounter += 1
    anotherList.sort()
    for i, v in anotherList:
        result += string[v]
    return result
_____________________________
def encode_rail_fence_cipher(string, n):
    encoded = []
    
    for i in range(n+1):
        encoded.append('')
    
    count = -1
    
    for i in range(len(string)):
        if i % (n-1) == 0:
            count += 1
        if count % 2 == 0:
            encoded[i%(n-1)] += string[i]
        else:
            encoded[n-1 - i%(n-1)] += string[i]
        
    return ''.join(encoded)
            
def decode_rail_fence_cipher(string, n):
    decoded = []
    lengths = []

    len_edges = len(string) // (2 * n - 2)
    len_middle = len_edges * 2

    balance = len(string) % (2 * n - 2)

    for i in range(n):
        if i == 0 or i == n - 1:
            lengths.append(len_edges)
        else:
            lengths.append(len_middle)
    
    if 0 < balance <= n:
        count = balance
        index = 0
        while count > 0:
            lengths[index] += 1
            index += 1
            count -= 1
    elif balance > n:
        count = balance
        index = 0
        while index < n:
            lengths[index] += 1
            index += 1
            count -= 1
        index = n - 2
        while count > 0:
            lengths[index] += 1
            index -= 1
            count -= 1

    str = string

    for i in lengths:
        decoded.append(str[:i])
        str = str[i:]

    decoded_phrase = ''

    count = -1
    index = 0
    int_index_start = -1
    int_index_end = -1
    int_index_middle = -1
    if n == 2:
        while len(decoded_phrase) != len(string):
            if index == 0:
                int_index_start += 1
                decoded_phrase += decoded[index][int_index_start]
                index += 1
            elif index == 1 and len(decoded_phrase) != len(string):
                int_index_end += 1
                decoded_phrase += decoded[index][int_index_end]
                index -=1
    else:        
        while len(decoded_phrase) != len(string):

            if index == 0:
                count += 1
                int_index_start += 1
                decoded_phrase += decoded[index][int_index_start]
                index += 1
                int_index_middle += 1

            if len(decoded_phrase) == len(string):
                break

            if count % 2 == 0:
                decoded_phrase += decoded[index][int_index_middle]
                index += 1
            else:
                decoded_phrase += decoded[index][int_index_middle]
                index -= 1

            if len(decoded_phrase) == len(string):
                break

            if index == n - 1:
                count += 1
                int_index_end += 1
                decoded_phrase += decoded[index][int_index_end]
                index -= 1
                int_index_middle += 1

            if len(decoded_phrase) == len(string):
                break
    
    return decoded_phrase
_____________________________
def encode_rail_fence_cipher(string, n):
    arr = []
    for i in range(n):
        h = []
        for j in range(len(string)):
            h.append('')
        arr.append(h)

    i, j, let = 0, 0, 0
    switch = False
    while let < len(string):
        arr[i][j] = string[let]
        let += 1
        if (i == n-1 and j == n-1) or switch:
            switch = True
            i -= 1
            j += 1
            print(i, j)
            if i == 0:
                switch = False  
            
        elif not switch:
            i += 1
            j += 1
            if i == n-1:
                switch = True        
    res = ''
    for each in arr:
        res += ''.join(each)
    return res


def decode_rail_fence_cipher(string, n):
    arr = [["" for i in range(len(string))] 
                  for j in range(n)]
    switch = False
    row, col = 0, 0
    for i in range(len(string)):
        if row == 0:
            switch = True
        if row == n - 1:
            switch = False
        arr[row][col] = '*'
        col += 1
        if switch:
            row += 1
        else:
            row -= 1  
    c = 0
    for i in range(n):
        for j in range(len(string)):
            if ((arr[i][j] == "*") and (c < len(string))):
                arr[i][j] = string[c]
                c += 1
    row, col = 0, 0
    res = ''
    for i in range(n):
        for j in range(len(string)):
            if row == 0:
                switch = True
            if row == n - 1:
                switch = False
            if col < len(string):
                res += arr[row][col]
                col += 1
            if switch:
                row += 1
            else:
                row -= 1
    return res

