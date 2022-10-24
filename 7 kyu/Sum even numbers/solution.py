586beb5ba44cfc44ed0006c3


def sum_even_numbers(seq): 
    return sum(x for x in seq if x%2==0)
_______________________________________
def sum_even_numbers(seq): 
    return sum(filter(lambda n: n%2==0, seq))
_______________________________________
def sum_even_numbers(seq): 
    L=[]
    for i in seq:
        if i%2==0:
            L.append(i)
    return sum(L)
_______________________________________
def sum_even_numbers(seq): 
    return sum(i for i in seq if i%2 == 0)
_______________________________________
def sum_even_numbers(seq):
    to_sum = [num for num in seq if num % 2 == 0]
    return sum(to_sum)
_______________________________________
def sum_even_numbers(seq): 
    sum = 0
    for i in range(len(seq)):
        if seq[i] % 2 == 0:
            sum += seq[i]
    return sum
_______________________________________
sum_even_numbers = lambda _: sum(filter(lambda __: not __%2,_))
_______________________________________
def sum_even_numbers(seq):
    resultado = 0
    for enum in seq:
        if enum%2 == 0:
            resultado += enum
    return resultado
_______________________________________
def sum_even_numbers(seq): 
    return sum([seq[i] for i in range(len(seq)) if seq[i]%2 == 0])
    pass
