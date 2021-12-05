def min_max(lst):
    res=[]
    res.append(min(lst))
    res.append(max(lst))
    return(res)
##########
def min_max(lst):
  return [min(lst), max(lst)]
########
def min_max(lst):
  lst.sort()
  tempor = [lst[0],lst[-1]]
  return tempor
############
def min_max(lst):
    bagr = sorted(lst)
    array = [bagr[0], bagr[len(lst)-1]]
    return array
##########
def min_max(lst):
    MAX = max(lst)
    MIN = min(lst)
    
    minMax = [MIN, MAX]
    
    return minMax
###########
def min_max(lst):
    if lst:
        return [min(lst), max(lst)]
    return lst
###########
def min_max(lst):
    list = []
    minl = min(lst)
    maxl = max(lst)
    list.append(minl)
    list.append(maxl)
    return list
########
def min_max(lst):
    max_in = max(lst)
    min_in = min(lst)
    return([min_in,max_in])
#############
def min_max(lst):
    result_lst = []
    result_lst.append(min(lst))
    result_lst.append(max(lst))
    return result_lst
##########
def min_max(lst):
    mini=lst[0]
    maxi=lst[0]
    k=0
    while k<len(lst):
        x=lst[k]
        if x<mini:
            mini=x
        elif x>maxi:
            maxi=x
        k=k+1
    return [mini,maxi]
  ##############
  def min_max(lst):
    res =[ sorted(lst)[0], sorted(lst)[-1]]
    return res
  ###########
  def min_max(lst):
    lst.sort()
    sorted_lst = list(lst)
    sorted_lst2 = [sorted_lst[0],sorted_lst[-1]]
    return sorted_lst2 
