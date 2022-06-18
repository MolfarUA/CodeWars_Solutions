def digitize(n):
    return map(int, str(n)[::-1])
________________________
def digitize(n):
    return [int(x) for x in str(n)[::-1]]
________________________
def digitize(n):
    return [int(x) for x in reversed(str(n))]
________________________
def digitize(num):
    num_list = []
    num = str(num)
    for _ in range(len(num)):
        remainder = int(num)%10
        num = int(num)//10
        num_list.append(remainder)
    return num_list
________________________
def digitize(n):
    myString=str(n)
    myList=[]
    for i in myString:
        myList.insert(0,int(i))
    return myList
________________________
def digitize(n):
    list_numbers_to_strings = [str(n)[digit] for digit in range(len(str(n)))]
    list_strings_to_numbers = [int(digit) for digit in list_numbers_to_strings]
    return list(reversed(list_strings_to_numbers))
________________________
def digitize(n):
    out = []
    n = str(n)
    for i in range(len(n)):
        out.append(int(n[i]))
    out.reverse()
    return out
________________________
def digitize(n):
    dl = len(str(n))
    a = str(n)
    lista = []
    for i in range(dl):
        lista.insert(0, int(a[i]))
        print (lista)
    return lista
________________________
def digitize(n):
    q = str(n)
    s = [x for x in q]
    s = s[::-1]
    s = [int(x) for x in s]
    return s 
________________________
def digitize(n):
    nString = str(n)
    listString=list(nString)
    reversedArray=list(reversed(listString))
    for i in range(0, len(reversedArray)):
        reversedArray[i]=int(reversedArray[i])
    print (reversedArray)
    return reversedArray
