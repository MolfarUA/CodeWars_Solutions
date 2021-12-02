def maskify(cc):
    return "#"*(len(cc)-4) + cc[-4:]
###########
def maskify(cc):
    l = len(cc)
    if l <= 4: return cc
    return (l - 4) * '#' + cc[-4:]
###############
def maskify(cc):
    return '{message:#>{fill}}'.format(message=cc[-4:], fill=len(cc))
###########
def maskify(cc):
  
  word = list(cc)
  #loop through the list except the last 4 index's this will also prevent
  #the loop from running for anything less than 5 index's long
  for i in range(len(word) - 4):
    word[i] = '#'
  # join and return the list
  return ''.join(word)
  pass
####################
def maskify(cc):
    return len(cc[:-4])*"#" + cc[-4:]
################
def maskify(cc):
    width = len(cc)
    return cc[-4:].rjust(width, '#')
##############
def maskify(cc):
    return cc[-4:].rjust(len(cc), "#")
############
def maskify(cc):
    if len(cc) < 4:
        return cc
    return "#" * (len(cc)-4) + cc[-4:]
##############
def maskify(cc):
    newstring = ''
    for character in cc[0:-4]:
        newstring += '#'
    for number in cc[-4:]:
        newstring += number
    return newstring
#############
def maskify(cc):
    return "".join(["#" if i < len(cc) - 4 else cc[i] for i in range(len(cc))])
