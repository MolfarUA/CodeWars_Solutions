def single_digit(n):
    while n > 9:
        n = bin(n).count("1")
    return n
__________________________
def single_digit(n):
  return n if n<10 else single_digit(bin(n).count("1"))
__________________________
def single_digit(n):
    while n > 9:
        n = int(bin(n).count('1'))
    return n
__________________________
def single_digit(n):
    while n > 9:
        out = 0
        for i in bin(n)[2:]:
            out += int(i)
            
        n = out
    return n
__________________________
def single_digit(n):
    if len(str(n)) == 1:
        return n
    else:
        return single_digit(bin(n)[2:].count('1'))
__________________________
s=single_digit=lambda n:n if n<10else s(sum(map(int,bin(n)[2:])))
__________________________
def single_digit(n):
    while n/10>=1:
        n=sum(map(int, bin(n)[2:]))
    return n
__________________________
def single_digit(n):
    return n  if n < 10 else single_digit(sum(  int(d) for d in  bin(n)[2:]))
__________________________
def single_digit(n):
    while len(str(n)) != 1:
        n = sum(map(int, bin(n)[2:]))
    return n
__________________________
def single_digit(n):
    if n > 9:
        n = single_digit(bin(n).count('1'))
    return n
__________________________
single_digit = lambda n: n if n<10 else single_digit(sum(c=='1' for c in bin(n)))
__________________________
def single_digit(n):
    while n > 9:
        n = sum(1 if i == "1" else 0 for i in bin(n))
    return n
__________________________
def single_digit(n):
    while n >= 10:
        n = sum(c == '1' for c in bin(n))
    return n
__________________________
single_digit=s=lambda n:s(bin(n).count('1'))if n>9else n
