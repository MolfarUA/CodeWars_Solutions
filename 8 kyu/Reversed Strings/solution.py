def solution (string):
    return string[::-1]

def tests():
    if solution ('workd') != 'dlrow':
        print ('Not correct')
    if solution('hello') != 'olleh':
        print ('Not correct')

tests()
##################
def solution(str):
  return str[::-1]
################
solution = lambda s: s[::-1]
################
def solution(string):
    newstring = ""
    letter = len(string) - 1
    for x in string:
        x = string[letter]
        newstring = newstring + x
        letter = letter -1 
    return newstring
####################
def solution(string):
    temp = list(string)
    temp.reverse()
    return ''.join(temp)
###################
def solution(string):
    s1=''
    for x in string:
        s1= x+s1
    return s1 
##################
def solution(string):
    if len(string) == 5:
      return string[4] + string[3] + string[2] + string[1] + string[0]
    if len(string) == 4:
      return string[3] + string[2] + string[1] + string[0]
    if len(string) == 3:
      return string[2] + string[1] + string[0]
    if len(string) == 2:
      return string[1] + string[0]
    if len(string) == 1:
      return string[0]
    if len(string) == 0:
      return ""
    pass
################
def solution(s):
    return s[::-1]
###############
def solution(string):
    return ''.join(i for i in reversed(string))
##############
def solution(string):
    s = list(string)
    j = len(s)-1
    for i in range(len(s)):
        if (i<j):
            s[i], s[j] = s[j], s[i]
            j = j-1
        else:
            continue
    s1 = ''.join(s)
    return s1
#################
solution=lambda s:s[-1::-1]
################
def solution(string):
    charlist = []
    res = ""
    for l in string:
        charlist.append(l)
    charlist.reverse()
    for c in charlist:
        res=res+c
    return res
###################
def solution(string):
    reverse = ""
    for i in string:
        reverse = i + reverse
    return reverse
###############
def solution(string: str) -> str:
    return string[::-1]
##############
solution = lambda x:x[::-1]
###############
def solution(string):
    lst = []
    reversed = ''
    for letter in string:
        lst.insert(0, letter)
    for letter in lst:
        reversed += letter
    return reversed
#################
def solution(string):
    L=[]
    for i in string:
        L.append(i)
    L.reverse()
    return ''.join(L)
