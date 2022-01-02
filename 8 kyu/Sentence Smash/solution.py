def smash(words):
    return " ".join(words)
  
_____________________________________
smash = ' '.join

_____________________________________
smash=lambda x:' '.join(x)

_____________________________________
def smash(words):
  smashed=""
  for i in words:
    smashed=smashed+i+" "
  return smashed[:-1]

_____________________________________
def smash(words):
    str = ""
    if words  != []:
        str = " ".join(words)
    
    return str
    
_____________________________________
def smash(words):
    arr_len = len(words)
    
    if(arr_len == 0):
        return ""
    elif(arr_len == 1):
        return words[0]
    else:
        return " ".join(words)
      
_____________________________________
def smash(words):
    list=[]
    for i in words:
        if words.index(i)<len(words)-1:
            list.append(i+" ")
        else:
            list.append(i)
    return "".join(list)
