def summation(num):
    return sum(range(num + 1))
#############
def summation(num):
    return (1+num) * num / 2
##############
def summation(num):
    return sum(range(1,num+1))
##############
summation=lambda n:n*-~n>>1
############
def summation(num):
    if num > 1:
       return num + summation(num - 1)
    return 1
##############
def summation(num):
    return num/2*(2*1+(num-1)*1) # Sn = n/2[2a+(n-1)d]
###############
def summation(num):
    total = 0
    for i in range(0, num+1):
        total = total + i
    return total
##############
summation = lambda x: sum(range(1, x + 1))
#############
def summation(num):
    fac = 0 
    i = 0 
    while i < num:
        i += 1
        fac = fac + i
    return fac
##############
summation  = lambda num: sum([i for i in range(num)], num)
#############
def summation(num):
    if num ==1:
        return 1
    return sum([num,summation(num-1)])
