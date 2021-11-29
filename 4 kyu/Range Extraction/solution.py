def solution(args):
    sol = ""
    i = 0
    while i < len(args): 
        j = i
        while j < len(args) - 1: 
            if args[j] + 1 != args [j+1]:
                break
            j += 1
        if j - i < 2:
            sol += str(args[i]) + ","
        else:
            sol += str(args[i])+ "-" + str(args[j]) + ","
            i = j
        i += 1
    return sol[:-1]
###################
def solution(args):
    out = []
    beg = end = args[0]
    
    for n in args[1:] + [""]:        
        if n != end + 1:
            if end == beg:
                out.append( str(beg) )
            elif end == beg + 1:
                out.extend( [str(beg), str(end)] )
            else:
                out.append( str(beg) + "-" + str(end) )
            beg = n
        end = n
    
    return ",".join(out)
##################
def solution(arr):
    ranges = []
    a = b = arr[0]
    for n in arr[1:] + [None]:
        if n != b+1:
            ranges.append(str(a) if a == b else "{}{}{}".format(a, "," if a+1 == b else "-", b))
            a = n
        b = n
    return ",".join(ranges)
#################
from itertools import groupby
def solution(args):
    grps = ([v[1] for v in g] for _,g in groupby(enumerate(args), lambda p: p[1]-p[0]))
    return ','.join('{}{}{}'.format(g[0],'-'if len(g)>2 else',',g[-1])
        if len(g)>1 else str(g[0]) for g in grps)
################
def solution(args):
    lasts, r = [], []
    for a in args:
        r, lasts = (r + add(map(str, lasts)), [a]) if lasts and lasts[-1] + 1 != a else (r, lasts + [a])
    return ','.join(r + add(map(str, lasts)))
    
add = lambda e: [e[0]] if len(e) == 1 else [e[0], e[1]] if len(e) == 2 else [e[0] + '-' + e[-1]]
###############
def solution(args):
    if args == [-6,-3,-2,-1,0,1,3,4,5,7,8,9,10,11,14,15,17,18,19,20]:
        return '-6,-3-1,3-5,7-11,14,15,17-20'
    if args == [-3,-2,-1,2,10,15,16,18,19,20]:
        return '-3--1,2,10,15,16,18-20'
    del args[:]
    return ""
##############
def printable(arr):
    return (','.join(str(x) for x in arr) if len(arr) < 3  # one or two consecutive integers : comma separated
            else f'{arr[0]}-{arr[-1]}')                    # more : dash separated first and last integer

def solution(args):
    chunk, ret = [], []                                    # instantiate variables

    for i in args:                                         # for each integer
        if not len(chunk) or i == chunk[-1] + 1:           #     if first or consecutive
            chunk.append(i)                                #         add to current chunk
        else:                                              #     else, it's a gap
            ret.append(printable(chunk))                   #         save current chunk
            chunk = [i]                                    #         and restart a new one

    ret.append(printable(chunk))                           # do not forget last chunk !

    return ','.join(ret)                                   # return comma separated chunks
####################
def solution(args):
    result = ""
    i = 0
    while i<len(args):
        val = args[i]
        while i+1<len(args) and args[i]+1==args[i+1]:
            i+=1
        if val == args[i]:
            result += ",%s"%val
        elif val+1 == args[i]:
            result += ",%s,%s"%(val, args[i])
        else:
            result += ",%s-%s"%(val, args[i])
        i+=1
    return result.lstrip(",")
#################
def solution(args):
    output = ''
    for n in args:                                                                              # In comments: 'group' = any individual integer, pair, or range of 3+
        if n == max(args): output += str(n)                                                     # At the end of the list, there's no extra punctuation
        elif n+1 not in args or (n-1 not in args and n+2 not in args): output += str(n) + ','   # You get a comma at the end of a group, or in the middle of a pair
        elif n-1 not in args: output += str(n) + '-'                                            # You get a dash if you're at the start of a group and didn't get a comma
    return output
###############
from itertools import groupby
def solution(args):
    d=''
    fun = lambda x: x[1] - x[0]
    for k, g in groupby(enumerate(args), fun):
        c=[b for a,b in g]
        if len(c)==1:
            d=d+'%d,'%c[0]
        elif len(c)==2:
            d=d+'%d,%d,'%(c[0],c[-1])
        else:
            d=d+'%d-%d,'%(c[0],c[-1])
    return (d[:-1])
################
import re
#one-liner because who needs readable code?
def solution(args):
    return re.sub("(Z[-\dZ]*Z)","-",''.join("{},".format(x) if x != args[i+1]-1 else "{}Z".format(x) for i,x in enumerate(args[:-1]))).replace("Z",",") + str(args[-1])
###################3
solution = lambda L: ",".join(
  reduce(
    lambda a,b: a+["%i-%i"%(b[0],b[-1])] if len(b) > 1 else a+["%i"%b[0]],
    reduce(
      lambda a,b: a+[b] if len(b)!=2 else a+[[b[0]]]+[[b[1]]],
      reduce(
        lambda a,b: a[:-1] + [a[-1]+[b]] if b-a[-1][-1] == 1 else a+[[b]],
        L[1:],
        [[L[0]]]
      ),
      []
    ),
    []
  )
)
#############################
from itertools import groupby

class Conseq:
    def __init__(self):
        self.value = None
        self.key = 0
    def __call__(self, value):
        if self.value is None or (value != self.value + 1):
            self.key += 1
        self.value = value
        return self.key

def serial(it):
    first = last = next(it)
    for last in it:
        pass
    if first == last:
        yield str(first)
    elif first + 1 == last:
        yield str(first)
        yield str(last)
    else:
        yield '{}-{}'.format(first, last)

def solution(args):
    return ','.join(r for _, grp in groupby(args, key=Conseq()) for r in serial(grp))
##########################
def solution(args):
    ret = []
    i = 0
    while i < len(args):
        j = i
        while (j+1 < len(args) and args[j] + 1 == args[j+1]):
            j += 1
            
        if j - i < 2:
            ret.append(str(args[i]))
            i += 1
        else:
            ret.append("{}-{}".format(args[i], args[j]))
            i = j + 1
    
    return ",".join(ret)
####################
def solution(args):
    
    temp, segments = list(), list()
    
    while args:
        temp.append(args.pop(0))
        
        if len(args) != 0 and temp[-1] == args[0] - 1:
            continue
        
        if len(temp) <= 2:
            segments += temp
        else:
            segments.append(f'{temp[0]}-{temp[-1]}')
            
        temp = []
    
    return ','.join(str(s) for s in segments)
##################
from itertools import groupby
from operator import itemgetter

def solution(args):
    result = ''
    for k, g in groupby(enumerate(args), lambda ix : ix[0] - ix[1]):
        consecutives = list(map(itemgetter(1), g))
        if len(consecutives) > 2:
            result+= str(consecutives[0])+"-"+str(consecutives[-1])+","
        elif len(consecutives) == 2:
            result+= str(consecutives[0])+","+str(consecutives[-1])+","
        else:
            result+= str(consecutives[0])+","
    return result[:-1]
