def filter_list(l):
      return [x for x in l if type(x) == int]
  
_____________________________________________
def filter_list(l):
  'return a new list with the strings filtered out'
  return [i for i in l if not isinstance(i, str)]

_____________________________________________
def filter_list(l):
  'return a new list with the strings filtered out'
  return [x for x in l if type(x) is not str]

_____________________________________________
def filter_list(l):
  'return a new list with the strings filtered out'
  return [e for e in l if isinstance(e, int)]

_____________________________________________
def filter_list(l):
    x = []
    for i in l:
        if i not in x and type(i) is int:
            x.append(i)
    return x
  
_____________________________________________
def filter_list(l):
    nl = []
    for i in l:
        if type(i) == int:
            nl.append(i)
        else:
            pass
    
    return nl
  
_____________________________________________
def filter_list(l):
    stringless_list = []
    for i in l:
        if i != str(i):
            stringless_list.append(i)
    return stringless_list
  
_____________________________________________
def filter_list(l):
   return [n for n in l if type(n) ==int]
print(filter_list([3,7,'hi']))

_____________________________________________
def filter_list(l):
    list_new = []
    for x in l:
        if type(x) != str:
            list_new.append(x)
    return list_new
    
    
a = filter_list([1,2,3,"a","b"])
print(a)

_____________________________________________
def filter_list(l):
    str_new = []
    for i in l:
        if type(i) != str:
            str_new.append(i)
    return str_new
  
_____________________________________________
def filter_list(l):
    return [element for element in l if type(element) is type(0)]
