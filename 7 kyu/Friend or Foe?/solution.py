55b42574ff091733d900002f

def friend(x):
    return [i for i in x if len(i) == 4]
##########
def friend(x):
    myFriends = []                   # Initialize list variable
    for person in x:                 # Loop through list of names 
        if len(person) == 4:         # Check to see if the name is of length 4
            myFriends.append(person) # If the name is 4 characters long, append it to variable myFriends
    return myFriends                 # Return myFriends list
###########
def friend(x):
    return filter(lambda name: len(name) == 4, x)
##########
def friend(x):
    return list(filter(lambda s : len(s)==4 ,x))
###########
def friend(x):
    return [each for each in x if len(each) == 4]
###########
def friend(x):
    newlist = []
    for friend in x:
        if len(friend) == 4 and not friend.isdigit():
            newlist.append(friend)
    return newlist
###########
def friend(list):
    new_list = []
    for word in list:
        length = len(word)
        if length == 4:
            new_list.append(word)
    return new_list
###########
def friend(x):
    kawan = []
    for org in x:
        if len(org) == 4:
            kawan.append(org)
    return kawan
###########
def friend(x):
    result = []
    for name in x:
        if name and len(name) == 4:
            result.append(name)
    return result
############
def friend(input):
    output = []
    for i in range(len(input)):
        if len(input[i]) == 4:
            output.append(input[i])
    return output
#########
def friend(x):
    listOfNames = list(x)
    friends = []
    
    for n in listOfNames:
        if len(n) == 4:
            friends.append(n)
            
    return friends
________________________________
def friend(x):
    shouldBe = [friend for friend in x if len(friend) == 4]
    return shouldBe
________________________________
def friend(x):
    lista = []
    for i in x:
        if len(i) != 4:
            continue
        else:
            lista.append(i)
    
    return lista
________________________________
def friend(f):
    friends = []
    count = 0
    for i in f:
        if len(i) == 4:
            friends.append(i)
    return friends
