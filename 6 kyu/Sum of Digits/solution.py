def sum_of_digits(n):
    result = 0
    for digit in list(str(n)):
        result += int(digit)
    return result

def digital_root(n):
    result = sum_of_digits(n)
    while result > 9:
        result = sum_of_digits(result)
    return result
  
_______________________________________
def digital_root(n):
    return n if n < 10 else digital_root(sum(map(int,str(n))))
  
_______________________________________
def digital_root(n):
    return n%9 or n and 9 
  
_______________________________________
def digital_root(n):
    # ...
    while n>9:
        n=sum(map(int,str(n)))
    return n
  
_______________________________________
def digital_root(n):
    def sm(x):
        return sum(int(i) for i in str(x))
    
    st= sm(n)
    while len(str(st))>1:
        st=sm(st)

    return (st)
    
_______________________________________
def digital_root(n):
    tmp=str(n)
    res=999
    while(len(str(res))!=1):
        res=0
        for i in tmp:
            res+=int(i)
        tmp=str(res)
    return res
  
_______________________________________
def digital_root(n):
    while True:
        s = str(n)
        if len(s) <= 1:
            break
        n = sum(int(x) for x in s)
    return n
  
_______________________________________
def digital_root(n):
    number = list(str(n))
    number = [int(i) for i in number]
    total = sum(number)
    print(total)
    while len(list(str(total))) >= 2:
        number = list(str(total))
        number = [int(i) for i in number]
        total = sum(number) 
        print(total)
    return int(total)
