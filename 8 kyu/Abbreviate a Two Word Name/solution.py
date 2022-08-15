57eadb7ecd143f4c9c0000a3


def abbrev_name(name):
    initials = ''
    arr = name.split()
    for n in arr:
        initials += n[0].upper() + '.'
        
    print(initials[0:-1])
    return initials[0:-1]
###############
def abbrevName(name):
    return '.'.join(w[0] for w in name.split()).upper()
###############
def abbrevName(name):
    first, last = name.upper().split(' ')
    return first[0] + '.' + last[0]
###############
def abbrevName(name):
    return name.split(' ')[0][0].upper()+'.'+name.split(' ')[1][0].upper()
################
def abbrevName(name):
    return '.'.join(filter(str.isupper,name.title()))
###############
def abbrevName(name):
    names = name.split()
    return f"{names[0][0]}.{names[1][0]}".upper()
#################
def abbrevName(name):
    return '.'.join(x[0].upper() for x in name.split())
#####################
def abbrevName(name):
    x = name
    y = name.split()
    return y[0][0].upper() + "." + y[1][0].upper()
##############
def abbrevName(name):
    first_initial = name[0]
    for letter in range(len(name)):
        if name[letter]  == ' ':
            last_initial = name[letter + 1]
          
    return (first_initial.upper() + "." + last_initial.upper())
#####################
abbrevName = lambda name: ".".join(e[0].upper() for e in name.split())
############
def abbrevName(name):
    n = name.upper().split(' ')
    return n[0][0]+'.'+n[1][0]
##############
def abbrev_name(name):
    name = name.upper()
    return f'{name.split()[0][0]}.{name.split()[1][0]}'
################
def abbrev_name(name):
    for i, x in enumerate(name):
        if x == ' ':
            y = i + 1
            z = name[y]
                
    return name[0].upper() + '.' + z.upper()
#################
def abbrev_name(name):
    return '.'.join([word[0] for word in name.split(' ')]).upper()
#################
def abbrevName(name):
    n,s="",name.split(" ")
    for i in range(2):
        n+=s[i][0].upper()+"."
    return n[:3]  
