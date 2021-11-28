def averages(arr):
    averages = []

    if arr:
        for i in range(1, len(arr)):
            average = (arr[i - 1] + arr[i]) / 2
            averages.append(average)

    return averages
###################
def averages(arr):
    return [(arr[x]+arr[x+1])/2 for x in range(len(arr or [])-1)]
##############
def averages(arr):
    output = []
    try:        
        for i in range(len(arr)-1):
            output.append( (arr[i]+arr[i+1]) / 2 )        
        return output
    
    except:
        return output
##############
def averages(arr):
    return [(arr[i] + arr[i-1]) / 2 for i in range(1, len(arr))] if arr else []
##############
def averages(arr):
    if arr:
        return list(map(lambda x,y: (x+y)/2, arr, arr[1:]))
    else:
        return []
##############
def averages(arr):
  
  if arr is None or len(arr) < 2:
    return []
  
  return [(arr[i] + arr[i+1]) / 2 for i in range(len(arr)-1) ]
################
def averages(lst):
    return [(a + b) / 2 for a, b in zip(lst, lst[1:])] if isinstance(lst, list) else []
###############
mean = lambda x,y: (x+y)/2

def averages(arr):
    return list(map(mean, arr, arr[1:])) if arr else []
##############
def averages(arr):
    return [] if arr==None else [(arr[i]+arr[i+1])/2 for i in range(len(arr)-1)]
##############
def averages(arr):
    return [(arr[i] + arr[i + 1]) / 2.0 for i in range(len(arr) - 1)] if arr else []
#############
def averages(arr):
  return [(a+b)/2. for a, b in zip(arr, arr[1:])] if arr else []
##############
def averages(arr):
    if arr is None: return []
    return [(x + y) / 2 for x, y in zip(arr[:-1], arr[1:])]
##############
def averages(arr):
    return [(x + y) / 2 for x, y in zip(arr[:-1], arr[1:])] if arr else []
##############
def averages(arr):
    return arr and [(x + y) / 2 for x, y in zip(arr, arr[1:])] or []
#############
averages=lambda a:[]if not a else list(map(lambda x:sum(x)/2,zip(a[:-1],a[1:])))
