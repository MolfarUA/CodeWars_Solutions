def permutations(string):
    if len (string) == 1:
        return string
    answer = []
    for x in string:
        answer = answer + list(map(lambda p: x + p, permutations(string.replace(x,'',1))))
    return set(answer)
###########################
def permutations(string):
  if len(string) == 1: return set(string)
  first = string[0]
  rest = permutations(string[1:])
  result = set()
  for i in range(0, len(string)):
    for p in rest:
      result.add(p[0:i] + first + p[i:])
  return result
###########################
import itertools
def permutations(string):
    return set(''.join(x) for x in itertools.permutations(string, r=len(string)))
########################
def permutations(s):
    if len(s) == 0:
        return []
    elif len(s) == 1:
        return [s]
    else:
        return set(s[i]+p for i in range(len(s)) for p in permutations(s[:i] + s[i+1:]))
##########################
def permutations(s):        
    if(len(s)==1): return [s]
    result=[]
    for i,v in enumerate(s):
        result += [v+p for p in permutations(s[:i]+s[i+1:])]
    return list(set(result))
