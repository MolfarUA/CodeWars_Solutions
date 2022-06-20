566fc12495810954b1000030


def nb_dig(n, d):
    return sum(str(i*i).count(str(d)) for i in range(n+1))
____________________________
def nb_dig(n, d):
    return ''.join(str(a ** 2) for a in xrange(n + 1)).count(str(d))
____________________________
def nb_dig(n, d):
    
    tot_occur = 0;
    
    for i in range(n+1):
        #print(i**2)
        tot_occur += str(i**2).count(str(d))
        
    return tot_occur
____________________________
def nb_dig(n, d):
   return ''.join(str(n * n) for n in range(n + 1)).count(str(d))
____________________________
def nb_dig(n, d):
    return sum([str(x**2).count(str(d)) for x in range(n+1)])
____________________________
nb_dig = lambda n,d: sum(str(k**2).count(str(d)) for k in range(n+1))
____________________________
nb_dig=lambda n,d:sum(str(i**2).count(str(d))for i in range(n+1))
____________________________
def nb_dig(n, d):
    integers = [str(integer ** 2) for integer in range(n + 1)]
    return sum([digits.count(str(d)) for digits in integers])
____________________________
def nb_dig(n, d):
    string = ''
    count = 0
    
    for i in range(n+1):
        string += str(i*i)
    
    for i in string:
        if i == str(d):
            count += 1

    return count
