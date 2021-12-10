def men_from_boys(arr):
    arr = list(set(arr))
    men = sorted([x for x in arr if x % 2 == 0])
    boys = sorted([x for x in arr if x not in men], reverse = True)
    return men + boys
  
###############
def men_from_boys(arr):
    men = []
    boys = []
    for i in sorted(set(arr)):
        if i % 2 == 0:
            men.append(i)
        else:
            boys.append(i)
    return men + boys[::-1]
  
##############
def men_from_boys(arr):
    return sorted(set(arr), key=lambda n: (n%2, n * (-1)**(n%2)))
  
##########
def men_from_boys(arr):
    evens = {x for x in arr if x%2==0}
    odds = {x for x in arr if x%2==1}
    return sorted(list(evens))+sorted(list(odds), reverse=True)
  
###########
def men_from_boys(arr):
    arr = list(set(arr))
    return sorted([x for x in arr if x % 2 == 0]) + sorted([x for x in arr if x % 2 != 0], reverse=True)
  
############
def men_from_boys(arr):
    return sorted(set(arr), key=lambda a: (a % 2, [a, -a][a % 2]))
  
############
def men_from_boys(arr):
    sorted_unique_arr = sorted(set(arr))
    men, boys = [], []
    for d in sorted_unique_arr:
        if d % 2 == 0: men = men + [d]
        else: boys = [d] + boys
    return men+boys
  
#############
def men_from_boys(arr):
    men = sorted(list(set([i for i in arr if i % 2 == 0])))
    boys = sorted(list(set([j for j in arr if j % 2 != 0])), reverse=True)
    return men + boys
  
############
def men_from_boys(arr):
    return sorted(set(filter(lambda n: n % 2 == 0, arr))) + sorted(set(filter(lambda n: n % 2, arr)), reverse=True)

################
def men_from_boys(arr):
    even_num = []
    odd_num = []
    for i in sorted(set(arr)):
        if i % 2 == 0:
            even_num.append(i)
        else:
            odd_num.append(i)
    return even_num + odd_num[::-1]
  
#################
def men_from_boys(arr):
    boys, men = [], []
    
    for i in arr:
        if i % 2 == 0:
            if i not in men:
                men.append(i)
        else:
            if i not in boys:
                boys.append(i)
    
    return sorted(men) + sorted(boys, reverse=True)
  
##################
def men_from_boys(arr):
    return sorted({c for c in arr if c % 2 == 0}) + sorted({c for c in arr if c%2}, reverse=True)
  
###############
def men_from_boys(arr):
    arr = sorted(set(arr))
    isodd = []
    iseven = []
    for i in arr:
        if i % 2 == 0:
            iseven.append(i)
        else:
            isodd.append(i)            
    iseven.extend(isodd[::-1])
    return iseven
