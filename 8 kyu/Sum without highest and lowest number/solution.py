def sum_array(arr):
    if arr == None or len(arr) < 3:
        return 0
    return sum(arr) - max(arr) - min(arr)
________________________________________
def sum_array(arr):
    return sum(sorted(arr)[1:-1]) if arr and len(arr) > 1 else 0
________________________________________
def sum_array(arr):
    return 0 if arr == None else sum(sorted(arr)[1:-1])
________________________________________
def sum_array(arr):
    return sum(arr) - min(arr) - max(arr) if arr and len(arr) > 1 else 0
________________________________________
def sum_array(arr):
    return sum(sorted(arr or [])[1:-1])
________________________________________
def sum_array(arr):
  
  if arr is None or len(arr) < 2:
    return 0
  
  mi, ma, s = arr[0], arr[0], 0
  
  for x in arr:
    if x > ma:
      ma = x
    elif x < mi:
      mi = x
    
    s += x
  
  return s - mi - ma

________________________________________
def sum_array(arr):
    if arr==None:
        return 0       
    elif len(arr)>1:
        arr.pop(arr.index(max(arr)))
        arr.pop(arr.index(min(arr)))
        return sum(arr)
    else:
        return 0
________________________________________
def sum_array(arr):
    return 0 if isinstance(arr, list) and len(arr) < 3 or not arr else sum(arr) - min(arr) - max(arr)
________________________________________
def sum_array(arr):
    if arr is None:
        Sorted = 0
        return Sorted
    elif not arr:
        Sorted = 0
        return Sorted
    elif len(arr) == 1:
        Sorted = 0
        return Sorted
    elif len(arr) == 2:
        SumUp = 0
        return SumUp
    else:
        Sorting = sorted(arr)
        LenList = len(arr)
        LenList = LenList - 1
        Group = sum(arr)
        Group = Group - Sorting[0]
        Group = Group - Sorting[LenList]
        return Group
