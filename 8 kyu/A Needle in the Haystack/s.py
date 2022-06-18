def find_needle(haystack): return 'found the needle at position %d' % haystack.index('needle')
________________________
def find_needle(haystack):
    return 'found the needle at position {}'.format(haystack.index('needle'))
________________________
def find_needle(haystack):
    return f'found the needle at position {haystack.index("needle")}'
________________________
def find_needle(haystack):
    for i, x in enumerate(haystack):
        if x == 'needle': 
            return 'found the needle at position %d' % i
________________________
def find_needle(haystack):
    n=1
    while n<= len(haystack):
        
        if haystack[n-1]=='needle':
            nfind='found the needle at position '
            break
        n+=1
    return nfind+str(n-1)
________________________
def find_needle(haystack):
    return "found the needle at position {}".format(haystack.index("needle")) if haystack.count("needle") ==1 else None
________________________
def find_needle(haystack):
    position = 0
    for needle in haystack:
        position = position + 1
        if needle == 'needle':
            position = position - 1
            break
        
    return 'found the needle at position ' + str(position)
________________________
def find_needle(haystack):
    string = iter(haystack)
    for i in range(len(haystack)):
        if "needle" == next(string):
            return ("found the needle at position {}".format(i))
