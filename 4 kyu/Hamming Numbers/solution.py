def hamming(n):
    h = [1] * n
    x2, x3, x5 = 2, 3, 5
    i = j = k = 0
    
    
    for a in range(1, n):
        h[a] = min(x2, x3, x5)
        if x2 == h[a]:
            i += 1
            x2 = 2 * h[i]
        if x3 == h[a]:
            j += 1
            x3 = 3 * h[j]
        if x5 == h[a]:
            k += 1
            x5 = 5 * h[k]
    return h[n-1]
  
___________________________________________________
def hamming(n):
    bases = [2, 3, 5]
    expos = [0, 0, 0]
    hamms = [1]
    for _ in range(1, n):
        next_hamms = [bases[i] * hamms[expos[i]] for i in range(3)]
        next_hamm = min(next_hamms)
        hamms.append(next_hamm)
        for i in range(3):
            expos[i] += int(next_hamms[i] == next_hamm)
    return hamms[-1]
  
___________________________________________________
def hamming(n):
    num = [1]
    i, j, k = 0, 0, 0
    if n == 1:
      return 1;
    else:
      for e in range(1, n):
        x = min(2*num[i], 3*num[j], 5*num[k])
        num.append(x)
        if 2*num[i] <= x: i += 1
        if 3*num[j] <= x: j += 1
        if 5*num[k] <= x: k += 1
    return num[len(num) - 1];
  
___________________________________________________
def hamming(n):
    h = [1] * n
    x2 = 2
    x3 = 3
    x5 = 5
    i = j = k = 0
    for num in range(1, n):
        h[num] = min(x2, x3, x5)
        if h[num] == x2:
            i += 1
            x2 = h[i] * 2
        if h[num] == x3:
            j += 1
            x3 = h[j] * 3
        if h[num] == x5:
            k += 1
            x5 = h[k] * 5
    return h[-1]
  
___________________________________________________
unique={1}
cache={1}
while len(unique)<=15000:
    new_numbers=[2*i for i in cache]+[3*i for i in cache]+[5*i for i in cache]
    cache=unique.copy()
    unique.update(new_numbers)
    cache=unique-cache
unique=sorted(unique)
def hamming(n):
    return unique[n-1]
    """Returns the nth hamming number"""
    
___________________________________________________
def hamming(n):
    twos = [1,2]
    threes = [1,3]
    fives = [1,5]
    for count in range(1,34):
        twos.append(twos[count]*2)
    for count in range(1,20):
        threes.append(threes[count]*3)
    for count in range(1,17):
        fives.append(fives[count]*5)
    all  = []
    for two in twos:
        for three in threes:
            for five in fives:
                all.append(two * three *five)

    all.sort()
    
    return all[n-1]
  
___________________________________________________
def hamming(n):

    a, b, c = 0, 0, 0
    s = [1]

    while (len(s) < n):

        aa, bb, cc = 2 * s[a], 3 * s[b], 5 * s[c]

        m = min(aa,bb,cc)

        s.append(m)

        if aa <= m: a += 1
        if bb <= m: b += 1
        if cc <= m: c += 1

    return s[-1]
  
___________________________________________________
def hamming(n):

    a, b, c = 0, 0, 0
    s = [1]

    while (len(s) < n):

        aa, bb, cc = 2 * s[a], 3 * s[b], 5 * s[c]

        if aa < bb and aa < cc:
            s.append(aa)
            a += 1
        elif bb < aa and bb < cc:
            s.append(bb)
            b += 1
        elif cc < aa and cc < bb:
            s.append(cc)
            c += 1
        elif aa == bb == cc:
            s.append(aa)
            a += 1
            b += 1
            c += 1
        elif aa == bb:
            if aa < cc:
                s.append(aa)
                a += 1
                b += 1
            else:
                s.append(cc)
                c += 1
        elif aa == cc:
            if aa < bb:
                s.append(aa)
                a += 1
                c += 1
            else:
                s.append(bb)
                b += 1
        elif cc == bb:
            if cc < aa:
                s.append(cc)
                c += 1
                b += 1
            else:
                s.append(aa)
                a += 1

    return s[-1]
